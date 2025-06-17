from datetime import datetime, timedelta
from pathlib import Path
import logging
import random
import sys
import os

import randomLogs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


log_path: str = "src/logs//app.log"
"""Configuring root logger with proper formatting and handlers."""
log_file = Path(log_path)
log_file.parent.mkdir(parents=True, exist_ok=True)

file_format = logging.Formatter("[%(levelname)s]%(asctime)s - %(name)s: %(message)s")
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(file_format)

stream_format = logging.Formatter("[%(levelname)s] - %(name)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(stream_format)

logging.basicConfig(
    level=logging.INFO,
    #datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[file_handler, stream_handler]
)

"""Set up module-level logger."""
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def generate_random_log_files():
    """
    Generate multiple random log files with synthetic call log entries.

    The number of files is randomly chosen between 12 and 48.
    Each file represents logs for one hour, starting from the current hour
    and going backwards in time based on the configured delta.
    """
    logger.info("Starting log generation process.")
    configs = config.Config("generator")

    file_path = configs.folder_path
    number_of_files = random.randint(12, 48)
    current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    deltaT = datetime.now().replace(microsecond=0) - current_hour

    # Generate logs for the current partial hour
    logger.debug(
        f"Generating {number_of_files} log files starting from {current_hour}.")
    random_single_logFile(current_hour, deltaT, file_path)
    # Generate logs for previous full hours
    for i in range(number_of_files):
        timestamp = current_hour - \
            timedelta(hours=i * int(configs.delta_T_for_file))
        timestamp = current_hour - \
            timedelta(hours=i * int(configs.delta_T_for_file))
        random_single_logFile(timestamp, timedelta(hours=1), file_path)
    logger.info("Logs generation completed.")

def random_single_logFile(starting_hour: datetime, deltaT: timedelta, file_path: str):
    """
    Generate a single log file for a given time range and write it to file.

    Args:
        starting_hour (datetime): The start time of the log file.
        deltaT (timedelta): Duration of the log entries.
        file_path (str): Directory where the log file will be saved.
    """
    file_name = f"{starting_hour.strftime('%Y-%m-%dT%H.00')}_logs.csv"
    log_collection = randomLogs.Logsfile(starting_hour, deltaT)
    full_path = Path(file_path) / file_name
    try:
        with open(full_path, 'w', newline='') as file:
            for log in log_collection.logs:
                file.write(log + '\n')
        logger.debug(f"Generated log file: {full_path}")
    except Exception as e:
        error_message: str = f"Failed to write log file {full_path}: {e}"
        logger.error(error_message, exc_info=True)


if __name__ == "__main__":
    # Entry point for generating random log files.
    try:
        generate_random_log_files()
    except Exception as e:
        error_message: str = f"file random generation failed: {e}"
        logger.critical(error_message, exc_info=True)
        sys.exit(1)
