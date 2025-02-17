from .connectors import LLMConnectorFactory

class ModelManager:
    """Gestor de modelos que soporta múltiples conectores de LLM"""
    
    def __init__(self, connector_type: str = "ollama", **kwargs):
        """
        Inicializa el ModelManager con el conector especificado
        
        Args:
            connector_type: String que indica el conector a usar ("huggingface", "ollama", "openai")
            **kwargs: Argumentos adicionales para el conector específico
        """
        self.llm = LLMConnectorFactory.get_connector(connector_type, **kwargs)
    
    def generate_advanced_query(self, user_question: str) -> str:
        """Convierte la pregunta del usuario en una consulta avanzada de PubMed."""
        prompt = f"""Convert the following user question into a GraphQL search query in english that can be used in an API call.
                    The output must be in plain text, without any formatting symbols like triple backticks, code blocks, or explanations.

                    Follow the format of the examples below:

                    Example 1:
                    User question: "Buscar artículos sobre cáncer de pulmón publicados después de 2020"
                    Query: ("2020/01/01"[Date - Create] : "3000"[Date - Create]) AND ("lung cancer"[Title])

                    Example 2:
                    User question: "Cómo los estudios sobre la enfermedad de Alzheimer de John Doe"
                    Query: ("John Doe"[Author]) AND ("Alzheimer's disease"[Title])

                    Example 3:
                    User question: "¿Cuáles son los últimos tratamientos para la diabetes?"
                    Query: ("diabetes"[Title]) AND ("treatment"[Title]) AND ("2023/01/01"[Date - Create] : "3000"[Date - Create])

                    Now, convert the following user question using the same format:

                    User question: "{user_question}"
                    Query:
                     """
        
        return self.llm.generate_text(prompt)

    def generate_response(self, query: str, context: list) -> str:
        """Genera una respuesta basada en los fragmentos recuperados."""
        final_prompt = f"""Using the following information: {context} 
                      together with the data you have from your previous training, answer the following question: {query}
                      Please answer the question in spanish and in a way that is easy to understand.
                      """
        return self.llm.generate_text(final_prompt)