from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional
import logging
import json
import sys

import dataStore
import loader


def setup_logging(log_path: str) -> None:
    """Configure logging with proper formatting and handlers."""
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main(length_between_logging: int = 100) -> None:
    """
    Executes the log collection and export pipeline.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Process each log and store it using the DataStore module
    4. Log progress every `length_between_logging` entries

    Args:
        length_between_logging (int): Number of logs to process before logging progress.
            Default is 100.

    Raises:
        SystemExit: If configuration loading or pipeline execution fails.
    """
    setup_logging("src/logs//app.log")
    # try:
    config: Dict = load_config()

    logging.info("Initializing log processing pipeline...")

    files = loader.CallLogLoader(config["folder_path"])
    db = dataStore.DataStore(
        config["export_path"], config["elasticsearch_address"], config["index_name"])

    if config["elasticsearch_address"] and not db.index_exists:
        if config["mapping"] is None:
            logging.warning(
                "Mapping configuration is missing in the config file, index created empty.")
        db.create_mapping(config["mapping"])
        logging.info(
            f"Index '{config['index_name']}' doesn't exists, using config mapping.")

    logging.info("Starting log processing...")
    total_processed: int = process_logs(files, db, length_between_logging)

    success_message: str = f"Successfully processed {total_processed} logs"
    logging.info(success_message)

    # except Exception as e:
    #    error_message: str = f"Pipeline failed: {e}"
    #    logging.critical(error_message, exc_info=True)
    #    sys.exit(1)


def process_logs(files: loader.CallLogLoader, db: dataStore.DataStore, batch_size: int) -> int:
    """
    Process and insert logs into the database.

    Args:
        files: CallLogLoader instance for reading CSV files
        db: DataStore instance for database operations
        batch_size: Number of logs to process before logging progress

    Returns:
        Total number of logs processed
    """
    logs_processed = 0
    batch_count = 0

    try:
        for row in files.load_csv_files():
            db.insert(row.to_json())
            logs_processed += 1

            if logs_processed % batch_size == 0:
                batch_count += 1
                logging.info(
                    f"Processed {logs_processed} logs (batch {batch_count} completed)")

    except Exception as e:
        logging.error(
            f"Error processing logs at entry {logs_processed + 1}: {e}")
        raise

    return logs_processed


def load_config() -> Dict[str, Any]:
    """
    Loads and validates configuration settings from the config.ini file.

    Returns:
        Dict: A dictionary containing validated configuration values:
            - log_path: Directory path for log files
            - folder_path: Path to folder containing CSV files
            - export_path: Export destination path (optional)
            - elasticsearch_address: Elasticsearch server address (optional)
            - index_name: Elasticsearch index name (optional)
            - mapping: Database mapping schema (optional)

    Raises:
        FileNotFoundError: If required files are missing.
        ValueError: If required config values are missing.
        NotADirectoryError: If the folder path is not a valid directory.
    """
    def get_required_config(parser: ConfigParser, section: str, key: str) -> str:
        """Get required configuration value or raise ValueError."""
        value = parser.get(section, key, fallback=None)
        if not value or not value.strip():
            error_msg: str = f"Missing required configuration: [{section}] {key}"
            logging.critical(error_msg)
            raise ValueError(error_msg)
        return value.strip()

    def get_optional_config(parser: ConfigParser, section: str, key: str) -> Optional[str]:
        """Get optional configuration value, return None if missing/empty."""
        value = parser.get(section, key, fallback=None)
        return value.strip() if value and value.strip() else None

    def validate_path(folder_path: str, file_extension: str | None = None, create_if_missing: bool = False) -> str:
        """Validate path and optionally ensure files with extension exist."""
        path = Path(folder_path).resolve()
        if create_if_missing:
            path.mkdir(parents=True, exist_ok=True)
            return str(path)

        if not path.is_dir():
            error_msg: str = f"Folder path is not a directory: {path}"
            logging.critical(error_msg)
            raise NotADirectoryError(error_msg)

        if file_extension is not None and not any(path.glob(f"*{file_extension}")):
            error_msg: str = f"No files with extension '{file_extension}' found in {path}"
            logging.critical(error_msg)
            raise FileNotFoundError(error_msg)
        return str(path)

    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        error_msg: str = f"Config file not found at: {config_path}"
        logging.critical(error_msg)
        raise FileNotFoundError(error_msg)

    parser = ConfigParser()
    parser.read(config_path)
    config: Dict = {}

    config["folder_path"] = validate_path(
        get_required_config(parser, 'handler', 'folder_path'), ".csv")

    config["export_path"] = get_optional_config(
        parser, 'handler', 'export_path')
    if config["export_path"]:
        config["export_path"] = validate_path(
            config["export_path"], create_if_missing=True)
    config["elasticsearch_address"] = get_optional_config(
        parser, 'handler', 'elasticsearch_address')
    config["index_name"] = get_optional_config(
        parser, 'handler', 'index_name')
    mapping_path_string: str | None = get_optional_config(
        parser, 'handler', 'mapping')
    mapping = None
    if mapping_path_string:
        path = Path(mapping_path_string).resolve()
        if path.is_file():
            try:
                with open(path, "r") as f:
                    mapping = json.load(f)
            except json.JSONDecodeError as e:
                logging.warning(f"Invalid JSON in mapping file {path}: {e}")
            except Exception as e:
                logging.warning(f"Error reading mapping file {path}: {e}")
    config["mapping"] = mapping

    has_elasticsearch = config.get("elasticsearch_address")
    has_index_name = config.get("index_name")
    has_export_path = config.get("export_path")
    if has_elasticsearch and not has_index_name:
        logging.error(
            "Elasticsearch address provided but index_name is missing")
    elif has_index_name and not has_elasticsearch:
        logging.warning(
            "Index name provided but elasticsearch_address is missing")
    elif not has_elasticsearch and not has_export_path:
        error_msg = "No output destination configured - need either elasticsearch_address or export_path"
        logging.critical(error_msg)
        raise ValueError(error_msg)
    destinations = [
        config.get(key) for key in ['elasticsearch_address', 'export_path'] if config.get(key) is not None]
    logging.info(f"Configured output destinations: {destinations}")
    return config


if __name__ == "__main__":
    main()
