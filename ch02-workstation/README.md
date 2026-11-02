# Chapter 2 — Setting up your workstation

## Check your tools

```bash
python3 --version        # 3.11 or newer
git --version
docker --version
docker compose version
```

## Start PostgreSQL

From the repository root:

```bash
docker compose up -d postgres
docker compose exec postgres psql -U de_user -d warehouse -c "SELECT version();"
```

## Project layout used in every chapter

```text
data-ai-book/
├── docker-compose.yml
├── requirements.txt
├── .env                 # secrets, never committed
├── data/
│   ├── raw/             # untouched input files
│   └── processed/       # cleaned outputs
├── pipelines/           # extract, transform, load code
├── sql/                 # SQL models and queries
├── notebooks/           # exploration only
├── tests/               # automated tests
└── README.md
```

## Solutions

### Exercise 1 — Create and push the project

```bash
mkdir -p data-ai-book/{data/raw,data/processed,pipelines,sql,notebooks,tests}
cd data-ai-book
git init
printf ".venv/\n__pycache__/\n.env\n" > .gitignore
echo "# Data & AI book project" > README.md
git add . && git commit -m "Create project layout"
git branch -M main
git remote add origin https://github.com/<your-user>/data-ai-book.git
git push -u origin main
```

Empty folders are not tracked by Git. Add a `.gitkeep` file to each one if you want them in the repository.

### Exercise 2 — Prove that the volume keeps your data

```bash
docker compose exec postgres psql -U de_user -d warehouse \
  -c "CREATE TABLE test (id INT); INSERT INTO test VALUES (1), (2), (3);"

docker compose stop postgres
docker compose start postgres

docker compose exec postgres psql -U de_user -d warehouse -c "SELECT * FROM test;"
```

The three rows are still there because the data lives in the `pgdata` volume, not inside the container. Only `docker compose down -v` deletes the volume.

### Exercise 3 — Inspect a CSV with the terminal only

```bash
head -n 1 file.csv | tr ',' '\n'   # column names, one per line
wc -l file.csv                      # rows + 1 header line
head -n 5 file.csv                  # first records
cut -d, -f2 file.csv | sort | uniq -c | sort -rn | head   # most common values of column 2
```

`cut` splits on every comma, so it gives wrong results when values contain quoted commas. That is one reason real pipelines use a CSV parser such as pandas.
