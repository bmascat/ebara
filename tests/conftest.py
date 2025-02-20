import pytest
import sys
import os

# add the root directory of the project to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Shared fixtures for all tests
@pytest.fixture
def sample_abstract():
    return "This is a test abstract for medical research."

@pytest.fixture
def mock_response():
    class MockResponse:
        def __init__(self, json_data):
            self._json_data = json_data
        
        def json(self):
            return self._json_data
            
    return MockResponse
