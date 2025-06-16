import ollama
import os
from .LLMConnector import LLMConnector

class OllamaConnector(LLMConnector):
    """Local connector for models via Ollama"""
    
    def __init__(self, model_name: str = "llama3.2"):
        self.model = model_name
        # Detectar si estamos en Docker o en desarrollo local
        is_docker = os.getenv('DOCKER_ENV', 'false').lower() == 'true'
        
        if is_docker:
            # En Docker, usar host.docker.internal
            ollama_host = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
        else:
            # En desarrollo local, usar localhost
            ollama_host = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
            
        ollama.set_host(ollama_host)
    
    def generate_text(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
        )
        return response['response']