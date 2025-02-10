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


# @celery_app.task
# @log_to_file(logger)
# def create_worker_nodes(aws_access_key: str = None, aws_secret_key: str = None, region: str = None,
#                         instance_type: str = None, ami_id: str = None, key_name: str = None,
#                         security_group_ids: list = None, namespace:str=None,**kwargs):
#     response_data = ""
#     try:
#         aws_interface = AwsInterface(aws_access_key, aws_secret_key, region)
#         response_data = aws_interface.create_ec2_instance(instance_type, ami_id, key_name, security_group_ids,namespace, **kwargs)
#     except Exception as err:
#         print(f"erroring with {err}")
#     finally:
#         return response_data


