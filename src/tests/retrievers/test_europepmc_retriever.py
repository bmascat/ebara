import pytest
import requests
from unittest.mock import patch, MagicMock
from models.retrievers import EuropePMCRetriever

@pytest.fixture
def europepmc_retriever():
    return EuropePMCRetriever(max_results=2)

def test_init(europepmc_retriever):
    assert europepmc_retriever.max_results == 2
    assert europepmc_retriever.BASE_URL == "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

@patch('requests.get')
def test_fetch_articles_success(mock_get, europepmc_retriever):
    # Preparar respuesta mock
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'resultList': {
            'result': [
                {'abstractText': 'Test abstract 1'},
                {'abstractText': 'Test abstract 2'}
            ]
        }
    }
    mock_get.return_value = mock_response
    
    # Ejecutar
    results = europepmc_retriever.fetch_articles("test query")
    
    # Verificar
    assert len(results) == 2
    assert results[0] == "Test abstract 1"
    assert results[1] == "Test abstract 2"
    
    # Verificar llamada a la API
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == europepmc_retriever.BASE_URL
    assert kwargs['params']['query'] == "test query"
    assert kwargs['params']['pageSize'] == 2

@patch('requests.get')
def test_fetch_articles_api_error(mock_get, europepmc_retriever):
    # Simular error de API
    mock_get.side_effect = requests.exceptions.RequestException("API Error")
    
    # Verificar que se maneja la excepción
    with pytest.raises(requests.exceptions.RequestException):
        europepmc_retriever.fetch_articles("test query")

@patch('requests.get')
def test_fetch_articles_missing_abstract(mock_get, europepmc_retriever):
    # Preparar respuesta con artículo sin abstract
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'resultList': {
            'result': [
                {'title': 'Test title'},  # Sin abstractText
                {'abstractText': 'Test abstract 2'}
            ]
        }
    }
    mock_get.return_value = mock_response
    
    # Ejecutar
    results = europepmc_retriever.fetch_articles("test query")
    
    # Verificar
    assert len(results) == 1
    assert results[0] == "Test abstract 2"
