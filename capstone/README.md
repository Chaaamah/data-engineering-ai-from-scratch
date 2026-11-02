# Capstone — A churn intelligence platform for an online shop

This folder gives you the data and the plan. Building the platform is your job: that is what makes it a portfolio project.

## 1. Generate and load the data

```bash
python capstone/generate_shop_data.py     # 5,000 customers, ~50,000 orders, 3,000 tickets
bash capstone/load_raw.sh                 # loads them into the raw schema
```

The data has a genuine churn signal: customers with many support tickets are more likely to stop ordering. Your model should find it.

## 2. Target architecture

| Layer | What you build | Chapter |
| --- | --- | --- |
| Sources | Shop tables in PostgreSQL (`raw` schema) and a folder of policy documents | 4 |
| Ingestion | Idempotent Python jobs that copy new and changed rows | 6 |
| Transformation | dbt staging models, a star schema and a `customer_features` table | 5, 6 |
| Orchestration and quality | One Airflow DAG: ingest, dbt run, dbt test, freshness checks | 7 |
| Machine learning | Weekly training on `customer_features`, tracked in MLflow, promoted only if it beats the champion | 10, 12 |
| Serving | FastAPI with `/predict` for churn scores and `/ask` for a RAG assistant over the policies | 11, 12 |

## 3. Build order

Commit to Git after each step.

- [ ] Docker Compose with PostgreSQL (pgvector image) and Airflow
- [ ] Data generated and loaded into `raw`
- [ ] Ingestion jobs from `raw` into `staging`, safe to run twice
- [ ] dbt project: staging models, star schema, `customer_features`, tests
- [ ] Airflow DAG running end to end, with failure alerts
- [ ] Churn model trained on `customer_features`, tracked in MLflow
- [ ] FastAPI service with `/predict`, tested
- [ ] Policy documents chunked, embedded into pgvector, `/ask` connected to an LLM
- [ ] README with an architecture diagram, setup steps, screenshots and next improvements

## 4. Features worth building in `customer_features`

Compute every feature **as of a cut-off date**, using only data from before it, and label churn from what happens **after** it (for example: no paid order in the next 60 days).

- Recency: days since the last paid order
- Frequency: paid orders in the last 30, 90 and 180 days
- Monetary: spend in the last 90 days, average order value
- Trend: spend in the last 30 days divided by the 90-day monthly average
- Support: tickets in the last 90 days, share of tickets about refunds or damage
- Tenure: days since signing up; plan; city

## 5. Suggested repository layout

```text
churn-platform/
├── docker-compose.yml
├── ingestion/            # Python extract-and-load jobs
├── dbt/                  # staging, marts, customer_features, tests
├── airflow/dags/
├── ml/                   # training, evaluation, promotion
├── api/                  # FastAPI: /predict and /ask
├── docs/policies/        # documents for the RAG assistant
├── tests/
└── README.md             # the first thing a recruiter reads
```

## 6. Definition of done

- One command starts everything: `docker compose up`.
- Running the whole pipeline twice changes nothing the second time.
- Every dbt model has tests, and a failing test stops the DAG.
- The README explains the business problem, the design decisions and the trade-offs.
- No password, key or `.env` file is committed.
