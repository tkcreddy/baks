import os

from logpkg.log_kcld import LogKCld,log_to_file
import platform
import subprocess

logger = LogKCld()


class OsMetricsCmd:

    def __init__(self,msg_json):
        self.json_obj=msg_json['Os_Metrics_Cmd']
        self.key=list(self.json_obj.keys())[0]
        self.data:dict = {}

    def get_system_info(sel)->dict:
        # Retrieve system information using 'platform' module
        system_info = {
            'System': platform.system(),
            'Node Name': platform.node(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor()

        }
        return system_info

    def get_disk_space(self):
        # Get disk space information using 'df' command and store it in a variable
        disk_space_info = subprocess.run(['df', '-h'], capture_output=True, text=True)
        return disk_space_info.stdout

    def cmd_execute(self)->dict:
        cmd=self.json_obj[self.key]

        self.data[self.key]=os.system(cmd)
        if self.data[self.key] == 0:
            self.data[self.key]={"Error cmd not executed"}
        logger.info(f"data is {self.data}")
        return self.data

    def command_execute(self, command):
        count = os.cpu_count()
        data = os.system(command)
        return data
