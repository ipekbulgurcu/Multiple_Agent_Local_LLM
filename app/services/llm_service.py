from langchain_ollama import OllamaLLM
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import LLMConnectionException

class LLMService:
    """
    Service for interacting with the Ollama LLM.
    """
    def __init__(self):
        try:
            self.llm = OllamaLLM(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.LLM_MODEL
            )
            logger.info(f"LLM Service initialized with model: {settings.LLM_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM Service: {e}")
            raise LLMConnectionException(f"Failed to connect to Ollama: {str(e)}")

    def generate_response(self, query: str, context: str) -> str:
        """
        Generates a response from the LLM based on the query and context.
        """
        if not query:
            return ""
            
        prompt = f"""
        You are a helpful assistant. Use the following context to answer the question.
        If the answer is not in the context, say you don't know.
        
        Context:
        {context}
        
        Question:
        {query}
        
        Answer:
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise LLMConnectionException(f"Error during LLM generation: {str(e)}")
