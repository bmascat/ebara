import pytest
from unittest.mock import patch, MagicMock
from models.retrievers import PubMedRetriever

@pytest.fixture
def pubmed_retriever():
    return PubMedRetriever(max_results=2)

def test_init(pubmed_retriever):
    assert pubmed_retriever.max_results == 2
    assert pubmed_retriever.pubmed is not None

@patch('pymed.PubMed.query')
def test_fetch_articles_success(mock_query, pubmed_retriever):
    # Preparar los datos mock
    article1 = MagicMock()
    article1.doi = "10.1000/xyz123"
    article1.title = "Test title 1"
    article1.abstract = "Test abstract 1"
    
    article2 = MagicMock()
    article2.doi = "10.1000/xyz456"
    article2.title = "Test title 2"
    article2.abstract = "Test abstract 2"
    
    mock_query.return_value = [article1, article2]
    
    # Ejecutar
    results = pubmed_retriever.fetch_articles("test query")
    
    # Verificar
    assert len(results) == 2
    assert results[0] == {'doi': "10.1000/xyz123", 'title': "Test title 1", 'abstract': "Test abstract 1"}
    assert results[1] == {'doi': "10.1000/xyz456", 'title': "Test title 2", 'abstract': "Test abstract 2"}
    mock_query.assert_called_once_with("test query", max_results=2)

@patch('pymed.PubMed.query')
def test_fetch_articles_no_abstract(mock_query, pubmed_retriever):
    # Preparar artículo sin abstract
    article = MagicMock()
    article.doi = "10.1000/xyz789"
    article.title = "Test title"
    article.abstract = None
    mock_query.return_value = [article]
    
    # Ejecutar
    results = pubmed_retriever.fetch_articles("test query")
    
    # Verificar
    assert len(results) == 0
    mock_query.assert_called_once()

@patch('pymed.PubMed.query')
def test_fetch_articles_empty_result(mock_query, pubmed_retriever):
    mock_query.return_value = []
    results = pubmed_retriever.fetch_articles("test query")
    assert len(results) == 0
    mock_query.assert_called_once()

@pytest.mark.integration
# @pytest.mark.skip(reason="Solo ejecutar cuando se necesite probar la integración real")
def test_real_pubmed_api_call():
    # Inicializar el retriever
    retriever = PubMedRetriever(max_results=3)
    
    # Realizar una búsqueda real
    query = '"diabetes mellitus"[Title] AND "2024"[Date - Publication]'
    results = retriever.fetch_articles(query)
    
    # Verificaciones
    assert len(results) > 0
    assert all(isinstance(result['abstract'], str) for result in results)
    assert all(len(result['abstract']) > 0 for result in results)
    
    # First result for manual inspection
    print(f"\nFirst article found:\n{results[0]}...")
