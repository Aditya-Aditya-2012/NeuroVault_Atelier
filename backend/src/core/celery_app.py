from celery import Celery

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

celery_app = Celery(
    "neurovault_tasks",
    broker = CELERY_BROKER_URL,
    backend= CELERY_RESULT_BACKEND,
    include=["backend.src.tasks.ai_tasks"]
)

celery_app.conf.task_routes = {
    "backend.src.tasks.ai_tasks.*": {"queue": "ai_queue"}
}