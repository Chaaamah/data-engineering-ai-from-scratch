# Data Engineering & AI from Scratch — Companion Code

Code, sample data and exercise solutions for the book **Data Engineering & AI from Scratch: A Hands-On Guide to Building Data Pipelines and Machine Learning Systems** by Chaima Agoumi.

Every chapter of the book has a folder here. Each folder holds the chapter's code, ready to run, and a `solutions/` folder with worked answers to the chapter's exercises.

> Try each exercise yourself before opening `solutions/`. You learn far more from a wrong first attempt than from reading a right answer.

## Quick start

```bash
git clone https://github.com/Chaaamah/data-engineering-ai-from-scratch.git
cd data-engineering-ai-from-scratch

python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

cp .env.example .env               # connection settings used by the scripts
docker compose up -d postgres      # PostgreSQL 16 with the pgvector extension
```

Kafka (Chapter 9) has its own profile so it only runs when you need it:

```bash
docker compose --profile streaming up -d
```

## What is in each folder

| Chapter | Folder | What you will run |
| --- | --- | --- |
| 1. What data engineering is | [`ch01-foundations`](ch01-foundations) | Model answers to the reflection exercises |
| 2. Your workstation | [`ch02-workstation`](ch02-workstation) | Commands, project layout, Docker checks |
| 3. Python for data work | [`ch03-python`](ch03-python) | pandas on messy sample data, API calls with retries |
| 4. SQL and relational databases | [`ch04-sql`](ch04-sql) | Shop schema, joins, window functions, indexes |
| 5. Data modeling and warehousing | [`ch05-modeling`](ch05-modeling) | Star schema, date dimension, slowly changing dimensions |
| 6. ETL and ELT | [`ch06-pipeline`](ch06-pipeline) | Idempotent weather pipeline, tests, dbt project |
| 7. Orchestration and data quality | [`ch07-orchestration`](ch07-orchestration) | Airflow DAG with quality checks |
| 8. Big data | [`ch08-big-data`](ch08-big-data) | 5-million-row benchmark: pandas, DuckDB, Spark |
| 9. Streaming | [`ch09-streaming`](ch09-streaming) | Kafka producer, consumer, idempotent consumer |
| 10. Machine learning | [`ch10-ml`](ch10-ml) | Churn model, cross-validation, model comparison |
| 11. Deep learning and generative AI | [`ch11-deep-learning-genai`](ch11-deep-learning-genai) | PyTorch network, RAG with pgvector |
| 12. MLOps and the capstone | [`ch12-mlops`](ch12-mlops) | MLflow tracking, FastAPI serving, prediction logging |
| Capstone | [`capstone`](capstone) | Fake shop data generator and the build plan |

## Requirements

- Python 3.11 or newer
- Docker with Docker Compose
- Git
- Java 17 or newer, only for Spark in Chapter 8

dbt (Chapter 6) and Apache Airflow (Chapter 7) have large dependency trees. Install each in its own virtual environment, as explained in those chapters' folders.

## Configuration

Scripts read the database address from the `PG_DSN` environment variable and fall back to the local Docker database:

```text
PG_DSN=postgresql://de_user:de_password@localhost:5432/warehouse
```

The password in this repository is for learning on your own machine only. Never reuse it anywhere else.

## License

The code in this repository is released under the [MIT License](LICENSE). The book's text and figures are © 2026 Chaima Agoumi and are not covered by this license.

## Author

**Chaima Agoumi** — Casablanca, Morocco

- LinkedIn: [Chaima Agoumi](https://www.linkedin.com/in/chaima-a-218657295)
- GitHub: [@Chaaamah](https://github.com/Chaaamah)
- Email: agoumi.chaima@gmail.com

Found a bug or a broken example? Please open an issue.
