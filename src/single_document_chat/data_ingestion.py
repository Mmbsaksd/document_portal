import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption
from utils.model_loader import Model_loader

class SingleDocIngestor:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
            
        except Exception as e:
            self.log.error(f"Error initializing SingleDocIngestor: {e}")
            raise DocumentPortalExeption("Error initializing SingleDocIngestor", sys)
        
    def _create_retriver(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create retriver", error = str(e))
            raise DocumentPortalExeption("Error during retriver creation", sys)
        