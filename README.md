# AgenticScraping

This project demonstrates an agent-based scraping backend using FastAPI, Celery and CrewAI Flows.

## Quickstart

```bash
poetry install
playwright install
cp .env-example .env
cd docker
docker-compose up -d db redis
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

Then open `http://localhost:8000/ui` to access the web interface. Enter a
natural language scraping request and download the results once the task
completes.

