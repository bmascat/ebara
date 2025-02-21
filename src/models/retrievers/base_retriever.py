from abc import ABC, abstractmethod
from typing import List

class BaseRetriever(ABC):
    """
    Base abstract class for scientific databases retrievers.
    Defines the common interface that all retrievers must implement.
    """

    def __init__(self, max_results: int = 20):
        self.max_results = max_results

    @abstractmethod
    def fetch_articles(self, query: str) -> List[str]:
        """
        Abstract method to obtain articles from a database.
        
        Args:
            query (str): Search query
            
        Returns:
            List[str]: List of abstracts of the found articles
        """
        pass
