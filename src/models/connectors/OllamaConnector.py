import ollama
from connectors import LLMConnector

class OllamaConnector(LLMConnector):
    """Conector para modelos locales via Ollama"""
    
    def __init__(self, model_name: str = "llama2"):
        self.model = model_name
    
    def generate_text(self, prompt: str, max_length: int = 300) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            max_tokens=max_length
        )
        return response['response']