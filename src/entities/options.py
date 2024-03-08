from typing import NamedTuple

class Options(NamedTuple):
    disable_append_to_existing_file: bool
    performance_results_file_name: str
    drop_results_from_failed_test: bool
    analyze_by_browser: bool
    performance_results_directory: str
