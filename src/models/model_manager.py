from .connectors import LLMConnectorFactory

class ModelManager:
    """Model manager that supports multiple LLM connectors"""
    
    def __init__(self, connector_type: str = "ollama", **kwargs):
        """
        Initializes the ModelManager with the specified connector
        
        Args:
            connector_type: String indicating the connector to use ("huggingface", "ollama", "openai")
            **kwargs: Additional arguments for the specific connector
        """
        self.llm = LLMConnectorFactory.get_connector(connector_type, **kwargs)
    
    def generate_advanced_query(self, user_question: str) -> str:
        """Converts the user question into an advanced PubMed search query."""
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
    
    def structure_context(self, context: list) -> str:
        """Converts the context list to a structured JSON format."""
        return [{"title": item['title'], "abstract": item['abstract']} for item in context]

    def generate_response(self, query: str, context: list) -> str:
        """Generates a response based on the retrieved fragments."""
            
        structured_context = self.structure_context(context)
        
        final_prompt = f"""
        Using the following information, answer the question: {query}
        
        Provided information:
        {structured_context}
        
        Instructions:
        - Answer in Spanish in a clear and understandable manner.
        - Use only the information provided in the context.
        - Include citations in the text indicating from which abstract the information was taken.
        - At the end of the response, provide a bibliography with the titles of the abstracts used.
        - Do not invent information or references.
        """
        
        return self.llm.generate_text(final_prompt)