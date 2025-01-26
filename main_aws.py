from utils.ReadConfig import ReadConfig as rc
from logpkg.log_kcld import LogKCld
from utils.celery.celery_config import celery_app
from utils.extensions.utilities_extention import UtilitiesExtension
from kombu import Queue,Exchange
import time
logger = LogKCld()
from utils.celery.tasks.aws_tasks import get_ec2_instances,create_worker_nodes,terminate_worker_node

def main():
    read_config = rc()
    # instance_type = "t2.micro"
    # ami_id = "ami-02d3fd86e6a2f5122"
    # key_name = "NEW_KCR"
    # security_group_ids = ["sg-09ac434d5bead2ab1"]
    key_read=read_config.encryption_config
    #secure_exchange = Exchange('secure_exchange', type='direct')
    aws_config = read_config.aws_config
    ue=UtilitiesExtension(key_read['key'])
    print(f"print {aws_config}")
    #aws_interface_queue_name=
    queue_info={}
    queue_info={'exchange': Exchange('secure_exchange', type='direct'), 'queue': ue.encode_hostname_with_key('aws_interface'), 'routing_key': ue.encode_hostname_with_key('aws_interface'), 'delivery_mode': 2}

    # result=get_ec2_instances.apply_async(
    #     args=(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region']), **queue_info)
    #
    # print("Task sent. Waiting for result...")
    # print(result.get(timeout=30))
    min=2
    max=2
    cluster_key='ClusterName'
    cluster_value='Test_Cluster'
    min_max_tags={
        'MinCount':min,
        'MaxCount':max,
        'TagSpecifications':[{
            'ResourceType': 'instance',
            'Tags': [
                    {
                    'Key': cluster_key,
                    'Value': cluster_value
                    }
            ]
            }]
    }
    # result = create_worker_nodes.apply_async(args=(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],instance_type,ami_id,key_name,security_group_ids),
    #                                          kwargs=min_max_tags,**queue_info)
    # print("Task sent. Waiting for result...")
    # response= result.get(timeout=30)
    # instances=[]
    # print(min_max_tags['MaxCount'])
    # for i in range(int(min_max_tags['MaxCount'])):
    #     instances.append(response['Instances'][i]['InstanceId'])
    # print(instances)
    #time.sleep(50)
    instances=['i-07247997712a85fc7', 'i-0611d52dfc54bddec']
    result = terminate_worker_node.apply_async(args=(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],instances),**queue_info)
    response = result.get(timeout=30)

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
