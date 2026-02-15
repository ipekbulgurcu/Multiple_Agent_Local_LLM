from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain_core.tools import Tool
from app.services.vector_store_service import VectorStoreService
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

def get_web_search_tool() -> Tool:
    """
    Returns the DuckDuckGo search tool.
    """
    def search_func(query: str) -> str:
        if not DDGS:
            return "Error: duckduckgo-search package is not installed."
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "No results found."
                return "\n\n".join([f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}" for r in results])
        except Exception as e:
            return f"Search error: {e}"

    return Tool(
        name="web_search",
        description="A search engine. Use this to answer questions about current events or when you need to find information on the internet.",
        func=search_func
    )

def get_python_repl_tool() -> Tool:
    """
    Returns the Python REPL tool for executing python code.
    Useful for complex calculations or data analysis.
    """
    return PythonREPLTool()

def rag_tool_wrapper(query: str) -> str:
    # Initialize the service (ensure singleton behavior if needed, or lightweight init)
    vector_service = VectorStoreService()
    docs = vector_service.similarity_search(query)
    
    # Format results with sources
    formatted_docs = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        formatted_docs.append(f"Content: {doc.page_content}\nSource: {source}")
        
    return "\n\n---\n\n".join(formatted_docs)

def get_rag_tool() -> Tool:
    """
    Returns the RAG tool for querying the local vector database.
    Useful for answering questions about the uploaded documents.
    """
    return Tool(
        name="rag_tool",
        description="Search tool for internal documents. Use this to query the knowledge base/vector store.",
        func=rag_tool_wrapper
    )
