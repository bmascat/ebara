from abc import ABC, abstractmethod

class LLMConnector(ABC):
    """Clase base abstracta para conectores de LLM"""
    
    @abstractmethod
    def generate_text(self, prompt: str, max_length: int = 300) -> str:

        """Método abstracto para generar texto"""
        pass