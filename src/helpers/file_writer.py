import os
from typing import List
from filelock import FileLock
from helpers.bcolors import Bcolors


class FileWriter:

    def get_file_lock(self, data_file_path):
        lock_file_path = f"{data_file_path}.lock"
        return FileLock(lock_file_path)

    def read_all_lines(self, path: str) -> List[str]:
        lock = self.get_file_lock(path)
        try:
            with lock:
                with open(path, "r") as file:
                    data = file.read()
        except OSError as err:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal: failed to read file {path}: {err} {Bcolors.ENDC}"
            )
            return []
        return data.splitlines()

    def write_to_file(self, path: str, data: str) -> None:
        lock = self.get_file_lock(path)
        try:
            with lock:
                with open(path, "w") as file:
                    file.write(data)
        except OSError as err:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal error: '{path}' is not writable: {err} {Bcolors.ENDC}"
            )

    def append_line_to_file(self, path: str, data: str) -> None:
        lock = self.get_file_lock(path)
        try:
            with lock:
                with open(path, "a") as file:
                    file.write(data + "\n")
        except OSError as err:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal error: file '{path}' is not writable (append): {err} {Bcolors.ENDC}"
            )

    def get_file_path(self, results_dir: str, file_name: str) -> str:
        path = os.path.join(results_dir, file_name)
        return path

    def create_results_dir_if_not_exist(self, root_dir, results_dirname) -> str:
        dir_path = os.path.join(str(root_dir), results_dirname)
        is_file_exists = self.is_file_exist(dir_path)
        if not is_file_exists:
            self.make_dir(dir_path)
        return dir_path

    def is_file_exist(self, dir_path: str) -> bool:
        return os.path.exists(dir_path)

    def make_dir(self, dir_path: str) -> None:
        try:
            os.mkdir(dir_path)
        except OSError as err:
            print(
                f"{Bcolors.WARNING}pytest_performancetotal: can't create directory '{dir_path}': {err} {Bcolors.ENDC}"
            )
