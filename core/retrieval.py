# core/retrieval.py

from core.embeddings import embed_text
from core.similarity import cosine_similarity
from db.crud import fetch_all_chunks

def retrieve_top_k(query: str, k: int = 3):
    """
    Retrieve top-k most relevant chunks for a query
    """
    query_embedding = embed_text(query)

    chunks = fetch_all_chunks()
    scored_chunks = []

    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])

        scored_chunks.append({
            "document": chunk["document"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "similarity": score
        })

    # Sort by similarity (descending)
    scored_chunks.sort(key=lambda x: x["similarity"], reverse=True)

    return scored_chunks[:k]
