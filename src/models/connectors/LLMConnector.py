from abc import ABC, abstractmethod

class LLMConnector(ABC):
    """Base abstract class for LLM connectors"""
    
    @abstractmethod
    def generate_text(self, prompt: str, max_length: int = 300) -> str:

        """Abstract method to generate text"""
        pass