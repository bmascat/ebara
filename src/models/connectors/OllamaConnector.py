from ollama import Client
import os
from .LLMConnector import LLMConnector

class OllamaConnector(LLMConnector):
    """Local connector for models via Ollama"""
    
    def __init__(self, model_name: str = "llama3.2"):
        self.model = model_name
        # Configurar la URL base de Ollama usando la variable de entorno
        custom_host = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.client = Client(host=custom_host)

    def generate_text(self, prompt: str) -> str:
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
        )
        return response['response']