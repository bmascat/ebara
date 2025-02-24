import pytest
import os
from src.models.connectors import OpenAIConnector
from unittest.mock import patch, MagicMock

@pytest.fixture
def openai_connector():
    api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAIConnector(api_key=api_key)

@pytest.mark.integration
def test_generate_text_integration(openai_connector):
    prompt = "What is the capital of France?"
    result = openai_connector.generate_text(prompt)
    
    assert isinstance(result, str)
    assert "Paris" in result

@pytest.mark.integration
def test_generate_text_integration_long_prompt(openai_connector):
    prompt = """Explain the process of photosynthesis including 
               the main chemical reactions and factors that affect it"""
    result = openai_connector.generate_text(prompt)
    
    assert isinstance(result, str)
    assert len(result) > 100
    assert "chlorophyll" in result.lower() or "CO2" in result

@pytest.mark.integration
def test_generate_text_integration_technical(openai_connector):
    prompt = "Explain quantum computing and qubits"
    result = openai_connector.generate_text(prompt)
    
    assert isinstance(result, str)
    assert "qubit" in result.lower() or "quantum" in result.lower()
    assert len(result) > 50
