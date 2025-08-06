import os
from pathlib import Path
from src.document_analyzer.data_ingestion import DocumentHandler
from src.document_analyzer.document_analysis import DocumentAnalyzer

PDF_PATH = r"C:\Users\bsmun\document_portal\data\document_analysis\sample.pdf"

class DummyFile:
    def __init__(self, file_path):
        self.name = Path(file_path).name
        self._file_path = file_path

    def getbuffer(self):
        return open(self._file_path, "rb").read()
    
def main():
    try:
        #------Step 1: DATA INGESTION
        print("Starting PDF ingestion")
        dummy_pdf = DummyFile(PDF_PATH)

        handler = DocumentHandler(session_id="test_ingesion_analysis")

        save_path = handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {save_path}")

        text_content = handler.read_pdf(save_path)
        print(f"Extracted text length: {len(text_content)}")

        #------Step 2: DATA ANALYSIS
        print("Starting metadata analysis...")
        analyzer = DocumentAnalyzer()
        analysis_result = analyzer.analyze_document(text_content)

        #------Step 3: DISPLAY RESULT
        print("METADATA ANALYSIS RESULTS")
        for key, value in analysis_result.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Test failed {e}")

if __name__ == "__main__":
    main()