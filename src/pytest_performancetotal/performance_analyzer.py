import csv
import json
from helpers.bcolors import Bcolors
from helpers.calculator import Calculator
from helpers.dic_builder import DictBuilder
from helpers.file_writer import FileWriter
from helpers.group import Group
from helpers.table_printer import print_dict_as_table

class PerformanceAnalyzer:
    def __init__(self):
        self._performance_results = []

    def analyze(
        self, log_file_name, save_data_file_path, drop_results_from_failed_test
    ):
        performance_log_entries = self.deserialize_data(log_file_name)
        if drop_results_from_failed_test:
            performance_log_entries = [
                e for e in performance_log_entries if e["is_test_passed"]
            ]
        if not performance_log_entries:
            return
        grouped_results = Group().group_by(performance_log_entries, ["name"])
        for group_key, group_items in grouped_results.items():
            duration_list = [item["duration"] for item in group_items]
            avg_and_ste = Calculator().get_average_and_standard_deviation(duration_list)
            performance_result = (
                DictBuilder()
                .add("name", group_items[0]["name"])
                .add("earliest_time", group_items[0]["start_display_time"])
                .add("latest_time", group_items[-1]["start_display_time"])
                .add("avg_time", avg_and_ste[0])
                .add("sem", avg_and_ste[1])
                .add("repeats", len(duration_list))
                .add("min_value", min(duration_list))
                .add("max_value", max(duration_list))
                .build()
            )
            self._performance_results.append(performance_result)
        self.serialize_data(save_data_file_path)

    def serialize_data(self, save_data_file_path):
        # Print to the cli
        printed_keys = {'name', 'avg_time', 'sem', 'repeats', 'min_value', 'max_value'}
        printed_data = [{k: d[k] for k in printed_keys if k in d} for d in self._performance_results]
        print_dict_as_table(printed_data)
        
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
                    "earliest_time",
                    "latest_time"
                ]

                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                for result in self._performance_results:
                    row = {
                        "name": result["name"],
                        "avg_time": result["avg_time"],
                        "sem": result["sem"],
                        "repeats": result["repeats"],
                        "min_value": result["min_value"],
                        "max_value": result["max_value"],
                        "earliest_time":result["earliest_time"],
                        "latest_time":result["latest_time"]
                    }
                    csv_writer.writerow(row)
                print(
                    f"{Bcolors.OKCYAN}pytest_performancetotal: results saved to: {save_data_file_path} {Bcolors.ENDC}"
                )
        except IOError as e:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal: error occurred while writing to the CSV file: {e} {Bcolors.ENDC}"
            )

    def deserialize_data(self, file_name: str):
        results_array = []
        try:
            text_results_array = FileWriter().read_all_lines(file_name)
            for text_result in text_results_array:
                if text_result != "":
                    performance_result = json.loads(text_result)

                    if "id" in performance_result:
                        results_array.append(performance_result)
        except Exception as e:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal: error occurred while reading file {file_name}: {e} {Bcolors.ENDC}"
            )
        return results_array
