# Chapter 11 — Deep learning and generative AI

```bash
python ch11-deep-learning-genai/tiny_net.py
python ch11-deep-learning-genai/simple_rag.py        # downloads a ~90 MB embedding model once
```

To finish the RAG assistant, send the printed prompt to any LLM provider's API, or to an open model running locally.

## Solutions

| Exercise | File |
| --- | --- |
| 1. Two hidden layers of 64 neurons | `solutions/ex1_two_hidden_layers.py` |
| 2. More documents and a retrieval evaluation | `solutions/ex2_retrieval_eval.py` |
| 3. RAG on PostgreSQL with pgvector | `pgvector_setup.sql` then `solutions/ex3_rag_pgvector.py` |

```bash
docker compose exec -T postgres psql -U de_user -d warehouse < ch11-deep-learning-genai/pgvector_setup.sql
python ch11-deep-learning-genai/solutions/ex3_rag_pgvector.py
```

The evaluation in exercise 2 is the habit that matters most: a fixed list of questions with known right answers, re-run after every change to the documents, the chunking or the embedding model.
