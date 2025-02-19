import requests
from typing import List
from .base_retriever import BaseRetriever

class EuropePMCRetriever(BaseRetriever):
    """
    Retriever para la base de datos Europe PMC.
    Utiliza la API REST de Europe PMC.
    """

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def __init__(self, max_results: int = 20):
        super().__init__(max_results)

    def fetch_articles(self, query: str) -> List[str]:
        """
        Obtiene los primeros 'max_results' artículos de Europe PMC según la consulta.
        
        Args:
            query (str): Query de búsqueda
            
        Returns:
            List[str]: Lista de abstracts de los artículos
        """
        params = {
            'query': query,
            'format': 'json',
            'pageSize': self.max_results
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        titles = [] 
        
        for result in data.get('resultList', {}).get('result', []):
            if 'title' in result:
                titles.append(result['title'])
                
        return titles
