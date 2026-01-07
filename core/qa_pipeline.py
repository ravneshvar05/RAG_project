from core.retrieval import retrieve_top_k  # your cosine similarity retrieval
from llm.prompt import build_prompt
from llm.client import generate_answer

def answer_question(question: str, k: int = 3) -> dict:
    """
    Full end-to-end QA pipeline:
    - Retrieve top-k relevant chunks
    - Build hallucination-safe prompt
    - Generate answer using local FLAN-T5
    - Compute confidence score
    - Collect evidence
    """

    # Retrieve top-k chunks
    top_chunks = retrieve_top_k(question, k=k)

    if not top_chunks:
        return {
            "question": question,
            "answer": "I don’t know based on the provided context.",
            "confidence": 0.0,
            "evidence": []
        }

    # Build prompt
    chunk_texts = [c["text"] for c in top_chunks]
    prompt = build_prompt(question, chunk_texts)

    # Generate answer
    answer = generate_answer(prompt)

    # Compute confidence (average similarity of top-k chunks)
    avg_similarity = sum(c["similarity"] for c in top_chunks) / len(top_chunks)

    # Collect evidence
    evidence = [
        {"document": c["document"], "chunk_id": c["chunk_id"], "text": c["text"]}
        for c in top_chunks
    ]

    # Prepare final response
    response = {
        "question": question,
        "answer": answer,
        "confidence": round(avg_similarity, 3),
        "evidence": evidence
    }

    return response
