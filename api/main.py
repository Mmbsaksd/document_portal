#uvicorn main:app --reload

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Dict, Any


from src.document_ingestion.data_ingestion import (
    DocHandler,
    DocumentComparator,
    ChatIngestor,
    FaissManager
)
from src.document_analyzer.document_analysis import DocumentAnalyzer
from src.document_compare.document_comparator import DocumentComparatorLLM
from src.document_chat.retrival import ConversationalRAG


app = FastAPI(title = "Document Portal API", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/health")
def health() -> Dict[str,str]:
    return{"status":"ok","service":"document-portal"}

class FastAPIAdapter:
    def __init__(self,uf:UploadFile):
        self.uf = uf
        self.name = uf.filename
    def getbuffer(self):
        self._uf.file.seek(0)
        return self.uf.file.read()


def _read_pdf_via_handler(handler:DocHandler, path:str)->str:
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error reading PDF: {str(e)}")


@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)) ->Any:
    try:
        dh = DocHandler()
        saved_path = dh.save_pdf(FastAPIAdapter(file))
        text = _read_pdf_via_handler(dh, saved_path)

        analyzer = DocumentAnalyzer()
        result = analyzer.analyze_document(text)
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed:{e}")

@app.post("/compare")
async def compare_document(referance:UploadFile = File(...), actual:UploadFile=File(...)) ->Any:
    try:
        dc = DocumentComparator()
        ref_path, act_path = dc.save_uploaded_files(FastAPIAdapter(referance),FastAPIAdapter(actual))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

@app.post("/chat/query")
async def chat_query():
    try:
        pass
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
    



