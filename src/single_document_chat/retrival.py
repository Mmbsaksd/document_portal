import sys
import os
import streamlit as st
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

class ConversationalRAG:
    def __init__(self, session_id: str, retriever)->None:
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.retriever = retriever
            self.llm = self._load_llm
            self.contextualize_prompt = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            self.history_aware_retriever = create_history_aware_history(
                self.llm, self.retriever, self.contextualize_prompt
            )
            self.log.info("Created history-aware-retriever", session_id=session_id)
            self.qa_chain = create_stuff_documents_chain(self.llm, self.qa_prompt)
            self.rag_chain = create_retrival_chain(self.history_aware_retriever, self.qa_chain)
            self.logo.info("Initialized ConversationalRAG", session_id=session_id)

            self.chain = RunnableWithMessageHistory(
                self.rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )




        except Exception as e:
            self.log.error("Error initializing ConversionalRAG", error=str(e), session_id = session_id)
            raise DocumentPortalExeption("Failed to initialize ConversionalRAG", sys)
        
    def _load_llm(self):
        try:
            llm = Model_loader().load_llm
            self.log.info("LLM loaded successfully", class_name = llm.__class__.__name__)
            return llm
        
        except Exception as e:
            self.log.error("Error loading LLM via ModelLoader", error = str(e))
            raise DocumentPortalExeption("Failed to load LLM", sys)
        
    def _get_session_history(self, session_id:str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to access session history.", session_id = session_id, error=str(e))
            raise DocumentPortalExeption("Failed to retrive session history", sys)
        
        
    def load_retriver_from_faiss(self, index_path:str):
        try:
            self.log = CustomLogger().get_logger(__name__)
            embeddings = Model_loader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            vectorstore = FAISS.load_local(index_path, embeddings)
            self.log.info("Loaded retriever from FAISS index", index_path = index_path)
            return vectorstore.as_retriever(search_tyoe="similarity", search_kwargs={"k":5})
        
        except Exception as e:
            self.log.error("Failed to load retriver from FAISS", error=str(e))
            raise DocumentPortalExeption("Error loading retrival from FAISS", sys)
        
    def invoke(self, user_input):
        try:
            response = self.chain.invoke(
                {"input":user_input},
                config={"configurable":{"session_id":self.session_id}}
            )
            answer = response.get("answer","No answer")
            if not answer:
                self.log.warning("Empty answer received", session_id = self.session_id)

            self.log.info("Chain invoked successfully", session_id = self.session_id, user_input = user_input, answer_preview = answer[:150])
            return answer
        
        except Exception as e:
            self.log.error("Failed to invoke conversational RAG", error = str(e), session_id = self.session_id)
            raise DocumentPortalExeption("Failed to invoke RAG chain", sys)
        