import hashlib
import boto3
from celery_config import app

# Helper function to generate a queue name
def generate_dynamic_queue_name(identifier):
    hash_value = int(hashlib.md5(identifier.encode()).hexdigest(), 16)
    return f"dynamic_queue_{hash_value % 1000}"  # Modulus to limit queue count

# Define the task
@app.task
def create_instance(instance_type, key_name, security_group, ami_id, region):
    ec2 = boto3.client('ec2', region_name=region)
    try:
        response = ec2.run_instances(
            InstanceType=instance_type,
            KeyName=key_name,
            SecurityGroups=[security_group],
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
        )
        instance_id = response['Instances'][0]['InstanceId']
        return f"Instance {instance_id} created successfully."
    except Exception as e:
        return f"Failed to create instance: {e}"
