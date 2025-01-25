from utils.ReadConfig import ReadConfig as rc
from logpkg.log_kcld import LogKCld
from utils.celery.celery_config import celery_app
from utils.extensions.utilities_extention import UtilitiesExtension
from kombu import Queue,Exchange
import time
logger = LogKCld()
from utils.celery.aws.tasks import get_ec2_instances,create_worker_nodes,terminate_worker_node

def main():
    read_config = rc()
    # instance_type = "t2.micro"
    # ami_id = "ami-02d3fd86e6a2f5122"
    # key_name = "NEW_KCR"
    # security_group_ids = ["sg-09ac434d5bead2ab1"]
    key_read=read_config.encryption_config
    secure_exchange = Exchange('secure_exchange', type='direct')
    aws_config = read_config.aws_config
    ue=UtilitiesExtension(key_read['key'])
    print(f"print {aws_config}")
    aws_interface_queue_name=ue.encode_hostname_with_key('aws_interface')
    #result=get_ec2_instances.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'])
    result=get_ec2_instances.apply_async(
        args=(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region']),
        exchange=secure_exchange,
        queue=aws_interface_queue_name,
        routing_key=aws_interface_queue_name,
        delivery_mode=2,  # Persistent messages
    )
    print("Task sent. Waiting for result...")
    print(result.get(timeout=30))
    #result = create_worker_nodes.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],instance_type,ami_id,key_name,security_group_ids)
    #print("Task sent. Waiting for result...")
    #response= result.get(timeout=30)
    #instance = response['Instances'][0]['InstanceId']
    #print(instance)
    #time.sleep(50)
    #result = terminate_worker_node.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],[instance])
    #response = result.get(timeout=30)
    #print(str(response))




    #awsiface = AwsInterface(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'])
    # awsiface.create_ec2_instance(instance_type, ami_id, key_name, security_group_ids)
    # print("checking the version")
    # awsiface.get_ec2_info()
    #ec2_instances = awsiface.get_ec2s_information()
    #print(aws_iface_data)
    # instance_ids_to_terminate = ['i-0601632618a211983', 'i-04d7bdc645e572aec']  # Replace with your instance IDs
    # response=awsiface.terminate_ec2_instances(instance_ids_to_terminate)
    # Terminate instances
    # response =  aws terminate_ec2_instances(instance_ids_to_terminate)

    # Print the response
    # print(response)


if __name__ == '__main__':
    instance_type = "t2.micro"
    ami_id = "ami-02d3fd86e6a2f5122"
    key_name = "NEW_KCR"
    security_group_ids = ["sg-09ac434d5bead2ab1"]
    main()
