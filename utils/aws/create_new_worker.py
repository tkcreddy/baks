import boto3
import logging
from utils.celery.celery_app import celery_app
from utils.ReadConfig import ReadConfig as rc
from logpkg.log_kcld import LogKCld, log_to_file
import json
logger = LogKCld()

class EC2InstanceManager:
    """
    A class to manage AWS EC2 instance creation.
    """

    @log_to_file(logger)


    def __init__(self):
        try:
            read_config = rc("/Users/krishnareddy/PycharmProjects/kobraCldSS")
            aws_config = read_config.aws_config
            self.session = boto3.Session(aws_access_key_id=aws_config['aws_access_key_id'], aws_secret_access_key=aws_config['aws_secret_access_key'],region_name=aws_config['region'])
            self.ec2_client = self.session.client('ec2')
        except Exception as err:
            logging.error(f"Exception initializing AWS Interface "f" {err}")
            raise
    @log_to_file(logger)
    def create_ec2_instance(self,instance_type, ami_id, key_name, security_group_ids,min,max) -> None:
        """
        Creates an EC2 instance using credentials loaded from a YAML file.

        Args:
            yaml_file_path (str): Path to the YAML file containing AWS credentials.
            instance_type (str): EC2 instance type (e.g., "t2.micro").
            ami_id (str): Amazon Machine Image (AMI) ID.
            key_name (str): Name of the key pair to use for access.
            security_group_ids (list): List of security group IDs.
        """

        response = self.ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroupIds=security_group_ids,
            MinCount=min,
            MaxCount=max
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance created with ID: {instance_id}")

    def create_instance(self, instance_name):
        """
        Method to create an EC2 instance.
        """
        response = self.ec2_client.run_instances(
            ImageId=self.ami_id,
            InstanceType=self.instance_type,
            KeyName=self.key_name,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': instance_name}]
                }
            ]
        )
        instance_id = response['Instances'][0]['InstanceId']
        return f"Created EC2 instance with ID: {instance_id}"


# Define a Celery task that uses the EC2InstanceManager class
@celery_app.task(name='tasks.create_ec2_instance')
def create_ec2_instance_task(instance_name):
    """
    Celery task to create an EC2 instance using EC2InstanceManager.
    """
    manager = EC2InstanceManager(
        region="us-west-2",  # Replace with your region
        ami_id="ami-12345678",  # Replace with your AMI ID
        instance_type="t2.micro",  # Replace with your instance type
        key_name="your-key-pair-name"  # Replace with your key pair
    )
    return manager.create_instance(instance_name)
