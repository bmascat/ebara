from models import ModelManager, PubMedRetriever, EmbeddingProcessor, DatabaseManager

def main():
    # Inicializar componentes
    model_manager = ModelManager(connector_type="ollama", model_name="llama3.2",)
    pubmed_retriever = PubMedRetriever()
    embedding_processor = EmbeddingProcessor()
    db_manager = DatabaseManager()
    
    print("=== PubMed AI Research Assistant ===")
    print("(Escribe 'salir' para terminar)")
    
    while True:
        # Obtener pregunta del usuario
        question = input("\nIntroduce tu pregunta sobre enfermedades, tratamientos o fármacos:\n> ")
        
        if question.lower() == 'salir':
            print("\n¡Hasta luego!")
            break
            
        try:
            print("\nBuscando información...")
            
            # Generar consulta optimizada para PubMed
            pubmed_query = model_manager.generate_advanced_query(question)
            
            print(f"Consulta optimizada: {pubmed_query}")

            # Obtener artículos de PubMed
            articles = pubmed_retriever.fetch_articles(pubmed_query)
            
            print(f"Artículos encontrados: {len(articles)}")
            # Procesar los artículos
            embedding_processor.process_abstracts(articles)
            
            print("Procesando artículos...")
            
            # Obtener documentos relevantes
            relevant_docs = embedding_processor.retrieve_relevant_docs(question)
            
            print(f"Documentos relevantes encontrados: {len(relevant_docs)}")
            
            if not relevant_docs:
                print("No se encontraron artículos relevantes.")
                continue
            
            # Crear contexto
            context = []
            for doc in relevant_docs:
                context.append(
                    f"- {doc['title']} (DOI: {doc['doi']})\n  Abstract: {doc['abstract']}"
                )
            
            print("Generando respuesta...")
            
            # Generar respuesta
            response = model_manager.generate_response(question, context)
            
            print("Guardando en base de datos...")
            
            # Guardar en base de datos
            db_manager.save_to_db(question, response, context)
            
            print("Mostrando resultados...")
            
            # Mostrar resultados
            print("\nRespuesta:")
            print(response)
            print("\nFuentes:")
            for doc in relevant_docs:
                print(f"- DOI: {doc['doi']}")
                
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
