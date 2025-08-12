import sys
import datetime
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption
from datetime import datetime, timezone 
import uuid 
class DocumentIngestion:
    def __init__(self, base_dir:str="data\document_compare", session_id=None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.log.info("Document comparator initialized.", session_path = str(self.session_path))
    
    def save_uploaded_files(self, reference_file, actual_file):
        try:

            ref_path = self.base_dir/reference_file.name
            act_path = self.base_dir/actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
            
            with open(ref_path,"wb") as f:
                f.write(reference_file.getbuffer())

            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files saved", reference = str(ref_path), actual = str(act_path))
            return ref_path, act_path


        except Exception as e:
            self.log.error(f"Error in saving uploaded PDF: {e}")
            raise DocumentPortalExeption("An error occured while saving uploaded PDF", sys)
    def read_pdf(self, pdf_path)->str:
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        all_text.append(f"\n---Page{page_num+1}---\n{text}")
                self.log.info("PDF readed successfully", file=str(pdf_path), pages = len(all_text))
                return "\n".join(all_text)
            
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalExeption("An error occured while reading the PDF", sys)
        

    def combine_document(self)-> str:
        try:
            doc_parts = []
            for file in sorted(self.session_path.iterdir()):
                if file.is_file() and file.suffix==".pdf":
                    content = self.read_pdf(file)
                    doc_parts.append(f"Document: {file}\n{content}")

            combine_text = "\n\n".join(doc_parts)
            self.log.info("Document combined", count = len(doc_parts), session = self.session_id)
            return combine_text
        
        except Exception as e:
            self.log.error("Error while comparing documents")
            raise DocumentPortalExeption("An error occurred while comparing documents.",sys) 
    def clean_old_session(self, keep_latest:int = 3):
        try:
            session_folder = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse=True
            )
            for folder in session_folder[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink
                folder.rmdir()
                self.log.info("Old session folder deleted",path = str(folder))
        except Exception as e:
            self.log.error("Error cleaning old sessions", error=str(e))
            raise DocumentPortalExeption("Error cleaning se ssions", sys)
