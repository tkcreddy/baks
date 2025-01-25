from celery import Celery
class CeleryAppConfig:
    def __init__(self, name='utils.celery.tasks', broker_url='redis://localhost:6379/0',
                 backend_url='redis://localhost:6379/0') -> None:
        """
        Initializes the Celery application with broker and backend configurations.
        """
        self.app = Celery(name, broker=broker_url, backend=backend_url)
        self.configure()

    def configure(self):
        """
        Configures the Celery application with dynamic routing and task queues.
        """

        self.app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True)

# Initialize Celery app
celery_app = CeleryAppConfig().app


