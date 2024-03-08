import csv
import json
from pytest_performancetotal.helpers.bcolors import bcolors
from pytest_performancetotal.helpers.calculator import Calculator
from pytest_performancetotal.helpers.dic_builder import DictBuilder
from pytest_performancetotal.helpers.file_writer import FileWriter
from pytest_performancetotal.helpers.group import Group
from entities.performance_log_entry import PerformanceLogEntry


class PerformanceAnalyzer:
    def __init__(self):
        self._performance_results = []

    def analyze(
        self,
        log_file_name,
        save_data_file_path,
        drop_results_from_failed_test,
        analyze_by_browser,
    ):
        performance_log_entries = self.deserialize_data(log_file_name)

        if drop_results_from_failed_test:
            performance_log_entries = [
                e for e in performance_log_entries if e.is_test_passed
            ]

        if not performance_log_entries:
            return

        grouped_results = Group().group_by(performance_log_entries, ["name"])

        for group_key, group_items in grouped_results.items():
            duration_list = [item['duration'] for item in group_items]
            
            avg_and_ste = Calculator().get_average_and_standard_deviation(duration_list)
            
            performance_result = (DictBuilder()
                                .add('name', group_items[0]['name'])
                                .add('br_name', 'general')
                                .add('earliest_time', group_items[0]['start_display_time'])
                                .add('latest_time', group_items[-1]['start_display_time'])
                                .add('avg_time', avg_and_ste[0])
                                .add('sem', avg_and_ste[1])
                                .add('repeats', len(duration_list))
                                .add('min_value', min(duration_list))
                                .add('max_value', max(duration_list))
                                .build())

            self._performance_results.append(performance_result)
            
        self.serialize_data(save_data_file_path)

    def serialize_data(self, save_data_file_path):
        # Serialize to JSON
        file_writer = FileWriter()
        file_writer.write_to_file(
            f"{save_data_file_path}.json", json.dumps(self._performance_results)
        )

        # Serialize to CSV
        try:
            with open(f"{save_data_file_path}.csv", mode="w", newline="") as csv_file:
                fieldnames = [
                    "name",
                    "avg_time",
                    "sem",
                    "repeats",
                    "min_value",
                    "max_value",
                    "br_name"
                ]
                
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                print(f"{bcolors.HEADER} {fieldnames}")
                
                writer.writeheader()
                
                for result in self._performance_results:
                    row = {
                            "name": result['name'],
                            "avg_time": result['avg_time'],
                            "sem": result['sem'],
                            "repeats": result['repeats'],
                            "min_value": result['min_value'],
                            "max_value": result['max_value'],
                            "br_name": result['br_name']
                        }
                    print(f"{bcolors.OKGREEN} {list(row.values())}")
                    
                    writer.writerow(row)
                    
                print(f"{bcolors.OKCYAN}pytest_performancetotal: results saved to: {save_data_file_path} {bcolors.ENDC}")
                    
        except IOError as e:
            print(
                f"pytest_performancetotal: error occurred while writing CSV file: {e}"
            )

    def deserialize_data(self, file_name: str) -> list[PerformanceLogEntry]:
        results_array = []
        try:
            text_results_array = FileWriter().read_all_lines(file_name)
            for text_result in text_results_array:
                if text_result != "":
                    performance_result = json.loads(text_result) # PerformanceLogEntry(**json.loads(text_result)) # convert dictionary to PerformanceLogEntry object
                    # print("performance_result=")
                    # print(performance_result)
                    if 'id' in performance_result:
                        results_array.append(performance_result)
        except Exception as e:
            print(
                f"pytest_performancetotal: An error occurred while reading file {file_name}: {e}"
            )
        return results_array
