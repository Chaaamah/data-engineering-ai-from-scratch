"""Chapter 11.6: the retrieval half of RAG, in plain Python.

The first run downloads the small all-MiniLM-L6-v2 embedding model (about 90 MB).
"""
import numpy as np
from sentence_transformers import SentenceTransformer

docs = [
    "Orders above 500 MAD ship for free anywhere in Morocco.",
    "Refunds are processed within 7 business days after we receive the item.",
    "Customer support is open from 9:00 to 18:00, Monday to Saturday.",
    "Premium members get 10% off every order and priority delivery.",
]

embedder = SentenceTransformer("all-MiniLM-L6-v2")   # small, free, runs on CPU
doc_vectors = embedder.encode(docs, normalize_embeddings=True)


def retrieve(question: str, k: int = 2) -> list[str]:
    q = embedder.encode([question], normalize_embeddings=True)[0]
    scores = doc_vectors @ q                 # cosine similarity
    best = np.argsort(scores)[::-1][:k]
    return [docs[i] for i in best]


def build_prompt(question: str) -> str:
    context = "\n".join(f"- {c}" for c in retrieve(question))
    return (
        "Answer the question using only the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )


if __name__ == "__main__":
    print(build_prompt("How long does a refund take?"))
