"""Exercise 11.3: store the documents in PostgreSQL with pgvector and retrieve with SQL.

Run ../pgvector_setup.sql first.
"""
import os

import psycopg
from sentence_transformers import SentenceTransformer

DSN = os.environ.get("PG_DSN", "postgresql://de_user:de_password@localhost:5432/warehouse")
docs = [
    ("shipping-policy", "Orders above 500 MAD ship for free anywhere in Morocco."),
    ("refund-policy", "Refunds are processed within 7 business days after we receive the item."),
    ("support-hours", "Customer support is open from 9:00 to 18:00, Monday to Saturday."),
    ("premium", "Premium members get 10% off every order and priority delivery."),
]

embedder = SentenceTransformer("all-MiniLM-L6-v2")


def to_pgvector(vec) -> str:
    """pgvector accepts a text literal like '[0.1,0.2,...]' cast to ::vector."""
    return "[" + ",".join(f"{x:.6f}" for x in vec) + "]"


with psycopg.connect(DSN) as conn:
    conn.execute("TRUNCATE doc_chunks")          # make the script safe to re-run
    vectors = embedder.encode([text for _, text in docs], normalize_embeddings=True)
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO doc_chunks (source, content, embedding) VALUES (%s, %s, %s::vector)",
            [(src, text, to_pgvector(v)) for (src, text), v in zip(docs, vectors)],
        )


def retrieve(question: str, k: int = 2) -> list[tuple[str, str, float]]:
    q = to_pgvector(embedder.encode([question], normalize_embeddings=True)[0])
    with psycopg.connect(DSN) as conn:
        return conn.execute(
            """
            SELECT source, content, 1 - (embedding <=> %s::vector) AS similarity
            FROM doc_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (q, q, k),
        ).fetchall()


for source, content, similarity in retrieve("How long does a refund take?"):
    print(f"{similarity:.3f}  [{source}] {content}")
