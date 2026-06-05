from celery import Celery
from backend_service.core.config import settings

celery_app = Celery(
    "plate_worker", broker=settings.BROKER_URL, backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,
    include=['backend_service.worker.tasks'] 
)
