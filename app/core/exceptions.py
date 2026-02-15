class BaseAppException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class InvalidFileTypeException(BaseAppException):
    """Raised when an unsupported file type is uploaded."""
    def __init__(self, message: str = "Invalid file type. Only PDF and TXT are supported."):
        super().__init__(message, status_code=400)

class LLMConnectionException(BaseAppException):
    """Raised when there is an error connecting to the LLM service."""
    def __init__(self, message: str = "Could not connect to LLM service."):
        super().__init__(message, status_code=503)

class EmptyQueryException(BaseAppException):
    """Raised when the query is empty."""
    def __init__(self, message: str = "Query cannot be empty."):
        super().__init__(message, status_code=400)
    
class DocumentIngestionException(BaseAppException):
    """Raised when document ingestion fails."""
    def __init__(self, message: str = "Failed to ingest document."):
        super().__init__(message, status_code=500)
