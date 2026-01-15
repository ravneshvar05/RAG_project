import numpy as np
from db.database import get_connection


def insert_chunk(document: str, chunk_id: int, text: str, embedding: np.ndarray):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO documents (document, chunk_id, text, embedding)
        VALUES (%s, %s, %s, %s)
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
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT document, chunk_id, text, embedding
        FROM documents
        """
    )

    rows = cursor.fetchall()
    conn.close()

    chunks = []

    for row in rows:
        embedding = np.frombuffer(row["embedding"], dtype=np.float32)

        chunks.append({
            "document": row["document"],
            "chunk_id": row["chunk_id"],
            "text": row["text"],
            "embedding": embedding
        })

    return chunks
