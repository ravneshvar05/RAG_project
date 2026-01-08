# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# MODEL_NAME = "google/flan-t5-base"

# print("Loading FLAN-T5 model... This may take 10-20s on first run.")
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
# print("Model loaded successfully!")

# def generate_answer(prompt: str) -> str:
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=256,
#         temperature=0.0
#     )
#     decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)


#     for prefix in ["Answer:", "answer:"]:
#         if decoded.lower().startswith(prefix.lower()):
#             decoded = decoded[len(prefix):].strip()
#     return decoded

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()  

# Token will come from environment (Space / local)
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# Create inference client
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    # model="meta-llama/Llama-2-7b-chat-huggingface",
    # model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HF_API_TOKEN
)

def generate_answer(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]

    response = client.chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.0
    )

    answer = response.choices[0].message.content.strip()

    # HARD SAFETY GUARD
    refusal_text = "I don't know based on the provided context."

    if "CONTEXT:" in prompt:
        # If model answer does NOT reference context keywords
        if answer.lower().startswith("i don't know"):
            return refusal_text

        # If hallucination keywords detected
        hallucination_triggers = [
            "generally",
            "in general",
            "commonly",
            "typically",
            "outside the context",
            "based on knowledge"
        ]

        for t in hallucination_triggers:
            if t in answer.lower():
                return refusal_text

    return answer


# ✅ Local test (runs ONLY when you execute client.py directly)
# if __name__ == "__main__":
#     test_prompt = "Explain Retrieval Augmented Generation in simple terms."
#     print("Testing LLM client...\n")
#     print(generate_answer(test_prompt))

