from langchain_ollama import ChatOllama
from app.core.config import settings

def get_fast_llm() -> ChatOllama:
    """
    Returns the 'Fast' LLM (e.g., phi3, gemma) for routing and simple tasks.
    """
    return ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=settings.FAST_LLM_MODEL,
        temperature=0
    )

def get_smart_llm(model_name: str = None) -> ChatOllama:
    """
    Returns the 'Smart' LLM (e.g., llama3, mistral) for complex reasoning and coding.
    If model_name is provided, it attempts to use that model.
    """
    return ChatOllama(
        base_url=settings.OLLAMA_BASE_URL,
        model=model_name if model_name else settings.SMART_LLM_MODEL,
        temperature=0
    )
