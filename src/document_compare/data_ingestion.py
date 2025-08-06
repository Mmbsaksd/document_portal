import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from exeption.custom_exeption import DocumentPortalExeption

class DocumentComparator:
    def __init__(self, base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    def delete_existing_files(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error deleting the PDF: {e}")
            raise DocumentPortalExeption("An error occured while deleting existing PDF", sys)
    def save_uploaded_files(self):
        try:
            pass
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
