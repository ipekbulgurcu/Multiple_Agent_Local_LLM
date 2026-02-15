from pydantic import BaseModel
from typing import List, Optional

class HealthCheck(BaseModel):
    """Response model for health check."""
    status: str = "ok"

class IngestResponse(BaseModel):
    """Response model for document ingestion."""
    message: str
    filename: str
    chunks_count: int

class AskRequest(BaseModel):
    """Request model for asking a question."""
    query: str
    model: Optional[str] = None

class AskResponse(BaseModel):
    """Response model for the answer."""
    query: str
    answer: str
    source_documents: Optional[List[str]] = []
