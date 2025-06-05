from configparser import ConfigParser
from pathlib import Path
import logCollector
import loader
import dataStore

def main():
    """
    Main function to run the log collection and export process.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Collect logs using the logCollector module.
    4. Export the collected logs to a JSON file using the dataStore module.
    """

    config:dict = load_config()

    print("Collecting logs from the file system...")
    files = loader.CallLogLoader(config["folder_path"])
    collection = logCollector.LogCollector(files.callLogs)
    print("Log collection completed successfully.")
    
    print("Exporting log collection to JSON file...")
    db = dataStore.DataStore(config["export_file_path"])
    db.insert(collection.to_json__())
    print("Log collection successfully exported.")
    
def load_config() -> dict:
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