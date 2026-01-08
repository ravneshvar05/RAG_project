# def build_prompt(question: str, chunks: list[str]) -> str:
#     context = "\n\n".join([f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(chunks)])
#     prompt = f"""
# You are a helpful question answering assistant.

# Answer the question in complete, detailed sentences using ALL the provided context.
# Do NOT use any outside knowledge.
# If the answer cannot be found in the context, say exactly:
# "I don't know based on the provided context."

# {context}

# Question:
# {question}

# Answer:
# """.strip()
#     return prompt

def build_prompt(question: str, chunks: list[str]) -> str:
    if not chunks:
        return (
            "You are a question answering assistant.\n\n"
            "Context:\n"
            "NONE\n\n"
            f"Question:\n{question}\n\n"
            "Answer:\n"
            "I don't know based on the provided context."
        )

    context = "\n\n".join(
        [f"[CONTEXT {i+1}]\n{chunk}" for i, chunk in enumerate(chunks)]
    )

    prompt = f"""
You are a STRICT retrieval-based question answering assistant.

CRITICAL RULES (YOU MUST FOLLOW):
- Use ONLY the information in the provided CONTEXT.
- Do NOT use prior knowledge.
- Do NOT guess.
- If the answer is not explicitly stated in the context, reply EXACTLY with:
"I don't know based on the provided context."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""".strip()

    return prompt