import csv
import os
from datetime import datetime


def log(filepath: str, action: str, logger_path):
    print(f'Creating a new dir for log: {logger_path}')
    if not os.path.exists(logger_path):
        os.makedirs(logger_path, exist_ok=True)

    log_file = os.path.join(logger_path, 'log.txt')
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()} - File {filepath} {action}.\n")


def log_table(rows, logger_path):
    if not os.path.exists(logger_path):
        os.makedirs(logger_path, exist_ok=True)

    log_file = os.path.join(logger_path, 'db_status.csv')
    with open(log_file, 'w') as f:
        my_file = csv.writer(f)
        my_file.writerows(rows)
