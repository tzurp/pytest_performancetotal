from helpers.bcolors import Bcolors
from helpers.logger import Logger


def print_dict_as_table(dict_list):
    logger = Logger()
    if not dict_list or not all(isinstance(d, dict) for d in dict_list):
        return
    else:
        logger.info("pytest_performancetotal results:")
    headers = dict_list[0].keys()
    column_widths = {key: max(len(str(key)), max(len(str(d.get(key, ''))) for d in dict_list)) for key in headers}
    header_row = " | ".join(f"{key:{column_widths[key]}}" for key in headers)
    separator = "-+-".join('-' * column_widths[key] for key in headers)
    logger.info(f"{Bcolors.HEADER} {header_row}")
    logger.info(separator)
    for d in dict_list:
        row = " | ".join(f"{str(d.get(key, '')):{column_widths[key]}}" for key in headers)
        logger.info(f"{Bcolors.OKCYAN} {row} {Bcolors.ENDC}")