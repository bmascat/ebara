from .LLMConnector import LLMConnector
from .HuggingFaceConnector import HuggingFaceConnector
from .OllamaConnector import OllamaConnector
from .OpenAIConnector import OpenAIConnector

class LLMConnectorFactory:
    """Fábrica de conectores LLM"""
    
    @staticmethod
    def get_connector(connector_type: str, model_name: str, **kwargs) -> LLMConnector:
        """
        Crea y retorna una instancia del conector especificado
        
        Args:
            connector_type: Tipo de conector ("huggingface", "ollama", "openai")
            **kwargs: Argumentos específicos para el conector
        
        Returns:
            LLMConnector: Instancia del conector solicitado
        """
        connectors = {
            "huggingface": HuggingFaceConnector,
            "ollama": OllamaConnector,
            "openai": OpenAIConnector
        }
        
        if connector_type not in connectors:
            raise ValueError(f"Conector no soportado. Opciones válidas: {list(connectors.keys())}")
            
        return connectors[connector_type](model_name, **kwargs)