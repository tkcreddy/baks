from utils.ReadConfig import ReadConfig as rc
from logpkg.log_kcld import LogKCld
import time
logger = LogKCld()
from utils.celery.aws import get_ec2_instances,create_worker_nodes,terminate_worker_node

def main():
    read_config = rc("/Users/krishnareddy/PycharmProjects/kobraCldSS")
    # instance_type = "t2.micro"
    # ami_id = "ami-02d3fd86e6a2f5122"
    # key_name = "NEW_KCR"
    # security_group_ids = ["sg-09ac434d5bead2ab1"]
    aws_config = read_config.aws_config
    print(f"print {aws_config}")
    # result=get_ec2_instances.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'])
    # print("Task sent. Waiting for result...")
    # print(result.get(timeout=30))
    result = create_worker_nodes.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],instance_type,ami_id,key_name,security_group_ids)
    print("Task sent. Waiting for result...")
    response= result.get(timeout=30)
    instance = response['Instances'][0]['InstanceId']
    print(instance)
    time.sleep(50)
    result = terminate_worker_node.delay(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'],[instance])
    response = result.get(timeout=30)
    print(str(response))




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
