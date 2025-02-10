import os

from logpkg.log_kcld import LogKCld,log_to_file
import platform
import subprocess
import socket
logger = LogKCld()


@log_to_file(logger)
def get_disk_space():
    # Get disk space information using 'df' command and store it in a variable
    disk_space_info = subprocess.run(['df', '-h'], capture_output=True, text=True)
    return disk_space_info.stdout


@log_to_file(logger)
def get_system_info() -> dict:
    return {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
    }


@log_to_file(logger)
def command_execute(command):
    count = os.cpu_count()
    return os.system(command)


def hostname(self):
    self.host=socket.gethostname()
    return  self.host

def hostip(self):
    self.ip=socket.gethostbyname(socket.gethostname())
    return self.ip

def hoststring(self):
    self.host_data= ''.join([self.host, self.ip])
    return self.host_data

def host_string(self):
    self.host_data= '_'.join([self.host, self.ip])
    return self.host_data

class OsMetricsCmd:

    def __init__(self,msg_json):
        self.json_obj=msg_json['Os_Metrics_Cmd']
        self.key=list(self.json_obj.keys())[0]
        self.data:dict = {}

    def cmd_execute(self)->dict:
        cmd=self.json_obj[self.key]

        self.data[self.key]=os.system(cmd)
        if self.data[self.key] == 0:
            self.data[self.key]={"Error cmd not executed"}
        logger.info(f"data is {self.data}")
        return self.data
