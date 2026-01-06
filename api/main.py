# api/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

from core.ingest_pipeline import ingest_document  # ✅ updated function name
from core.qa_pipeline import answer_question

app = FastAPI(title="RAG QA System")

# Directory to store uploaded documents
UPLOAD_DIR = Path("uploaded_docs")
UPLOAD_DIR.mkdir(exist_ok=True)


# -------------------------------
# POST /ingest
# -------------------------------
@app.get("/")
def hello():
    return {"message": "Welcome to the RAG QA System API"}
@app.post("/ingest")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a .txt document, split into semantic chunks, generate embeddings, and store in DB.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files allowed")

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        chunks_added = ingest_document(file_path)  # ✅ use correct function name
        return {"status": "success", "document": file.filename, "chunks_added": chunks_added}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingest pipeline error: {str(e)}")


# -------------------------------
# POST /ask
# -------------------------------
@app.post("/ask")
async def ask_question(question: str):
    """
    Ask a question: retrieves top-k relevant chunks, generates answer, returns confidence & evidence.
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        response = answer_question(question, k=3)  # k can be adjusted as needed
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA pipeline error: {str(e)}")


# -------------------------------
# GET /health
# -------------------------------
@app.get("/health")
async def health_check():
    """
    Check system status:
    - Database file exists
    - LLM is loaded
    """
    try:
        db_exists = Path("chunkdata.db").exists()
        llm_loaded = True  # assume LLM is loaded if no errors in import

        status = "ok" if db_exists and llm_loaded else "error"
        return {
            "status": status,
            "db_exists": db_exists,
            "llm_loaded": llm_loaded
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
