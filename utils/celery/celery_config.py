from celery import Celery

# Initialize Celery app
app = Celery(
    'dynamic_tasks',
    broker='redis://localhost:6379/0',  # Redis as broker
    backend='redis://localhost:6379/0'  # Redis for results
)

# Basic Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
