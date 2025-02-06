# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.embedding_utils import compute_embedding, search_vector_db
from src.ollama_client import generate_response
from src.supabase_client import log_query_response
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500, description="La pregunta debe tener entre 5 y 500 caracteres")

@app.post("/query")
async def handle_query(query: QueryRequest):
    try:
        # Calcular embedding en un thread separado
        query_embedding = await run_in_threadpool(compute_embedding, query.question)
        relevant_articles = await run_in_threadpool(search_vector_db, query_embedding, 3)
        
        if not relevant_articles:
            raise HTTPException(status_code=404, detail="No se encontraron artículos relevantes.")
        
        prompt = f"Pregunta: {query.question}\n\nDocumentos relevantes:\n"
        for article in relevant_articles:
            prompt += (
                f"- {article['title']} (DOI: {article['doi']})\n"
                f"  Abstract: {article['abstract']}\n\n"
            )
        
        # Usar la nueva función de generación
        response_text = await run_in_threadpool(generate_response, prompt)
        
        await run_in_threadpool(log_query_response, query.question, response_text, relevant_articles)
    
        return {"response": response_text, "references": [article['doi'] for article in relevant_articles]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
