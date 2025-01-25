from celery import Celery
from kombu import Queue,Exchange
from hashlib import sha256
from socket import gethostname
from utils.extensions.utilities_extention import UtilitiesExtension
from utils.ReadConfig import ReadConfig as rc


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
        secure_exchange = Exchange('secure_exchange', type='direct')
        hostname = gethostname()

        read_config=rc()
        key=read_config.encryption_config['key']
        encode_util = UtilitiesExtension(key)
        print(f'Key is {key}')
       # encode_hostname=encode_util.encode_hostname_with_key(hostname)


        # Generate the dynamic queue name
        #dynamic_queue_name = generate_queue_name(hostname)
        health_check_queue_name = encode_util.encode_hostname_with_key('health_check')



        #
        # # Optionally configure a default route
        # self.app.conf.task_routes = {
        #     'tasks.utils.celery.health_check.tasks.health_check_task': {'queue': health_check_queue_name, 'routing_key': health_check_queue_name},
        #     'tasks.utils.celery.aws.tasks.get_ec2_instances': {'queue': aws_interface_queue_name, 'routing_key': aws_interface_queue_name },
        # }

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
                    'task': 'utils.celery.tasks.health_check_tasks.health_check_task',
                    'schedule': 5.0,
                    'args': [url_list],
                    'options': {
                        'queue': health_check_queue_name,
                        'exchange': secure_exchange,
                        'routing_key': health_check_queue_name,
                        'delivery_mode': 2,
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


