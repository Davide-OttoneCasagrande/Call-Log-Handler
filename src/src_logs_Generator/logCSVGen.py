from datetime import datetime, timedelta
from configparser import ConfigParser
from pathlib import Path
import randomLogs
import logging
import random
import sys


def setup_logging(log_path: str) -> None:
    """Configure logging with proper formatting and handlers."""
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


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
    logging.debug(
        f"Generating {number_of_files} log files starting from {current_hour}.")
    random_single_logFile(current_hour, deltaT, file_path)
    # Generate logs for previous full hours
    for i in range(number_of_files):
        timestamp = current_hour - \
            timedelta(hours=i * int(configs["delta_T_for_file"]))
        random_single_logFile(timestamp, timedelta(hours=1), file_path)
    logging.info("Logs generation completed.")


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
    def get_required_config(parser: ConfigParser, section: str, key: str, fallback=None) -> str:
        """Get required configuration value or raise ValueError."""
        value = parser.get(section, key, fallback=fallback)
        if not value or not value.strip():
            error_msg: str = f"Missing required configuration: [{section}] {key}"
            logging.critical(error_msg)
            raise ValueError(error_msg)
        return value.strip()

    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        error_msg: str = f"Config file not found at: {config_path}"
        logging.critical(error_msg)
        raise FileNotFoundError(error_msg)

    parser = ConfigParser()
    parser.read(config_path)

    folder_path = get_required_config(parser, 'generator', 'folder_path')
    folder = Path(folder_path).resolve()
    if not folder.is_dir():
        error_msg: str = f"The specified folder path is not a directory: {folder}"
        logging.critical(error_msg)
        raise NotADirectoryError()

    delta_T_for_file = get_required_config(
        parser, 'generator', 'delta_T_for_file', 1)

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
    logging.debug(f"Generated log file: {full_path}")


if __name__ == "__main__":
    # Entry point for generating random log files.
    setup_logging("src/logs/generator.log")
    try:
        generate_random_log_files()
    except Exception as e:
        error_message: str = f"file random generation failed: {e}"
        logging.error(error_message, exc_info=True)
        sys.exit(1)
