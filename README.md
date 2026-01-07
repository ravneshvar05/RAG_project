Retrieval-Augmented Question Answering System (RAG Backend) :-

This project implements a document ingestion and question-answering backend using FastAPI, Hugging Face models, and a traditional relational database (SQLite) — without using any vector databases.

-->>System Overview

High-level flow :-
Upload a plain text document
Split the document into semantic chunks
Generate embeddings for each chunk
Store chunks + embeddings in SQLite
Accept a user question via API
Retrieve top-K relevant chunks using cosine similarity
Generate an answer using an LLM strictly grounded in retrieved context
Return answer, confidence score, and supporting evidence

-->>Chunking Strategy

Goal :-
Split plain text documents into meaningful, semantically coherent chunks without using ML models.

Approach :-
Documents are first split by paragraph boundaries (\n\n) to preserve natural topic separation.
Each paragraph is then split into sentences using punctuation-aware rules.
Sentences are grouped into fixed-size semantic windows of 3 sentences per chunk.

Why this works :-
Avoids naïve line-based or character-based splitting
Preserves semantic continuity across related sentences
Deterministic and fast
Easy to debug and reason about
Commonly used in production-grade RAG pipelines

Stored fields per chunk:-
document: original uploaded filename
chunk_id: sequential integer per document
text: chunk content


-->>Embedding Choice
Model Used :- sentence-transformers/all-MiniLM-L6-v2

Why this model:-
Lightweight (~80MB)
CPU-friendly (no GPU required)
High-quality sentence-level semantic representations
Widely adopted in industry and research
Ideal for similarity search and retrieval tasks
Execution Strategy
Embeddings are generated locally using PyTorch
TensorFlow/Keras dependencies are avoided to ensure stability
This reduces unnecessary dependencies and compatibility issues

Retrieval Strategy (No Vector Database):-
All embeddings are stored in SQLite

At query time:
The user question is embedded
All stored chunk embeddings are fetched
Cosine similarity is computed manually
Top-K most similar chunks are retrieved


-->>LLM Choice
Model Used
Hugging Face FLAN-T5 (local inference)

Why FLAN-T5:-
Instruction-tuned model
Strong performance on question answering
Runs locally on CPU
Open-source and cost-free
Predictable output format

LLM Abstraction:-
The LLM is accessed through a dedicated client module, making it easy to:
Replace FLAN-T5 with another local model or Switch to an external API (OpenAI, Anthropic, etc.) without changing core logic

-->>Hallucination Prevention

The system actively prevents hallucinations through:
Strict prompt grounding
The LLM is instructed to answer only using retrieved context
Fallback response
If the answer is not found in context, the model must return:
"I don’t know based on the provided context."


No external knowledge access
The LLM never sees the user query without supporting chunks
This ensures faithful, explainable answers.

-->>Confidence Logic

Each answer includes a confidence score based on retrieval strength, not model guesswork.

How confidence is computed:-
Cosine similarity scores of the top-K retrieved chunks are normalized

The final confidence score reflects:-
Semantic closeness of retrieved evidence
Agreement across multiple chunks

Why this approach:-

Model probabilities are unreliable for factual confidence
Retrieval-based confidence is explainable and deterministic
Aligns with industry RAG best practices

-->>Limitations
Designed for plain text (.txt) documents only
Not optimized for millions of chunks
SQLite is not suited for high-concurrency workloads
CPU-only inference limits throughput
Sentence-based chunking may miss deeper discourse structure

