import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.api.dependencies import get_llm_service, get_vector_store_service, get_ingestion_service

@pytest.fixture
def client():
    """Returns a TestClient instance."""
    return TestClient(app)

@pytest.fixture
def mock_llm_service():
    """Returns a mock LLMService."""
    mock = MagicMock()
    mock.generate_response.return_value = "This is a mocked response."
    return mock

@pytest.fixture
def mock_vector_store_service():
    """Returns a mock VectorStoreService."""
    mock = MagicMock()
    mock.similarity_search.return_value = []
    return mock

@pytest.fixture
def mock_ingestion_service():
    """Returns a mock IngestionService."""
    mock = MagicMock()
    mock.process_file.return_value = []
    return mock
