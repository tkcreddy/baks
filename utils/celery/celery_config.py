from celery import Celery
from kombu import Queue


class CeleryAppConfig:
    def __init__(self, name='utils.celery.tasks', broker_url='redis://localhost:6379/0',
                 backend_url='redis://localhost:6379/0'):
        """
        Initializes the Celery application with broker and backend configurations.
        """
        self.app = Celery(name, broker=broker_url, backend=backend_url)
        self.configure()

    def configure(self):
        """
        Configures the Celery application with dynamic routing and task queues.
        """
        # url_list={}
        url_list = [
            "https://www.google.com",
            "https://www.timesofindia.com",
            "https://www.yahoo.com",
            "https://www.cnn.com",
            "https://www.foxnews.com",
            "https://www.thehindu.com",
            "https://www.vzw.com",
            "https://www.verizon.com",
            "https://www.att.com",
            "https://www.greatandhra.com",
            "https://www.youtube.com",
            "https://www.nfl.com",
            "https://www.nba.com",
            "https://www.pgatour.com",
            "https://www.deccanchronicle.com/",
            "https://www.lll.com"
            # Add more unique host URLs here
        ]
        self.app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            # task_queues=[],  # Start with an empty list of queues
            # task_routes=(self.route_task, ),  # Use custom task routing

            beat_schedule={
                'run-health-check-every-5-seconds': {
                    'task': 'utils.celery.health_check.tasks.health_check_task',
                    'schedule': 5.0,
                    'args': [url_list],
                    'options': {
                        # ensure we don't accumulate a huge backlog of these if the workers are down
                        'expires': 5
                    }

                },
            },
        )

    # def route_task(self, name, args, kwargs, options, task=None, **kw):
    #     """
    #     Routes tasks dynamically based on a specific logic (e.g., encoded hostname).
    #     """
    #     if name == 'tasks.create_instance':
    #         # Example logic: dynamically route tasks to queues based on a hostname hash
    #         hostname = "kcrhost1234" # Assume the hostname or identifier is the first argument
    #         queue_name = f"queue_{hostname[:8]}"  # Generate a queue name
    #         print(f'queue:' + queue_name)
    #         return {'queue': queue_name}
    #     return None


# Initialize Celery app
celery_app = CeleryAppConfig().app


