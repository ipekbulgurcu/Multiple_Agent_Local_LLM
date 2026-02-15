from functools import lru_cache
from app.services.llm_service import LLMService
from app.services.vector_store_service import VectorStoreService
from app.services.ingestion_service import IngestionService

@lru_cache()
def get_llm_service() -> LLMService:
    """Returns a singleton instance of LLMService."""
    return LLMService()

@lru_cache()
def get_vector_store_service() -> VectorStoreService:
    """Returns a singleton instance of VectorStoreService."""
    return VectorStoreService()

@lru_cache()
def get_ingestion_service() -> IngestionService:
    """Returns a singleton instance of IngestionService."""
    return IngestionService()
