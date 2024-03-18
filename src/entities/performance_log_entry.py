from dataclasses import dataclass

@dataclass(init=False)
class PerformanceLogEntry:
    name: str
    id: str
    instance_id: str
    start_time: int
    end_time: int
    start_display_time: str
    duration: int
    is_test_passed: bool
    instance_id: str

    def __init__(self):
        self.name = ""
        self.id = ""
        self.instance_id = ""
        self.start_time = 0
        self.end_time = 0
        self.start_display_time = ""
        self.duration = 0
        self.is_test_passed = True
        self.instance_id = ""


    def get_duration(self) -> int:
        return self.end_time - self.start_time