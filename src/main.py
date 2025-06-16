# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.models import ModelManager, EmbeddingProcessor, DatabaseManager
from src.models.retrievers import PubMedRetriever
import logging, os

app = FastAPI()

# Configurar el logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500, description="Question must be between 5 and 500 characters")

@app.post("/query")
async def handle_query(query: QueryRequest):
    try:
        logger.info("Starting query handling.")
        # api_key = os.environ.get("OPENAI_API_KEY")
        # Initialize the necessary components
        logger.info("Initializing ModelManager, EmbeddingProcessor and PubMedRetriever.")
        model_manager = ModelManager(connector_type="ollama", model_name="llama3.2")
        # model_manager = ModelManager(connector_type="openai", api_key=api_key, model="gpt-4o-mini")

        embedding_processor = EmbeddingProcessor()
        pubmed_retriever = PubMedRetriever()
        
        # Generate optimized query for PubMed
        logger.info(f"Question: {query.question}")
        logger.info("Generating optimized query for PubMed.")
        pubmed_query = model_manager.generate_advanced_query(query.question)
        logger.info(f"Optimized query: {pubmed_query}")

        # Fetch articles from PubMed
        logger.info("Fetching articles from PubMed.")
        articles = pubmed_retriever.fetch_articles(pubmed_query)
        
        if not articles:
            logger.warning("No articles found. Generating response without literature.")
            response_text = model_manager.generate_response(

                f"""No relevant articles found. 
                However, based on the general knowledge available, I will answer the following:
                
                {query.question}""", []
            )
            return {"response": response_text, "references": []}
        
        logger.info(f"Articles found: {len(articles)}")
        # Process the articles with the embedding processor
        logger.info("Processing articles with the EmbeddingProcessor.")
        embedding_processor.process_abstracts(articles)
        
        # Fetch relevant documents
        logger.info("Fetching relevant documents.")
        relevant_docs = embedding_processor.retrieve_relevant_docs(query.question)
    
        if not relevant_docs:
            logger.warning("No relevant documents found. Generating response without literature.")
            response_text = model_manager.generate_response(

                f"""No relevant documents found. 
                However, based on the general knowledge available, I will answer the following:
                
                {query.question}""", []
            )
            return {"response": response_text, "references": []}

        logger.info(f"Relevant documents found: {len(relevant_docs)}")

        # Create a formatted context with the complete information of each article
        logger.info("Creating formatted context.")
        context = model_manager.structure_context(relevant_docs)
        logger.info(f"Context: {context}")
        # Generate the response using the ModelManager method
        logger.info("Generating the response.")
        response_text = model_manager.generate_response(query.question, context)
        
        # Register the query in the database using DatabaseManager
        logger.info("Registering the query in the database.")
        db_manager = DatabaseManager()
        db_manager.create_table()
        db_manager.save_to_db(query.question, response_text, context)
    
        logger.info("Query handled successfully.")
        return {"response": response_text, "references": [doc['title'] for doc in relevant_docs]}
    
    except HTTPException as e:
        logger.error(f"Error handling the query: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error handling the query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
