import sqlite3
from pathlib import Path

DB_PATH = Path("chunkdata.db")  # your existing DB

def get_connection():
    return sqlite3.connect(DB_PATH)

def clear_all_embeddings():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Delete all rows from documents table
    cursor.execute("DELETE FROM documents")
    conn.commit()
    conn.close()
    print("All embeddings and document rows deleted successfully.")

if __name__ == "__main__":
    clear_all_embeddings()
