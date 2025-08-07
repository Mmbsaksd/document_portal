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
            if self.base_dir.exists() and self.base_dir.is_dir:
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted", path=str(file))
                self.log.info("Directory cleaned", directory = str(self.base_dir))

        except Exception as e:
            self.log.error(f"Error deleting the PDF: {e}")
            raise DocumentPortalExeption("An error occured while deleting existing PDF", sys)
    def save_uploaded_files(self, reference_file, actual_file):
        try:
            self.delete_existing_files()
            self.log.info("Existing file deleted successfully.")

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
