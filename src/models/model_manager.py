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
                    User question: "What is the recommended dosage of ibuprofen for adult patients, and what are its common side effects?"
                    Query: ("Ibuprofen"[Title/Abstract] OR "Ibuprofen"[MeSH]) AND ("Dosage"[Title/Abstract] OR "Administration & Dosage"[MeSH]) 
                    AND ("Side Effects"[Title/Abstract] OR "Adverse Effects"[MeSH] OR "Toxicity"[MeSH]) 
                    AND ("Adult"[MeSH] OR "Adults"[Title/Abstract])

                    Example 2:
                    User question: "Is metformin effective in reducing cardiovascular risk in patients with type 2 diabetes?"
                    Query: ("Metformin"[Title/Abstract] OR "Metformin"[MeSH]) 
                    AND ("Cardiovascular Diseases"[MeSH] OR "Cardiovascular Risk"[Title/Abstract]) 
                    AND ("Type 2 Diabetes Mellitus"[MeSH] OR "T2DM"[Title/Abstract]) 
                    AND ("Effectiveness"[Title/Abstract] OR "Efficacy"[Title/Abstract] OR "Clinical Trials as Topic"[MeSH])

                    Example 3:
                    User question: "What are the latest diagnostic criteria for Marfan syndrome?"
                    Query: ("Marfan Syndrome"[MeSH] OR "Marfan Syndrome"[Title/Abstract]) 
                    AND ("Diagnosis"[MeSH] OR "Diagnostic Criteria"[Title/Abstract]) 
                    AND ("Guidelines as Topic"[MeSH] OR "Consensus"[Title/Abstract]) 
                    AND ("2023"[PDAT] OR "2024"[PDAT])

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
        - Answer in English in a clear and understandable manner.
        - Use only the information provided in the context.
        - Use all the references provided in the context to answer the question.
        - Include citations in the text indicating from which abstract the information was taken.
        - If an abstract is cited multiple times, use the same reference number for each citation.
        - At the end of the response, provide a bibliography with the titles of the abstracts used in the same order as they appear in the context.
        - Titles are in the provided information JSON with the key "title".
        - Do not invent information or references.
        """
        
        return self.llm.generate_text(final_prompt)