from celery import Celery
from celery.schedules import crontab
from app.core.settings import settings
from app.core.logging import logger, log_dir


# Initialize Celery app
celery_app = Celery(__name__, broker=settings.CELERY_BROKER_URL)

# Celery config (optional but recommended for clarity)
celery_app.conf.update(
    result_backend=settings.CELERY_RESULT_BACKEND,
    timezone="Europe/Amsterdam",
    beat_schedule={
        "pick-lottery-winner-every-midnight": {
            "task": "app.tasks.lottery_tasks.pick_today_lottery_winner",
            "schedule": crontab(hour=0, minute=0),  # Using crontab for exact timing
        },
    },
    task_routes={
        "app.tasks.*": {"queue": settings.CELERY_DEFAULT_QUEUE},
    },
    # Set the default queue name
    task_default_queue=settings.CELERY_DEFAULT_QUEUE,
    # Specifying the schedule file location
    beat_schedule_filename="app/tasks/celery/celerybeat-schedule",
    # Logging configuration
    worker_log_file=str(log_dir / "celery_worker.log"),
    worker_log_level="INFO",
    beat_log_file=str(log_dir / "celery_beat.log"),
    beat_log_level="INFO",
)

from app.tasks import lottery_tasks
