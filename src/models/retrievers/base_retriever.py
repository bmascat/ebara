from abc import ABC, abstractmethod
from typing import List

class BaseRetriever(ABC):
    """
    Clase abstracta base para los retrievers de bases de datos científicas.
    Define la interfaz común que todos los retrievers deben implementar.
    """

    def __init__(self, max_results: int = 20):
        self.max_results = max_results

    @abstractmethod
    def fetch_articles(self, query: str) -> List[str]:
        """
        Método abstracto para obtener artículos de una base de datos.
        
        Args:
            query (str): Query de búsqueda
            
        Returns:
            List[str]: Lista de abstracts de los artículos encontrados
        """
        pass
