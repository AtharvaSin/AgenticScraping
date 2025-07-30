import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from celery import Celery
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.jobs.tasks import run_flow

app = FastAPI(title="Agentic Scraper")
FastAPIInstrumentor.instrument_app(app)

celery_app = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

static_dir = Path(__file__).resolve().parent / "static"
app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="ui")

class Prompt(BaseModel):
    prompt: str

@app.post("/scrape")
async def scrape(p: Prompt):
    task = run_flow.delay(p.prompt)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "state": result.state, "result": result.result}


@app.get("/data/{task_id}")
async def data(task_id: str, format: str = "json"):
    result = celery_app.AsyncResult(task_id)
    if not result.ready():
        return {"task_id": task_id, "state": result.state}
    data = result.result or []
    if format == "csv":
        if not isinstance(data, list) or not data:
            return {"error": "no data"}
        output = []
        headers = list(data[0].keys())
        output.append(",".join(headers))
        for row in data:
            output.append(",".join(str(row[h]) for h in headers))
        csv_data = "\n".join(output)
        return StreamingResponse(
            iter([csv_data]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={task_id}.csv"},
        )
    return data


