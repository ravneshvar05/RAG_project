import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()
def get_connection():
    # print("DB_PORT =", os.getenv("DB_PORT"))
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return conn


def init_db():
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
