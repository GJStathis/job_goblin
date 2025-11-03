from celery import Celery  # type: ignore[import-untyped]

# Configure Celery
celery_app = Celery(
    "job_scraper",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["src.hoarder.tasks.job_processing"],
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

if __name__ == "__main__":
    celery_app.start()
