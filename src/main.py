# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from embedding_utils import compute_embedding, search_vector_db
from ollama_client import generate_response
from supabase_client import log_query_response

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def handle_query(query: QueryRequest):
    # 1. Calcular el embedding de la pregunta
    query_embedding = compute_embedding(query.question)
    
    # 2. Buscar artículos relevantes en el índice FAISS
    relevant_articles = search_vector_db(query_embedding, top_k=3)
    if not relevant_articles:
        raise HTTPException(status_code=404, detail="No se encontraron artículos relevantes.")
    
    # 3. Construir el prompt combinando la pregunta y los artículos recuperados
    prompt = f"Pregunta: {query.question}\n\nDocumentos relevantes:\n"
    for article in relevant_articles:
        prompt += (
            f"- {article['title']} (DOI: {article['doi']})\n"
            f"  Abstract: {article['abstract']}\n\n"
        )
    
    # 4. Llamar a Ollama para generar la respuesta
    response_text = generate_response(prompt)
    
    # 5. Registrar la consulta y la respuesta en Supabase
    log_query_response(query.question, response_text, relevant_articles)
    
    return {"response": response_text, "references": [article['doi'] for article in relevant_articles]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
