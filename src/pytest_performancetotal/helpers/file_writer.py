import os
from typing import List, TextIO
import time

class FileWriter:

    timeout = 0
    
    def __init__(self):
        self.timeout = 5

    def wait_write_available(self, path: str, mode: int):
        start_time = time.time()

        while True:
            if os.path.exists(path) and os.access(path, mode):
                break
            elif time.time() - start_time > self.timeout:
                print(f"pytest_performancetotal warning: '{self.file_name}' is not writable after {self.timeout} seconds.")
                break
            else:
                time.sleep(1)
                

    def read_all_lines(self, path: str) -> List[str]:
        data = ""
        try:
            self.wait_write_available(path, os.R_OK)
            file: TextIO = open(path, "r")
            data = file.read()
        except Exception as err:
            print(f"pytest_performancetotal warning: Failed to read file {path}: {err}")
        finally: file.close()
        
        stringArray = data.splitlines()

        return stringArray
  

    def write_to_file(self, path: str, data: str) -> None: 
        try:
            file: TextIO = open(path, "w")
            file.write(data)
        except Exception as err:
            print(f"pytest_performancetotal error: '{path}' is not writeable: {err}")
        finally:
            file.close()

    def append_line_to_file(self, path: str, data: str) -> None:
        try:
            file: TextIO = open(path, "a")
            file.write(data)
        except Exception as err:
            print(f"pytest_performancetotal warning: file '{path}' is not writable (append): {err}")
        finally:
            file.close()
           
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
      except Exception as err:
        print(f"pytest_performancetotal warning: can't create directory '{dir_path}': {err}")
        