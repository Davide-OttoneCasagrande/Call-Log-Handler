from configparser import ConfigParser
from pathlib import Path
import loader
import dataStore

def main( length_between_logging:int = 100):
    """
    Executes the log collection and export pipeline.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Iterates through each log and stores it using the DataStore module.
    4. Logs progress every `length_between_logging` entries.

    Args:
        length_between_logging (int): Number of logs to process before logging progress.
            Default is 100.
    """

    config:dict = load_config()
    files = loader.CallLogLoader(config["folder_path"])
    db = dataStore.DataStore(config["export_file_path"])
    
    print("Starting pipeline...")
    logs_since_last_log:int = 0
    log_batches_completed:int = 0
    for row in files.load_csv_files():
        db.insert(row.to_json())
        logs_since_last_log+= 1
        if logs_since_last_log==length_between_logging:
            print(f"{log_batches_completed*length_between_logging:} logs processed, continuing...")
            log_batches_completed += 1
            logs_since_last_log = 0
    print("Log collection successfully exported.")
    
def load_config() -> dict[str, str]:
    """
    Loads and validates configuration settings from the config.ini file.

    Returns:
        dict: A dictionary containing validated configuration values:
            - folder_path (str): Path to the folder containing log CSV files.
            - export_file_path (str): Path to the output JSON file.

    Raises:
        FileNotFoundError: If the config file or required CSV files are missing.
        ValueError: If required config values are missing.
        NotADirectoryError: If the folder path is not a valid directory.
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

    if not any(folder.glob("*.csv")):
        raise FileNotFoundError(f"No CSV files found in the specified folder: {folder}")

    export_file_path = (config.get('Settings', 'export_file_path', fallback=None))
    if not export_file_path:
        raise ValueError("Export file path is not provided in the config file.")
    return {
    "folder_path": str(folder),
    "export_file_path": str(Path(export_file_path).resolve())
    }

if __name__ == "__main__":
    main()