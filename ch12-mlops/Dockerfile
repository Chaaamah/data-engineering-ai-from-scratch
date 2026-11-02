# Build from the ch12-mlops folder after copying the trained model next to it:
#   cp ../model.joblib . && docker build -t churn-api . && docker run -p 8000:8000 churn-api
FROM python:3.12-slim
WORKDIR /app
COPY requirements-serving.txt .
RUN pip install --no-cache-dir -r requirements-serving.txt
COPY serving/ serving/
COPY model.joblib .
RUN useradd --create-home appuser
USER appuser
CMD ["uvicorn", "serving.app:app", "--host", "0.0.0.0", "--port", "8000"]
