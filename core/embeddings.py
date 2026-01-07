import numpy as np
from sentence_transformers import SentenceTransformer


_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)


def embed_text(text: str) -> np.ndarray:
    """
    Generate embedding for a single text string.
    Returns a float32 NumPy array.
    """
    embedding = _model.encode(text, convert_to_numpy=True)
    return embedding.astype("float32")
