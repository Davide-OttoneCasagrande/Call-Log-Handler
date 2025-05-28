import configparser
import os
import Loader as loader
import CallLog as callLog
import ToDataStore as toDataStore # TODO implement IToDataStore as ToDataStore elsewhere

def logCollector( file_path: str = None):
    """
    Collect logs and send them to the data store.

    Args:
        file_path (str, optional): Path to the log file. If not provided, read from config.
    """

    logs: list[dict] = []
    logs = _initializeLogs(file_path)
    logStrings:list[str] = __json__(logs)
    toDataStore.ToDataStore.insert(logStrings) # TODO implement IToDataStore as ToDataStore elsewhere

def _initializeLogs(file_path: str = None)-> list[callLog.CallLog]:
    """
    Load and parse logs from a CSV file.

    Args:
        file_path (str, optional): Path to the log file.

    Returns:
        list[CallLog]: Parsed call logs.

    Raises:
        ValueError: If path is missing or no logs found.
        FileNotFoundError: If file does not exist.
    """

    if not file_path:
        config = configparser.ConfigParser()
        config.read(os.path.join("src", "data", "config.ini"))
        file_path = config.get('Settings', 'file_path', fallback=None)           
        if not file_path:
            raise ValueError("logs File path is not provided and could not be read from config.")
    
    file_path = os.path.abspath(os.path.normpath(file_path))
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found at the specified path: {file_path}")
    
    logs: list = loader.CSVLoader(file_path)
    if not logs:
        raise ValueError("No logs found in the provided file path.")
    
    return logs

def __json__(logs:list[callLog.CallLog]) -> list[dict]:
    """
    Convert logs to a list of JSON-serializable dictionaries.

    Args:
        logs (list[CallLog]): List of call logs.

    Returns:
        list[dict]: JSON-serializable logs.
    """

    return [log.__json__() for log in logs]
    
if __name__ == "__main__":
    """
    Run the log collector using default or configured file path.
    """
    logCollector()