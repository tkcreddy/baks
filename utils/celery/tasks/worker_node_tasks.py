from utils.celery.celery_config import celery_app
from utils.aws.aws_interface import AwsInterface
from utils.os.os_interface import *
from logpkg.log_kcld import LogKCld, log_to_file

logger = LogKCld()


@celery_app.task
@log_to_file(logger)
def get_worker_node_info():
    response_data = ""

    try:
        response_data = get_system_info()
        # return respose_data
    except Exception as err:
        print(f"erroring with {err}")
    finally:
        return response_data



