from .LLMConnector import LLMConnector
from .HuggingFaceConnector import HuggingFaceConnector
from .OllamaConnector import OllamaConnector
from .OpenAIConnector import OpenAIConnector

class LLMConnectorFactory:
    """LLM Connector Factory"""
    
    @staticmethod
    def get_connector(connector_type: str, **kwargs) -> LLMConnector:
        """
        Creates and returns an instance of the specified connector
        
        Args:
            connector_type: Connector type ("huggingface", "ollama", "openai")
            **kwargs: Specific arguments for the connector
        
        Returns:
            LLMConnector: Instance of the requested connector
        """
        connectors = {
            "huggingface": HuggingFaceConnector,
            "ollama": OllamaConnector,
            "openai": OpenAIConnector
        }
        
        if connector_type not in connectors:
            raise ValueError(f"Unsupported connector. Valid options: {list(connectors.keys())}")
            
        return connectors[connector_type](**kwargs)