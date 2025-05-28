from src_logs_Generator import randomLogs as randomLogs
import os
import configparser

def gererate_random_logFile(num_entries: int = None, filePath: str = None):
    """
    Generate a random log file with a given number of entries.

    Args:
        num_entries (int, optional): Number of log entries to generate.
        filePath (str, optional): Path to save the generated file.
    """

    logs:list[str] = randomLogs.Logsfile(num_entries).__str__()
    write_log_to_file(logs, filePath)

def write_log_to_file(logs: list[str], filePath: str= None):
        """
        Writes the log entries to a CSV file.

        Args:
            log_entries (list[str]): List of log entries.
            filePath (str): Name of the file to write to.

        Raises:
            ValueError: If file path is not provided or not found in config.
        """
        
        if not filePath:
            config = configparser.ConfigParser()
            config.read(os.path.join("src", "data", "config.ini"))
            filePath = config.get('Settings', 'file_path', fallback=None)           
            if not filePath:
                raise ValueError("logs File path is not provided and could not be read from config.")
        filePath = os.path.abspath(os.path.normpath(filePath))
        with open(filePath, 'w', newline='') as file:
            for log in logs:
                file.write(log + '\n')