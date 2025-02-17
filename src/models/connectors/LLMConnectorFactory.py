from connectors import LLMConnector, HuggingFaceConnector, OllamaConnector, LMStudioConnector

class LLMConnectorFactory:
    """Fábrica de conectores LLM"""
    
    @staticmethod
    def get_connector(connector_type: str, **kwargs) -> LLMConnector:
        """
        Crea y retorna una instancia del conector especificado
        
        Args:
            connector_type: Tipo de conector ("huggingface", "ollama", "lmstudio")
            **kwargs: Argumentos específicos para el conector
        
        Returns:
            LLMConnector: Instancia del conector solicitado
        """
        connectors = {
            "huggingface": HuggingFaceConnector,
            "ollama": OllamaConnector,
            "lmstudio": LMStudioConnector
        }
        
        if connector_type not in connectors:
            raise ValueError(f"Conector no soportado. Opciones válidas: {list(connectors.keys())}")
            
        return connectors[connector_type](**kwargs)