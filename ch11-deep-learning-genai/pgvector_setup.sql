-- Chapter 11.5: store document chunks and their embeddings in PostgreSQL.
-- Needs the pgvector extension (included in this repo's docker-compose image).

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS doc_chunks (
    id        SERIAL PRIMARY KEY,
    source    TEXT,
    content   TEXT,
    embedding vector(384)       -- all-MiniLM-L6-v2 produces 384 numbers per text
);

-- An approximate nearest-neighbour index keeps searches fast as the table grows.
CREATE INDEX IF NOT EXISTS doc_chunks_embedding_idx
    ON doc_chunks USING hnsw (embedding vector_cosine_ops);
