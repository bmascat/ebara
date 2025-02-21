from models import ModelManager, EmbeddingProcessor, DatabaseManager
from models.retrievers import PubMedRetriever

def main():
    # Inicializar componentes
    model_manager = ModelManager(connector_type="ollama", model_name="llama3.2",)
    pubmed_retriever = PubMedRetriever()
    embedding_processor = EmbeddingProcessor()
    db_manager = DatabaseManager()
    
    print("===  Literature Review Assistant (LRA) ===")
    print("(Write 'exit' to finish)")
    
    while True:
        # Obtener pregunta del usuario
        question = input("\nIntroduce your question about literature:\n> ")
        
        if question.lower() == 'exit':
            print("\n¡Goodbye!")
            break
            
        try:
            print("\nSearching for information...")
            
            # Generar consulta optimizada para PubMed
            pubmed_query = model_manager.generate_advanced_query(question)
            
            print(f"Optimized query: {pubmed_query}")

            # Obtener artículos de PubMed
            articles = pubmed_retriever.fetch_articles(pubmed_query)
            
            print(f"Articles found: {len(articles)}")
            # Procesar los artículos
            embedding_processor.process_abstracts(articles)
            
            print("Processing articles...")
            
            # Obtener documentos relevantes
            relevant_docs = embedding_processor.retrieve_relevant_docs(question)
            
            print(f"Relevant documents found: {len(relevant_docs)}")
            print(relevant_docs)
            
            if not relevant_docs:
                print("No articles found.")
                continue
            
            # Crear contexto
            context = []
            for doc in relevant_docs:
                context.append(
                    f"- {doc['title']}\n  Abstract: {doc['abstract']}"
                )
            print("Generating response...")
            
            # Generar respuesta
            response = model_manager.generate_response(question, context)
            
            print("Showing results...")

            # Mostrar resultados
            print("\nResponse:")
            print(response)
            print("\nSources:")

            for doc in relevant_docs:
                print(f"- {doc['title']}\n")

            print("Saving to database...")
            
            # Guardar en base de datos
            db_manager.save_to_db(question, response, context)            
                
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
