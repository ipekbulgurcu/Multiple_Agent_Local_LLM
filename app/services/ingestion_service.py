import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import InvalidFileTypeException, DocumentIngestionException

class IngestionService:
    """
    Service for loading and splitting documents.
    """
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )

    async def process_file(self, file_path: str) -> List[Document]:
        """
        Loads a file and splits it into chunks.
        """
        if not os.path.exists(file_path):
            raise DocumentIngestionException(f"File not found: {file_path}")

        filename = os.path.basename(file_path)
        logger.info(f"Processing file: {filename}")

        try:
            if filename.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif filename.lower().endswith(".txt"):
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
            else:
                raise InvalidFileTypeException(f"Unsupported file type: {filename}")
            
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {filename} into {len(chunks)} chunks.")
            return chunks
            
        except InvalidFileTypeException as e:
            raise e
        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            raise DocumentIngestionException(f"Error processing file: {str(e)}")
