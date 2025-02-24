from models import ModelManager, EmbeddingProcessor, DatabaseManager
from models.retrievers import PubMedRetriever

def main():
    # Initialize components
    model_manager = ModelManager(connector_type="ollama", model_name="llama3.2",)
    pubmed_retriever = PubMedRetriever()
    embedding_processor = EmbeddingProcessor()
    db_manager = DatabaseManager()
    
    print("===  Literature Review Assistant (LRA) ===")
    print("(Write 'exit' to finish)")
    
    while True:
        # Get user question
        question = input("\nIntroduce your question about literature:\n> ")
        
        if question.lower() == 'exit':
            print("\n¡Goodbye!")
            break
            
        try:
            print("\nSearching for information...")
            
            # Generate optimized query for PubMed
            pubmed_query = model_manager.generate_advanced_query(question)
            
            print(f"Optimized query: {pubmed_query}")

            # Get articles from PubMed
            articles = pubmed_retriever.fetch_articles(pubmed_query)
            
            print(f"Articles found: {len(articles)}")

            if not articles:
                print("No articles found.")
                continue
            
            # Process articles
            embedding_processor.process_abstracts(articles)
            
            print("Processing articles...")
            
            # Get relevant documents
            relevant_docs = embedding_processor.retrieve_relevant_docs(question)
            
            print(f"Relevant documents found: {len(relevant_docs)}")            
            
            if not relevant_docs:
                print("No articles found.")
                continue
            
            # Create context
            # Convert context list to a structured JSON format
            context = model_manager.structure_context(relevant_docs)

            print("Generating response...")
            
            # Generate response
            response = model_manager.generate_response(question, context)
            
            print("Showing results...")

            # Show results
            print("\nResponse:")
            print(response)

            print("Saving to database...")
            
            # Save to database
            db_manager.save_to_db(question, response, context)            
                
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
