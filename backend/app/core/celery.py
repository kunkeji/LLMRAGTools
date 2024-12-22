from celery import Celery
from app.core.config import settings

celery = Celery(
    "agent_tools",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email",
        "app.tasks.document",
    ]
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    worker_max_tasks_per_child=200,
    broker_connection_retry_on_startup=True,
)

# 定时任务配置
celery.conf.beat_schedule = {
    "sync-emails": {
        "task": "app.tasks.email.sync_emails",
        "schedule": 300.0,  # 5分钟
    },
    "retry-failed-emails": {
        "task": "app.tasks.email.retry_failed_emails",
        "schedule": 600.0,  # 10分钟
    },
} 