import sqlite3
import numpy as np
from db.database import get_connection


def insert_chunk(document: str, chunk_id: int, text: str, embedding: np.ndarray):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chunks (document, chunk_id, text, embedding)
        VALUES (?, ?, ?, ?)
        """,
        (
            document,
            chunk_id,
            text,
            embedding.tobytes()
        )
    )

    conn.commit()
    conn.close()


def fetch_all_chunks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT document, chunk_id, text, embedding FROM chunks"
    )

    rows = cursor.fetchall()
    conn.close()

    results = []
    for document, chunk_id, text, embedding_blob in rows:
        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
        results.append({
            "document": document,
            "chunk_id": chunk_id,
            "text": text,
            "embedding": embedding
        })

    return results
