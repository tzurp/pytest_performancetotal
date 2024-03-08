from enum import Enum

class StepType(Enum):
    START = 1
    END = 2

class PartialLogEntry:
    def __init__(self):
        self.name = ""
        self.id = ""
        self.type = StepType.START
        self.time = 0
        self.display_time = ""
        self.instance_id = ""
        self.br_name = ""
