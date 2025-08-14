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


# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM

# def load_fake_uploaded_file(file_path:Path):
#     return io.BytesIO(file_path.read_bytes())

# def test_compare_documents():
#     ref_path = Path("C:\\Users\\bsmun\\document_portal\\data\\document_compare\\Long_Report_V1.pdf")
#     act_path = Path("C:\\Users\\bsmun\\document_portal\\data\\document_compare\\Long_Report_V2.pdf")
    
#     class FakeUpload:
#         def __init__(self, file_path:Path):
#             self.name = file_path.name
#             self.buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self.buffer

#     comparator = DocumentIngestion()
#     ref_upload = FakeUpload(ref_path)
#     act_upload = FakeUpload(act_path)

#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)
#     combined_text = comparator.combine_document()
#     comparator.clean_old_session(keep_latest=3)

#     print("\n Combined Text preview (First 1000 chars: )\n")
#     combined_text[:1000]

#     llm_comparator = DocumentComparatorLLM()
#     comparison_pdf = llm_comparator.compare_documents(combined_text)

#     print("\n=== COMPARISION RESULT ===")
#     print(comparison_pdf.head())

# if __name__ == "__main__":
#     test_compare_documents()

#Testing code for documents chat functionality
import sys
from pathlib import Path
from langchain_community.vectorstores import FAISS
from src.single_document_chat.data_ingestion import SingleDocIngestor
from src.single_document_chat.retrival import ConversationalRAG
from utils.model_loader import Model_loader

FAISS_INDEX_PATH = Path("faiss_index")
def test_conversional_rag_pdf(pdf_path:str, question:str):
    try:
        model_loader = Model_loader()
        if FAISS_INDEX_PATH.exists():
            print("Loading existing FAISS index...")
            embeddings = model_loader.load_embeddings()
            vectorstore = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)

            retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":5})
        else:
            print("FAISS index is not found. Ingesting PDF and creating index...")
            with open(pdf_path,"rb") as f:
                upload_file = [f]
                ingestor = SingleDocIngestor()
                retriever = ingestor.ingest_file(upload_file)
        print("Running Conversational RAG...")
        session_id = "test_conversational_rag"
        rag = ConversationalRAG(retriever=retriever, session_id=session_id)
        response = rag.invoke(question)
        print(f"\nQuestion: {question}\nAnswer: {response}")

    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
    
    if not Path(pdf_path).exists():
        print(f"PDF file does not exist: {pdf_path}")
        sys.exit(1)

if __name__=="__main__":
    pdf_path = r"C:\\Users\\bsmun\\document_portal\\data\\single_document_chat\\NIPS-2017-attention-is-all-you-need-Paper.pdf"
    question = "What is the main topic of the document?"

    #Run the test
    test_conversional_rag_pdf(pdf_path,question)



