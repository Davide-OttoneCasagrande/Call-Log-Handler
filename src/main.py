from configparser import ConfigParser
from pathlib import Path
from typing import Any
import dataStore
import loader
import json

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
    db = dataStore.DataStore(config["export_path"],config["index_name"])
    if not db.index_exists:
        if config["mapping"] is None:
            raise ValueError("Mapping configuration is missing in the config file, index created empty.")
        db.create_mapping(config["mapping"])
        print(f"Index '{config['index_name']}' doesn't exists, using config mapping.")    
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
    
def load_config() -> dict[str, Any]:
    """
    Loads and validates configuration settings from the config.ini file.

    Returns:
        dict: A dictionary containing validated configuration values:
            - folder_path (str): Path to the folder containing log CSV files.
            - export_path (str): URL of the Elasticsearch instance.
            - index_name (str): Name of the Elasticsearch index.
            - mapping (dict or None): Mapping schema loaded from a JSON file, if provided.

    Raises:
        FileNotFoundError: If required files are missing.
        ValueError: If required config values are missing.
        NotADirectoryError: If the folder path is not a valid directory.
    """
    def require_config_key(section: str, key: str) -> str:
        """
        Helper function to ensure a config key exists and is not empty.
        """
        value = config.get(section, key, fallback=None)
        if not value:
            raise ValueError(f"missing required config value: [{section}]{key}.")
        return value
        
    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    config = ConfigParser()
    config.read(config_path)

    folder = Path(require_config_key('Settings', 'folder_path')).resolve()
    if not folder:
        raise ValueError("Folder path is not provided in the config file.")
    if not folder.is_dir():
        raise NotADirectoryError(f"The specified folder path is not a directory: {folder}")
    if not any(folder.glob("*.csv")):
        raise FileNotFoundError(f"No CSV files found in the specified folder: {folder}")

    export_path = require_config_key('Settings', 'export_path')    
    index_name = require_config_key('Settings', 'index_name')

    mapping = require_config_key('Settings', 'mapping')
    if mapping:
        mapping_path = Path(mapping).resolve()
        if not mapping_path.is_file():
            raise FileNotFoundError(f"Mapping file not found at: {mapping_path}")
        with open(mapping_path, "r") as f:
            mapping = json.load(f)

    return {
    "folder_path": str(folder),
    "export_path": export_path,
    "index_name": index_name,
    "mapping": mapping
    }

if __name__ == "__main__":
    main()