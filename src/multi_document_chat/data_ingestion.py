class DocumentIngestor:
    SUPPORTED_EXTENTION = {'.pdf','.docx','.txt','.md'}
    def __init__(self, temp_dir:str = "data\multi_doc_chat", faiss_dir:str="faiss_index", session_id:str|None=None):
        pass

    def ingest_files(self):
        pass
    
    def _create_retriver(self,documents):
        pass