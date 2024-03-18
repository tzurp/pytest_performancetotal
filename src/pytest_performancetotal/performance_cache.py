from datetime import datetime
import json
from entities.partial_log_entry import PartialLogEntry, StepType
from entities.performance_log_entry import PerformanceLogEntry
from helpers.file_writer import FileWriter
from helpers.id_generator import IdGenerator
from consts.constants import constant_vars


class PerformanceCache:
    def __init__(self):
        self._start_log_entries = []
        self._end_log_entries = []
        self._performance_entries = []

    def sample_start(self, step_name, instance_id):
        log_entry = self.set_sample(StepType.START, step_name, instance_id)
        self._start_log_entries.insert(0, log_entry)

    def sample_end(self, step_name, instance_id):
        log_entry = self.set_sample(StepType.END, step_name, instance_id)
        self._end_log_entries.append(log_entry)

    def get_sample_time(self, step_name):
        return self.get_performance_entry_time(step_name)

    def flush(self, file_name, is_test_passed):
        self.create_performance_entries(is_test_passed)
        self.write_performance_data_to_file(file_name)

    def set_sample(self, step_type, step_name, instance_id):
        id = ""
        log_entry = PartialLogEntry()

        if step_type == StepType.START:
            id = IdGenerator().get_id()
        else:
            id = self.get_start_id_by_step_name(step_name, instance_id)

        log_entry.id = id
        log_entry.instance_id = instance_id
        log_entry.name = step_name
        log_entry.type = step_type
        log_entry.time = int(datetime.now().timestamp() * 1000)
        log_entry.display_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return log_entry

    def get_performance_entry_time(self, step_name):
        duration = 0
        start_entry = next(
            (
                e
                for e in self._start_log_entries
                if e.name == step_name + constant_vars["step_suffix_used"]
            ),
            None,
        )
        if start_entry:
            end_entry = next(
                (e for e in self._end_log_entries if e.id == start_entry.id), None
            )
            if end_entry:
                duration = end_entry.time - start_entry.time
        return duration

    def create_performance_entries(self, is_test_passed):
        rev_start_entries = list(reversed(self._start_log_entries))
        for start_entry in rev_start_entries:
            temp_performance_entry = PerformanceLogEntry()
            corresponded_end_entry = next(
                (e for e in self._end_log_entries if e.id == start_entry.id), None
            )
            if corresponded_end_entry:
                temp_performance_entry.id = start_entry.id
                temp_performance_entry.instance_id = start_entry.instance_id
                temp_performance_entry.name = corresponded_end_entry.name
                temp_performance_entry.start_display_time = start_entry.display_time
                temp_performance_entry.start_time = start_entry.time
                temp_performance_entry.end_time = corresponded_end_entry.time
                temp_performance_entry.duration = temp_performance_entry.get_duration()
                temp_performance_entry.is_test_passed = is_test_passed
                self._performance_entries.append(temp_performance_entry)
    def get_start_id_by_step_name(self, step_name: str, instance_id: str) -> str:
        id = ""
        start_entry = next(
            (
                e
                for e in self._start_log_entries
                if e.name == step_name and e.instance_id == instance_id
            ),
            None,
        )
        if start_entry:
            id = start_entry.id
        else:
            return
        start_entry.name += constant_vars.get("step_suffix_used")
        return id

    def clear_data(self) -> None:
        self._start_log_entries = []
        self._end_log_entries = []
        self._performance_entries = []

    def write_performance_data_to_file(self, file_name: str) -> None:
        for performance_entry in self._performance_entries:
            FileWriter().append_line_to_file(
                file_name, f"{json.dumps(performance_entry.__dict__)}\n"
            )
        self.clear_data()
