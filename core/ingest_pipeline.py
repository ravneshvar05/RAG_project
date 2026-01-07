
from core.ingestion import load_text_file
from core.chunking import semantic_chunk
from core.embeddings import embed_text
from db.crud import insert_chunk
from db.database import init_db

def ingest_document(file_path: str):
    
    init_db()

    data = load_text_file(file_path)
    chunks = semantic_chunk(data["text"], data["document"])

    for chunk in chunks:
        embedding = embed_text(chunk["text"])

        insert_chunk(
            document=chunk["document"],
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            embedding=embedding
        )

    return {
        "document": data["document"],
        "chunks_ingested": len(chunks)
    }
