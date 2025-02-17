from connectors import LLMConnectorFactory

class ModelManager:
    """Gestor de modelos que soporta múltiples conectores de LLM"""
    
    def __init__(self, connector_type: str = "ollama", **kwargs):
        """
        Inicializa el ModelManager con el conector especificado
        
        Args:
            connector_type: String que indica el conector a usar ("huggingface", "ollama", "lmstudio")
            **kwargs: Argumentos adicionales para el conector específico
        """
        self.llm = LLMConnectorFactory.get_connector(connector_type, **kwargs)
    
    def generate_advanced_query(self, user_question: str) -> str:
        """Convierte la pregunta del usuario en una consulta avanzada de PubMed."""
        prompt = f"""Convert the following question into an advanced PubMed search query in graphQL and in english: {user_question}"""
        return self.llm.generate_text(prompt, max_length=100)

    def generate_response(self, query: str, context: list) -> str:
        """Genera una respuesta basada en los fragmentos recuperados."""
        final_prompt = f"""Using the following information: {context} 
                      together with the data you have from your previous training, answer the following question: {query}
                      Please answer the question in spanish and in a way that is easy to understand.
                      """
        return self.llm.generate_text(final_prompt, max_length=300)