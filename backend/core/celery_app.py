"""
Q-Sentra Celery Application
Configures async task processing with Redis broker.
"""
from celery import Celery
from core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "qsentra",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=["tasks.celery_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    task_soft_time_limit=240,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
    # Scheduled tasks
    beat_schedule={
        "ct-log-monitor": {
            "task": "tasks.celery_tasks.monitor_ct_logs",
            "schedule": 21600.0,  # Every 6 hours
        },
        "rescan-critical": {
            "task": "tasks.celery_tasks.rescan_critical_assets",
            "schedule": 3600.0,  # Every hour
        },
    },
)
