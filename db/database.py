# 

import mysql.connector
import os
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

# Get environment variables with safe defaults
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "defaultdb")

# DB_PORT: convert to int, default 3306 if missing or invalid
try:
    DB_PORT = int(os.getenv("DB_PORT", 3306))
except (TypeError, ValueError):
    DB_PORT = 3306

def get_connection():
    """
    Returns a MySQL connection using environment variables.
    """
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    return conn

def init_db():
    """
    Creates the `documents` table if it doesn't exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            document VARCHAR(255) NOT NULL,
            chunk_id INT NOT NULL,
            text TEXT NOT NULL,
            embedding LONGBLOB NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
