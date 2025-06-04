from datetime import datetime, timedelta
from configparser import ConfigParser
from pathlib import Path
import randomLogs
import random

def generate_random_log_files():
    """
    Generate multiple random log files with synthetic call log entries.

    The number of files is randomly chosen between 12 and 48.
    Each file represents logs for one hour, starting from the current hour
    and going backwards in time based on the configured delta.
    """
    configs = load_config()
    file_path = configs["folder_path"]
    number_of_files = random.randint(12, 48)
    current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
    deltaT = datetime.now().replace(microsecond=0) - current_hour

    # Generate logs for the current partial hour
    random_single_logFile(current_hour, deltaT, file_path)

    # Generate logs for previous full hours
    for i in range(number_of_files):
        timestamp = current_hour - timedelta(hours=i * configs["delta_T_for_file"])
        random_single_logFile(timestamp, timedelta(hours=1), file_path)

def random_single_logFile(starting_hour: datetime, deltaT: timedelta, file_path: str):
    """
    Generate a single log file for a given time range.

    Args:
        starting_hour (datetime): The start time of the log file.
        deltaT (timedelta): Duration of the log entries.
        file_path (str): Directory where the log file will be saved.
    """
    file_name = f"{starting_hour.strftime('%Y-%m-%dT%H.00')}_logs.csv"
    log_collection = randomLogs.Logsfile(starting_hour, deltaT)
    full_path = Path(file_path) / file_name
    write_log_to_file(log_collection.logs, str(full_path))

def write_log_to_file(logs: list[str], file_path: str):
    """
    Write log entries to a CSV file.

    Args:
        logs (list[str]): List of log entry strings.
        file_path (str): Full path to the output CSV file.
    """
    with open(file_path, 'w', newline='') as file:
        for log in logs:
            file.write(log + '\n')

def load_config() -> dict:
    """
    Load and validate configuration settings from the config.ini file.

    Returns:
        dict: A dictionary containing:
            - folder_path (str): Path to the folder for log files.
            - delta_T_for_file (int): Time delta (in hours) between log files.

    Raises:
        FileNotFoundError: If the config file is missing.
        ValueError: If required config values are missing.
        NotADirectoryError: If the folder path is invalid.
    """
    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    config = ConfigParser()
    config.read(config_path)

    folder_path = config.get('Settings', 'folder_path', fallback=None)
    if not folder_path:
        raise ValueError("Folder path is not provided in the config file.")

    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"The specified folder path is not a directory: {folder}")

    delta_T_for_file = config.getint('Settings', 'delta_T_for_file', fallback=1)
    return {
        "folder_path": str(folder),
        "delta_T_for_file": delta_T_for_file
    }

if __name__ == "__main__":
    # Entry point for generating random log files.
    generate_random_log_files()
    print("Logs generation completed.")