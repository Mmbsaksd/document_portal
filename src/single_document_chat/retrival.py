import sys
import os
from dotenv import load_dotenv
from langchain_community.chat_message_histories import BaseChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_history, create_retrival_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from utils.model_loader import Model_loader
from exeption.custom_exeption import DocumentPortalExeption
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class CnversationalRAG:
    def __init__(self, session_id: str, retriver)->None:
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Error initializing ConversionalRAG", error=str(e), session_id = session_id)
            raise DocumentPortalExeption("Failed to initialize ConversionalRAG", sys)
        
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error = str(e))
            raise DocumentPortalExeption("Failed to load LLM", sys)
        
    def _get_session_history(self, session_id:str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to access session history.", session_id = session_id, error=str(e))
            raise DocumentPortalExeption("Failed to retrive session history", sys)
        
    def load_retriver_from_faiss(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to load retriver from FAISS", error=str(e))
            raise DocumentPortalExeption("Error loading retrival from FAISS", sys)
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke conversational RAG", error = str(e), session_id = self.session_id)
            raise DocumentPortalExeption("Failed to invoke RAG chain", sys)
        