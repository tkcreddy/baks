import logging
import boto3
import time
from logpkg.log_kcld import LogKCld, log_to_file
from utils.ReadConfig import ReadConfig as rc
from utils.singleton import Singleton
logger = LogKCld()

class AwsInterface:
    @log_to_file(logger)
    def __init__(self, aws_access_key_id, aws_secret_access_key,region_name):
        try:
            self.session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=region_name)
            self.ec2_client = self.session.client('ec2')
        except Exception as err:
            logging.error(f"Exception initializing AWS Interface "f" {err}")
            raise
    @log_to_file(logger)
    def create_ec2_instance(self,instance_type, ami_id, key_name, security_group_ids):
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
            MinCount=1,
            MaxCount=1
        )

        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance created with ID: {instance_id}")

