FROM python:3.11-slim as base
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir fastapi uvicorn celery crewai playwright sqlalchemy psycopg[binary] httpx bs4 opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-celery
RUN playwright install --with-deps
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

