# llm/prompt.py

def build_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n".join([f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(chunks)])
    prompt = f"""
You are a helpful question answering assistant.

Answer the question in complete, detailed sentences using ALL the provided context.
Do NOT use any outside knowledge.
If the answer cannot be found in the context, say exactly:
"I don't know based on the provided context."

{context}

Question:
{question}

Answer:
""".strip()
    return prompt