# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.models import ModelManager, EmbeddingProcessor, PubMedRetriever, DatabaseManager
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500, description="La pregunta debe tener entre 5 y 500 caracteres")

@app.post("/query")
async def handle_query(query: QueryRequest):
    try:
        # Calcular embedding en un thread separado
        # Inicializar los componentes necesarios
        model_manager = ModelManager(connector_type="ollama", model_name="deepseek-R1")
        embedding_processor = EmbeddingProcessor()
        pubmed_retriever = PubMedRetriever()
        
        # Generar consulta optimizada para PubMed
        pubmed_query = await run_in_threadpool(model_manager.generate_advanced_query, query.question)
        
        # Obtener artículos de PubMed
        articles = await run_in_threadpool(pubmed_retriever.fetch_articles, pubmed_query)
        
        # Procesar los artículos con el embedding processor
        await run_in_threadpool(embedding_processor.process_abstracts, articles)
        
        # Obtener chunks relevantes
        relevant_docs = await run_in_threadpool(
            embedding_processor.retrieve_relevant_docs, 
            query.question
        )
        
        if not relevant_docs:
            raise HTTPException(status_code=404, detail="No se encontraron artículos relevantes.")
        
        # Crear un contexto formateado con la información completa de cada artículo
        context = []
        for doc in relevant_docs:
            context.append(
                f"""- {doc['title']} (DOI: {doc['doi']})
                      Abstract: {doc['abstract']}"""
            )
        
        # Generar la respuesta utilizando el método del ModelManager
        # Se asume que generate_response recibe la pregunta y el contexto (lista de strings)
        response_text = await run_in_threadpool(model_manager.generate_response, query.question, context)
        
        # Registrar la consulta en la base de datos utilizando DatabaseManager
        db_manager = DatabaseManager()
        db_manager.create_table()

        await run_in_threadpool(db_manager.save_to_db, query.question, response_text, context)
    
        return {"response": response_text, "references": [doc['doi'] for doc in relevant_docs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
