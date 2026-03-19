"""Celery application for async task processing."""

from celery import Celery
from core.config import settings

celery_app = Celery(
    "qsentra",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "ct-log-monitor": {
            "task": "engines.discovery.monitor_ct_logs",
            "schedule": settings.CT_LOG_INTERVAL_HOURS * 3600,
        },
        "asset-rescan": {
            "task": "engines.scanner.rescan_assets",
            "schedule": 21600,  # 6 hours
        },
    },
)
