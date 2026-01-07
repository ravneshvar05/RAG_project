from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "google/flan-t5-base"

print("Loading FLAN-T5 model... This may take 10-20s on first run.")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully!")

def generate_answer(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.0
    )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)


    for prefix in ["Answer:", "answer:"]:
        if decoded.lower().startswith(prefix.lower()):
            decoded = decoded[len(prefix):].strip()
    return decoded