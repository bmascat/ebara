import ollama
from .LLMConnector import LLMConnector

class OllamaConnector(LLMConnector):
    """Conector para modelos locales via Ollama"""
    
    def __init__(self, model_name: str = "deepseek-R1"):
        self.model = model_name
    
    def generate_text(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
        )
        return response['response']