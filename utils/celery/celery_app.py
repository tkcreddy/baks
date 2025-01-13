from celery import Celery

# Initialize Celery
celery_app = Celery(
    'aws_instance_creation',
    broker='redis://localhost:6379/0',  # Redis as the broker
    backend='redis://localhost:6379/0'  # Redis as the result backend
)

# Configuration for Celery
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
