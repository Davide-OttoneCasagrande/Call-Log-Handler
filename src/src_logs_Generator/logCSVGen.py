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
        timestamp = current_hour - timedelta(hours=i * int(configs["delta_T_for_file"]))
        random_single_logFile(timestamp, timedelta(hours=1), file_path)

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
    def require_config_key(section: str, key: str, fallback=None) -> str:
        """
        Helper function to ensure a config key exists and is not empty.
        """
        value = config.get(section, key, fallback=fallback)
        if not value:
            raise ValueError(f"missing required config value: [{section}]{key}.")
        return value
    
    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    config = ConfigParser()
    config.read(config_path)

    folder_path = require_config_key('Settings', 'folder_path')
    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"The specified folder path is not a directory: {folder}")
    delta_T_for_file = require_config_key('Settings', 'delta_T_for_file', 1)
    return {
        "folder_path": str(folder),
        "delta_T_for_file": delta_T_for_file
    }

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
    with open(full_path, 'w', newline='') as file:
        for log in log_collection.logs:
            file.write(log + '\n')

if __name__ == "__main__":
    # Entry point for generating random log files.
    generate_random_log_files()
    print("Logs generation completed.")