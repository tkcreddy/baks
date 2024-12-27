
import asyncio
import argparse
from utils.kafka.producer_kafka import Producer
from utils.ReadConfig import ReadConfig as rc
from utils.server_side.SsOsSystemCmd import SsOsSystemCmd as ss
from logpkg.log_kcld import LogKCld,log_to_file
logger=LogKCld()
from utils.aws.aws_interface import AwsInterface
def main() ->None:
    read_config = rc("/Users/krishnareddy/PycharmProjects/kobraCldSS")
    instance_type = "t2.micro"
    ami_id = "ami-02d3fd86e6a2f5122"
    key_name = "NEW_KCR"
    security_group_ids = ["sg-09ac434d5bead2ab1"]
    aws_config = read_config.aws_config
    print(f"print {aws_config}")
    awsinterface = AwsInterface(aws_config['aws_access_key_id'], aws_config['aws_secret_access_key'], aws_config['region'])
    awsinterface.create_ec2_instance(instance_type, ami_id, key_name, security_group_ids)

if __name__ == '__main__':


    instance_type = "t2.micro"
    ami_id = "ami-02d3fd86e6a2f5122"
    key_name = "NEW_KCR"
    security_group_ids = ["sg-09ac434d5bead2ab1"]
    main()