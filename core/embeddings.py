import numpy as np
from sentence_transformers import SentenceTransformer


_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# _MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
_model = SentenceTransformer(_MODEL_NAME)


def embed_text(text: str) -> np.ndarray:
    """
    Generate embedding for a single text string.
    Returns a float32 NumPy array.
    """
    embedding = _model.encode(text, convert_to_numpy=True)
    return embedding.astype("float32")


if __name__ == "__main__":
    sample_texts = [
        "What is retrieval augmented generation?",
        "How does semantic search work?",
        "Tell me about Python programming."
    ]

    for text in sample_texts:
        emb = embed_text(text)
        print(f"Text: {text}")
        print(f"Embedding shape: {emb.shape}")
        print(f"First 5 dimensions: {emb[:5]}\n")