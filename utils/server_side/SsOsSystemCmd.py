import json
from utils.CommandConfig import CommandConfig

class SsOsSystemCmd:
    def __init__(self):
        self.cmdconf = CommandConfig()
        self.json ={"Os_System_Cmd":{}}

    def get_cpu_info(self):
        self.json['Os_System_Cmd'] = {"get_cpu_info": self.cmdconf.os_system_cmd['get_cpu_info']}
        return self.json
    def get_system_info(self):
        self.json['Os_System_Cmd'] = {"get_system_info": self.cmdconf.os_system_cmd['get_system_info']}
        return self.json