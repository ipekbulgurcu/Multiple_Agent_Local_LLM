import os
import shutil
from typing import List
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from app.core.config import settings
from app.core.logging import logger

class VectorStoreService:
    """
    Service for interacting with the Vector Database (ChromaDB).
    """
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        # Ensure the directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            logger.info(f"VectorStore initialized at {self.persist_directory}")
        except Exception as e:
            logger.error(f"Failed to initialize VectorStore: {e}")
            raise e

    def add_documents(self, documents: List[Document]):
        """
        Adds a list of documents to the vector store.
        """
        try:
            if not documents:
                logger.warning("No documents to add.")
                return
                
            self.vector_db.add_documents(documents=documents)
            # self.vector_db.persist() # Chroma 0.4+ persists automatically or needs handling differently depending on version
            logger.info(f"Added {len(documents)} documents to vector store.")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise e

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Performs a similarity search for the given query.
        """
        try:
            results = self.vector_db.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            raise e
            
    def clear_db(self):
        """
        Clears the vector database.
        """
        try:
           self.vector_db.delete_collection()
           logger.info("Vector database cleared.")
        except Exception as e:
            logger.error(f"Error clearing vector DB: {e}")
