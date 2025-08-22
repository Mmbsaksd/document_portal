from __future__ import annotations
import os
import sys
import json
import uuid
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable, List, Optional, Dict, Any

import fitz
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS


from utils.model_loader import Model_loader
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption




class FaissManager:
    def __init__(self, index_dir:Path,model_loader:Optional[Model_loader]=None):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)

        self.meta_path = self.index_dir/"ingested_meta.json"
        self._meta:Dict[str,Any] = {"rows":{}}

        if self.meta_path.exists():
            try:
                self.meta = json.loads(self.meta_path.read_text(encoding="uft-8")) or {"rows":{}}

            except Exception as e:
                self.meta = {"rowa":{}}
        self.model_loader = model_loader or Model_loader()
        self.emb = self.model_loader.load_embeddings()
        self.vs:Optional[FAISS] = None

    def _exists(self)->bool:
        return (self.index_dir/"index.faiss").exists() and (self.index_dir/"index.pkl").exists()
    
    @staticmethod
    def _fingerprint(text:str,md: Dict[str,Any])->str:
        src = md.get("source") or md.get("file_path")
        rid = md.get("row_id")
        if src is not None:
            return f"{src}::{''if rid is None else rid}" 
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
    

    def save_meta(self):
        self.meta_path.write_text(json.dumps(self._meta, ensure_ascii=False), encoding="utf-8")
    def add_document():
        pass

    def load_or_create(self, docs:List[Document]):
        if self.vs is None:
            raise RuntimeError("Call load_or_create")
        pass

class DocHandler:
    def __init__(self):
        pass
    def save_pdf(self):
        pass
    def read_pdf(self):
        pass

class DocumentComparator:
    def __init__(self):
        pass
    def save_uploaded_files(self):
        pass
    def read_pdf(self):
        pass
    def combine_documents(self):
        pass
    def clean_old_session(self):
        pass

class ChatIngestor:
    def __init__(self):
        pass
    def _resolve_dir(self):
        pass
    def split(self):
        pass
    def built_retriever(self):
        pass