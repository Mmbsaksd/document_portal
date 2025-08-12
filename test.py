# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler
# from src.document_analyzer.document_analysis import DocumentAnalyzer

# PDF_PATH = r"C:\Users\bsmun\document_portal\data\document_analysis\sample.pdf"

# class DummyFile:
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()
    
# def main():
#     try:
#         #------Step 1: DATA INGESTION
#         print("Starting PDF ingestion")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(session_id="test_ingesion_analysis")

#         save_path = handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {save_path}")

#         text_content = handler.read_pdf(save_path)
#         print(f"Extracted text length: {len(text_content)}")

#         #------Step 2: DATA ANALYSIS
#         print("Starting metadata analysis...")
#         analyzer = DocumentAnalyzer()
#         analysis_result = analyzer.analyze_document(text_content)

#         #------Step 3: DISPLAY RESULT
#         print("METADATA ANALYSIS RESULTS")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")
#     except Exception as e:
#         print(f"Test failed {e}")

# if __name__ == "__main__":
#     main()


import io
from pathlib import Path
from src.document_compare.data_ingestion import DocumentIngestion
from src.document_compare.document_comparator import DocumentComparatorLLM

def load_fake_uploaded_file(file_path:Path):
    return io.BytesIO(file_path.read_bytes())

def test_compare_documents():
    ref_path = Path("C:\\Users\\bsmun\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
    act_path = Path("C:\\Users\\bsmun\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")
    
    class FakeUpload:
        def __init__(self, file_path:Path):
            self.name = file_path.name
            self.buffer = file_path.read_bytes()

        def getbuffer(self):
            return self.buffer

    comparator = DocumentIngestion()
    ref_upload = FakeUpload(ref_path)
    act_upload = FakeUpload(act_path)

    ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
    combined_text = comparator.combine_document()
    comparator.clean_old_session(keep_latest=3)

    print("\n Combined Text preview (First 1000 chars: )\n")
    combined_text[:1000]

    llm_comparator = DocumentComparatorLLM()
    comparison_pdf = llm_comparator.compare_documents(combined_text)

    print("\n=== COMPARISION RESULT ===")
    print(comparison_pdf.head())

if __name__ == "__main__":
    test_compare_documents()

