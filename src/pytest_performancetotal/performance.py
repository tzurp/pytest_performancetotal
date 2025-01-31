from datetime import datetime
import pytest
import json
import os
from pytest_performancetotal.performance_analyzer import PerformanceAnalyzer
from helpers.file_writer import FileWriter
from helpers.id_generator import IdGenerator
from pytest_performancetotal.performance_cache import PerformanceCache


class Performance:

    def __init__(self, request: pytest.FixtureRequest):
        self.request = request
        self.no_append = request.config.getoption("--performance-noappend", False)
        self.drop_results_for_failed = request.config.getoption("--performance-drop-failed-results", False)
        self.recent_days = request.config.getoption("--performance-recent-days", 0)
        self.performance_results_directory_name = request.config.getoption("--performance-results-dir", "performance_results")
        self.performance_results_file_name = request.config.getoption("--performance-results-file", "results")
        self.instance_id = IdGenerator().get_id("inst")
        self.performance_cache = PerformanceCache()
        self.log_file_name = "performance-log.txt"

    def sample_start(self, stepName: str) -> None:
        self.performance_cache.sample_start(stepName, self.instance_id)

    def sample_end(self, stepName: str) -> None:
        self.performance_cache.sample_end(stepName, self.instance_id)

    def get_sample_time(self, stepName: str) -> int:
        return self.performance_cache.get_sample_time(stepName)

    def initialize(self) -> None:
        """Don't use this method directly."""
        global performancetotal_results_dir_path
        resultsDirPath = ""
        root_dir = self.request.config.rootdir
        file_writer = FileWriter()
        if "performancetotal_results_dir_path" in globals():
            resultsDirPath = performancetotal_results_dir_path
        else:
            resultsDirPath = file_writer.create_results_dir_if_not_exist(
                root_dir, self.performance_results_directory_name
            )
            performancetotal_results_dir_path = resultsDirPath
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        init_obj = json.dumps(
            {"start_display_time": local_time, "instance_id": self.instance_id}
        )
        file_name = os.path.join(resultsDirPath, self.log_file_name)
        if self.no_append:
            file_writer.write_to_file(file_name, f"{init_obj}\n")
        else:
            file_writer.append_line_to_file(file_name, f"{init_obj}\n")

    def finalize_test(self) -> None:
        """Don't use this method directly."""
        global performancetotal_results_dir_path
        test_passed = hasattr(self.request.node, "rep_call") and self.request.node.rep_call.passed
        self.performance_cache.flush(
            FileWriter().get_file_path(
                performancetotal_results_dir_path, self.log_file_name
            ),
            test_passed,
        )

    def analyze_results(self) -> None:
        """Don't use this method directly."""
        analyzer = PerformanceAnalyzer()
        file_writer = FileWriter()
        results_dir = performancetotal_results_dir_path
        log_file_name = file_writer.get_file_path(results_dir, self.log_file_name)
        save_data_file_path = file_writer.get_file_path(results_dir, self.performance_results_file_name)
        analyzer.analyze(log_file_name, save_data_file_path, self.drop_results_for_failed, self.recent_days)
