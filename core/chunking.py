import re
from typing import List, Dict

def semantic_chunk(text: str, document: str, max_sentences: int = 4) -> List[Dict]:
    """
    Splits text into semantic chunks using paragraph + sentence grouping.
    """
    chunks = []
    chunk_id = 0

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    for para in paragraphs:
        sentences = re.split(r'(?<=[.!?])\s+', para)

        for i in range(0, len(sentences), max_sentences):
            group = sentences[i:i + max_sentences]
            chunk_text = " ".join(group).strip()

            if chunk_text:
                chunks.append({
                    "document": document,
                    "chunk_id": chunk_id,
                    "text": chunk_text
                })
                chunk_id += 1

    return chunks