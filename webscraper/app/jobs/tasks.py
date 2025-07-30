from celery import Celery

from app.crews.scrape_flow import ScrapeFlow
from opentelemetry.instrumentation.celery import CeleryInstrumentor

celery = Celery('tasks')
celery.conf.broker_url = 'redis://redis:6379/0'
celery.conf.result_backend = 'redis://redis:6379/0'

CeleryInstrumentor().instrument()

@celery.task(name='run_flow')
def run_flow(prompt: str):
    flow = ScrapeFlow()
    result = flow.run(prompt)
    return result
