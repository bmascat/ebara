import pytest
from unittest.mock import patch, MagicMock
from src.models.connectors import OllamaConnector

@pytest.fixture
def ollama_connector():
    return OllamaConnector(model_name="test-model")

@patch('ollama.generate')
def test_generate_text_success(mock_generate, ollama_connector):
    # Configurar el mock para simular una respuesta exitosa
    mock_generate.return_value = {'response': 'Texto generado exitosamente'}

    # Ejecutar el método
    result = ollama_connector.generate_text("Test prompt")

    # Verificar el resultado
    assert result == 'Texto generado exitosamente'
    mock_generate.assert_called_once_with(model="test-model", prompt="Test prompt")

@patch('ollama.generate')
def test_generate_text_failure(mock_generate, ollama_connector):
    # Configurar el mock para simular una excepción
    mock_generate.side_effect = Exception("Error al generar texto")

    # Verificar que se maneja la excepción
    with pytest.raises(Exception, match="Error al generar texto"):
        ollama_connector.generate_text("Test prompt")
