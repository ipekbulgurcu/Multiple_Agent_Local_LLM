import pytest
from unittest.mock import MagicMock
from app.api.dependencies import get_llm_service, get_vector_store_service, get_ingestion_service
from app.core.exceptions import InvalidFileTypeException
from app.main import app
from langchain_core.documents import Document

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_ingest_endpoint(client, mock_ingestion_service, mock_vector_store_service):
    """Test the /ingest endpoint with mocked services."""
    
    # Override dependencies
    app.dependency_overrides[get_ingestion_service] = lambda: mock_ingestion_service
    app.dependency_overrides[get_vector_store_service] = lambda: mock_vector_store_service
    
    # Mock return values
    mock_ingestion_service.process_file.return_value = [
        Document(page_content="Chunk 1", metadata={"source": "test.txt"}),
        Document(page_content="Chunk 2", metadata={"source": "test.txt"})
    ]

    # Create dummy file
    files = {'file': ('test.txt', b'This is a test file content.', 'text/plain')}
    
    response = client.post("/ingest", files=files)
    
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == "Document ingested successfully."
    assert json_response["chunks_count"] == 2
    
    # Verify mocks were called
    mock_ingestion_service.process_file.assert_called_once()
    mock_vector_store_service.add_documents.assert_called_once()
    
    # Cleanup overrides
    app.dependency_overrides = {}

def test_ask_endpoint(client, mock_llm_service, mock_vector_store_service):
    """Test the /ask endpoint with mocked services."""
    
    # Override dependencies
    app.dependency_overrides[get_llm_service] = lambda: mock_llm_service
    app.dependency_overrides[get_vector_store_service] = lambda: mock_vector_store_service
    
    # Mock return values
    mock_vector_store_service.similarity_search.return_value = [
        Document(page_content="Relevant context.", metadata={"source": "doc1.pdf"})
    ]
    mock_llm_service.generate_response.return_value = "The answer is 42."
    
    payload = {"query": "What is the answer?"}
    
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["query"] == "What is the answer?"
    assert json_response["answer"] == "The answer is 42."
    assert "doc1.pdf" in json_response["source_documents"]

    # Verify mocks were called
    mock_vector_store_service.similarity_search.assert_called_once()
    mock_llm_service.generate_response.assert_called_once()
    
    # Cleanup overrides
    app.dependency_overrides = {}

def test_ask_endpoint_empty_query(client):
    """Test /ask with empty query."""
    response = client.post("/ask", json={"query": "   "})
    assert response.status_code == 400
