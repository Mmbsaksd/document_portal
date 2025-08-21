import sys
import os
from operator import itemgetter
from typing import List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage

from utils.model_loader import Model_loader
from exeption.custom_exeption import DocumentPortalExeption
from logger.custom_logger import CustomLogger
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType



class ConversationalRAG:
    def __init__(self, session_id, retriever=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.session_id = session_id
            self.llm = self._load_llm()
            self.contextualize_prompt:ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt: ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            if retriever is None:
                raise ValueError("Retriever cannot ne None")
            self.retriever = retriever
            self._build_lcel_chain()
            self.log.info("ConversationalRAG initialized", session_id = self.session_id)
        except Exception as e:
            self.log.error("Failed to initialize ConversationalRAG", error = str(e))
            raise DocumentPortalExeption("Initialize error in ConversationalRAG", sys)

    def load_retriever_from_faiss(self, index_path):
        try:
            embeddings = Model_loader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError(f"FAISS index directory not found: {index_path}")
            vectorstore = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )

            self.retriever = vectorstore.as_retriever(search_type = "similarity", search_kwargs = {"k":5})
            self.log.info("FAISS retriver loaded successfully", index_path=index_path, session_id = self.session_id)

            return self.retriever


        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", error = str(e))
            raise DocumentPortalExeption("Loading error in conversationalRAG", sys)

    def invoke(self, user_input:str,chat_history:Optional[List[BaseMessage]]=None):
        try:
            chat_history = chat_history or []
            payload = {"input":user_input, "chat_history":chat_history}
            answer = self.chain.invoke(payload)
            if not answer:
                self.log.warning("No answer generated", input = user_input, session_id = self.session_id)
                return "No answer generated"
            self.log.info("Chain invoked successfully",
                          session_id = self.session_id,
                          user_input = user_input,
                          answer_preview = answer[:150])
            return answer

        except Exception as e:
            self.log.error("Failed to invoke ConversationalRAG", error = str(e))
            raise DocumentPortalExeption("Invocation Error in ConversationalRAG", sys)
        
    def _load_llm(self):
        try:
            llm = Model_loader().load_llm()
            if not llm:
                raise ValueError("LLM coudnt be loaded")
            self.log.info("LLM loaded successfully", session_id = self.session_id)
            return llm
        except Exception as e:
            self.log.error("Failed to load LLM", error = str(e))
            raise DocumentPortalExeption("LLM loading error in ConversationalRAG", sys)
        

    @staticmethod
    def _format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    def _build_lcel_chain(self):
        try:
            question_rewriter = (
                {"input":itemgetter("input"), "chat_history": itemgetter("chat_history")}
                | self.contextualize_prompt
                | self.llm
                | StrOutputParser()
            )
            retrieve_docs = question_rewriter| self.retriever | self._format_docs
            self.chain = (
            {
                "context":retrieve_docs,
                "input": itemgetter("input"),
                "chat_history": itemgetter("chat_history")
            }
            | self.qa_prompt
            | self.llm
            | StrOutputParser()
        )
            self.log.info("LCEL chain built successfully", session_id = self.session_id)
        except Exception as e:
            self.log.info("Failed to build LCEL chain", error = str(e))
            raise DocumentPortalExeption("Chain building error in conversationalRAG", sys)
