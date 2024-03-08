from datetime import datetime
import json
import os
from pytest import FixtureRequest
from pytest_performancetotal.performance_analyzer import PerformanceAnalyzer
from pytest_performancetotal.helpers.file_writer import FileWriter
from pytest_performancetotal.helpers.id_generator import IdGenerator
from pytest_performancetotal.performance_cache import PerformanceCache


class Performance:
    options = None
    instance_id = 0
    performance_cache = {}
    performance_results_directory_name = ""
    performance_results_file_name = ""
    log_file_name = ""

    def __init__(self):
        self.instance_id = IdGenerator().get_id("inst")
        self.performance_cache = PerformanceCache()
        self.performance_results_directory_name = "performance_results"
        self.log_file_name = "performance-log.txt"
        self.options = {"disable_append_to_existing_file": False, "performance_results_fileName": "performance_results"}
        #TODO: add options?

    def sampleStart(self, stepName: str) -> None:
        self.performance_cache.sample_start(stepName, self.instance_id)
    

    def sampleEnd(self, stepName: str) -> None:
        self.performance_cache.sample_end(stepName, self.instance_id)

    def getSampleTime(self, stepName: str) -> int:
        return self.performance_cache.get_sample_time(stepName)
    
    def initialize(self, root_dir) -> None:
        """Don't use this method directly.
        """
        # performancetotal_results_dir_path is a global variable
        global performancetotal_results_dir_path
        resultsDirPath = ""
        file_writer = FileWriter()
        
        if 'performancetotal_results_dir_path' in globals():
           
            resultsDirPath = performancetotal_results_dir_path
        else:
            resultsDirPath = file_writer.create_results_dir_if_not_exist(root_dir, self.performance_results_directory_name)
            performancetotal_results_dir_path = resultsDirPath
        
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        init_obj = json.dumps({ "start_display_time": local_time, "instance_id": self.instance_id })

        file_name = os.path.join(resultsDirPath, self.log_file_name);

        if self.options["disable_append_to_existing_file"] == True:
            file_writer.writeToFile(file_name, f"{init_obj}\n")
        
        else:
            file_writer.append_line_to_file(file_name, f"{init_obj}\n")
        
    def finalize_test(self, request: FixtureRequest) -> None:
        """Don't use this method directly.
        """
        global performancetotal_results_dir_path
        
        test_passed = hasattr(request.node, 'rep_call') and request.node.rep_call.passed
        
        self.performance_cache.flush(FileWriter().get_file_path(performancetotal_results_dir_path, self.log_file_name), "SomeBrowser", test_passed)
    

    def analyze_results(self, workerIndex: int) -> None:
        analyzer = PerformanceAnalyzer()
        file_writer = FileWriter()
        results_dir = performancetotal_results_dir_path
        
        log_file_name = file_writer.get_file_path(results_dir, self.log_file_name)
        
        save_data_file_path = file_writer.get_file_path(results_dir,"results")
        
        analyzer.analyze(log_file_name, save_data_file_path, False, False)
