from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional
import logging
import json
import sys

import dataStore
import loader

log_path: str = "src/logs//app.log"
# Configuring root logger with proper formatting and handlers.
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

# Set up module-level logger.
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


def main(length_between_logging: int = 500) -> None:
    """
    Executes the log collection and export pipeline.

    Steps:
    1. Load configuration from the config file.
    2. Load call logs from the specified folder.
    3. Process each log and store it using the DataStore module
    4. Log progress every `length_between_logging` entries

    Args:
        length_between_logging (int): Number of logs to process before logging progress.
            Default is 500.

    Raises:
        SystemExit: If configuration loading or pipeline execution fails.
    """
    try:
        logger.info("initializing configuration settings...")
        config: dict= load_config()

        logger.info("initalizing log processing pipeline...")

        files = loader.CallLogLoader(config["folder_path"])
        db = dataStore.DataStore(
            config["export_path"], config["elasticsearch_address"], config["index_name"])

        if config["elasticsearch_address"] and not db.index_exists:
            if config["mapping"] is None:
                logger.warning(
                    "Mapping configuration is missing in the config file, index created empty.")
            db.create_mapping(config["mapping"])
            logger.info(
                f"Index '{config['index_name']}' doesn't exists, using config mapping.")
            
        logger.info("Starting log processing...")
        total_processed: int = process_logs(files, db, length_between_logging)

        success_message: str = f"Successfully processed {total_processed} logs"
        logger.info(success_message)

    except Exception as e:
        error_message: str = f"Pipeline failed: {e}"
        logger.critical(error_message, exc_info=True)
        sys.exit(1)


def process_logs(files: loader.CallLogLoader, db: dataStore.DataStore, batch_size: int) -> int:
    """
    Process and insert logs into the database.

    Args:
        files (CallLogLoader): Instance for reading CSV files.
        db (DataStore): Instance for database operations.
        batch_size (int): Number of logs to process before logging progress.

    Returns:
        Total number of logs processed

    Raises:
        Exception: If an error occurs during log processing.
    """
    logs_processed = 0
    batch_count = 0

    try:
        for row in files.load_csv_files():
            db.insert(row.to_json())
            logs_processed += 1

            if logs_processed % batch_size == 0:
                batch_count += 1
                logger.info(
                    f"Processed {logs_processed} logs (batch {batch_count} completed)")

    except Exception as e:
        logger.critical(
            f"Error processing logs at entry {logs_processed + 1}: {e}", exc_info=True)
        raise

    return logs_processed


def load_config() -> Dict[str, Any]:
    """
    Loads and validates configuration settings from the config.ini file.

    Returns:
        Dict[str, Any]: A dictionary containing validated configuration values:
            - folder_path (str): Path to folder containing CSV files
            - export_path (Optional[str]): Export destination path (optional)
            - elasticsearch_address (Optional[str]): Elasticsearch server address (optional)
            - index_name (Optional[str]): Elasticsearch index name (optional)
            - mapping (Optional[Dict]): Database mapping schema (optional)

    Raises:
        FileNotFoundError: If required files are missing.
        ValueError: If required config values are missing.
        NotADirectoryError: If the folder path is not a valid directory.
    """
    def get_config(parser: ConfigParser, section: str, key: str) -> Optional[str]:
        """
        Retrieve an optional configuration value from the config file.

        Args:
            parser (ConfigParser): The config parser instance.
            section (str): The section in the config file.
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The configuration value, or None if not present or empty.
        """
        value = parser.get(section, key, fallback=None)
        return value.strip() if value and value.strip() else None

    def validate_path(folder_path: str, file_extension: str | None = None, create_if_missing: bool = False) -> str:
        """
        Validate a folder path and optionally check for files with a specific extension.

        Args:
            folder_path (str): The path to validate.
            file_extension (Optional[str]): File extension to check for (e.g., '.csv').
            create_if_missing (bool): Whether to create the directory if it doesn't exist.

        Returns:
            str: The validated absolute path.

        Raises:
            NotADirectoryError: If the path is not a directory.
            FileNotFoundError: If no files with the given extension are found.
        """
        path = Path(folder_path).resolve()
        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
            return str(path)

        if not path.is_dir():
            error_msg: str = f"Folder path is not a directory: {path}"
            logger.critical(error_msg)
            raise NotADirectoryError(error_msg)

        if file_extension is not None and not any(path.glob(f"*{file_extension}")):
            error_msg: str = f"No files with extension '{file_extension}' found in {path}"
            logger.critical(error_msg)
            raise FileNotFoundError(error_msg)
        return str(path)

    config_path = Path("src/data/config.ini")
    if not config_path.is_file():
        error_msg: str = f"Config file not found at: {config_path}"
        logger.critical(error_msg)
        raise FileNotFoundError(error_msg)

    parser = ConfigParser()
    parser.read(config_path)
    config: Dict = {}

    folder_path = get_config(parser, 'handler', 'folder_path')
    if not folder_path:
            error_msg: str = f"Missing required configuration: [handler] folder_path"
            logger.critical(error_msg)
            raise ValueError(error_msg)
    else:
        config["folder_path"] = validate_path(folder_path, ".csv")

    config["export_path"] = get_config(
        parser, 'handler', 'export_path')
    if config["export_path"]:
        config["export_path"] = validate_path(
            config["export_path"], create_if_missing=True)
    config["elasticsearch_address"] = get_config(
        parser, 'handler', 'elasticsearch_address')
    config["index_name"] = get_config(
        parser, 'handler', 'index_name')
    mapping_path_string: str | None = get_config(
        parser, 'handler', 'mapping')
    mapping = None
    if mapping_path_string:
        path = Path(mapping_path_string).resolve()
        if path.is_file():
            try:
                with open(path, "r") as f:
                    mapping = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in mapping file {path}: {e}", exc_info=True)
            except Exception as e:
                logger.warning(f"Error reading mapping file {path}: {e}", exc_info=True)
    config["mapping"] = mapping

    has_elasticsearch = config.get("elasticsearch_address")
    has_index_name = config.get("index_name")
    has_export_path = config.get("export_path")
    if has_elasticsearch and not has_index_name:
        logger.error(
            "Elasticsearch address provided but index_name is missing")
    if has_index_name and not has_elasticsearch:
        logger.warning(
            "Index name provided but elasticsearch_address is missing")
    if not has_elasticsearch and not has_export_path:
        error_msg = "No output destination configured - need either elasticsearch_address or export_path"
        logger.critical(error_msg)
        raise ValueError(error_msg)
    destinations = [
        config.get(key) for key in ['elasticsearch_address', 'export_path'] if config.get(key) is not None]
    logger.info(f"Configured output destinations: {destinations}")
    return config


if __name__ == "__main__":
    main()
