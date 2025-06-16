from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional
import logging
import json


class Config:

    def __init__(self):
        self.__log_handler_config()

    def __log_handler_config(self) -> Dict[str, Any]:
        """
        Loads and validates configuration settings from the config.ini file.

        Returns:
            dict: A dictionary containing validated configuration values:
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
                logging.critical(ValueError(
                    f"Missing required configuration: [{section}] {key}"))
                raise
            return value.strip()

        def get_optional_config(parser: ConfigParser, section: str, key: str) -> Optional[str]:
            """Get optional configuration value, return None if missing/empty."""
            value = parser.get(section, key, fallback=None)
            return value.strip() if value and value.strip() else None

        def path_validation(folder_path: str, file_extension: str | None = None) -> str:
            """Validate path and optionally ensure CSV files existence."""
            path = Path(folder_path).resolve()

            if not path.is_dir():
                logging.critical(NotADirectoryError(
                    f"Folder path is not a directory: {path}"))

            if file_extension is not None and not any(path.glob(f"*{file_extension}")):
                raise FileNotFoundError(
                    f"No CSV files found in folder: {path}")
            return str(path)

        config_path = Path("src/data/config.ini")
        if not config_path.is_file():
            logging.critical(f"Config file not found at: {config_path}")
            raise FileNotFoundError(f"Config file not found at: {config_path}")

        parser = ConfigParser()
        parser.read(config_path)
        config: dict = {}

        config["log_path"] = path_validation(
            get_required_config(parser, 'handler', 'log_path'), ".log")
        config["folder_path"] = path_validation(
            get_required_config(parser, 'handler', 'folder_path'), ".csv")

        config["export_path"] = get_optional_config(
            parser, 'handler', 'export_path')
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
                    logging.warning(
                        f"Invalid JSON in mapping file {path}: {e}", exc_info=True)
                except Exception as e:
                    logging.warning(f"Error reading mapping file {path}: {e}", exc_info=True)
        config["mapping"] = mapping

        has_elasticsearch = config.get("elasticsearch_address")
        has_index_name = config.get("index_name")
        has_mapping = config.get("mapping")
        has_export_path = config.get("export_path")
        if has_elasticsearch and not has_index_name:
            logging.error(
                "Elasticsearch address provided but index_name is missing")
        elif has_index_name and not has_mapping:
            logging.warning(
                "Index name provided but elasticsearch_address is missing")
        elif not has_elasticsearch and not has_export_path:
            logging.critical("there isn't any configured destination")

        return config


def load_config() -> Dict[str, Any]:
    """
    Load and validate configuration settings from config.ini file.

    Returns:
        Dictionary containing validated configuration values:
        - log_path: Directory path for log files
        - folder_path: Path to folder containing CSV files  
        - export_path: Export destination path (optional)
        - elasticsearch_address: Elasticsearch server address (optional)
        - index_name: Elasticsearch index name (optional)
        - mapping: Database mapping schema (optional)

    Raises:
        FileNotFoundError: If required files are missing
        ValueError: If required config values are invalid
        NotADirectoryError: If specified paths are not valid directories
    """
    config_path = Path("src/data/config.ini")

    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    parser = ConfigParser()
    parser.read(config_path)

    # Load and validate required settings
    config = {}

    # Required settings
    config["log_path"] = _validate_log_path(
        _get_required_config(parser, 'handler', 'log_path')
    )
    config["folder_path"] = _validate_folder_path(
        _get_required_config(parser, 'handler', 'folder_path')
    )

    # Optional settings with validation
    config["export_path"] = _get_optional_config(
        parser, 'handler', 'export_path')
    config["elasticsearch_address"] = _get_optional_config(
        parser, 'handler', 'elasticsearch_address')
    config["index_name"] = _get_optional_config(
        parser, 'handler', 'index_name')

    # Load mapping if provided
    mapping_path = _get_optional_config(parser, 'handler', 'mapping')
    config["mapping"] = _load_mapping_file(
        mapping_path) if mapping_path else None

    _validate_configuration_consistency(config)

    return config


def _get_required_config(parser: ConfigParser, section: str, key: str) -> str:
    """Get required configuration value or raise ValueError."""
    value = parser.get(section, key, fallback=None)
    if not value or not value.strip():
        raise ValueError(f"Missing required configuration: [{section}] {key}")
    return value.strip()


def _get_optional_config(parser: ConfigParser, section: str, key: str) -> Optional[str]:
    """Get optional configuration value, return None if missing/empty."""
    value = parser.get(section, key, fallback=None)
    return value.strip() if value and value.strip() else None


def _validate_log_path(log_path: str) -> str:
    """Validate and create log directory path."""
    path = Path(log_path).resolve()

    # If it's a file path, use its parent directory
    if path.suffix:
        path = path.parent

    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def _validate_folder_path(folder_path: str) -> str:
    """Validate folder path and ensure CSV files exist."""
    path = Path(folder_path).resolve()

    if not path.is_dir():
        raise NotADirectoryError(f"Folder path is not a directory: {path}")

    if not any(path.glob("*.csv")):
        raise FileNotFoundError(f"No CSV files found in folder: {path}")

    return str(path)


def _load_mapping_file(mapping_path: str) -> Optional[Dict[str, Any]]:
    """Load and parse JSON mapping file."""
    path = Path(mapping_path).resolve()

    if not path.is_file():
        logging.warning(f"Mapping file not found: {path}")
        return None

    try:
        with open(path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        logging.info(f"Loaded mapping from: {path}")
        return mapping
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in mapping file {path}: {e}", exc_info=True)
        return None
    except Exception as e:
        logging.error(f"Error reading mapping file {path}: {e}", exc_info=True)
        return None


def _validate_configuration_consistency(config: Dict[str, Any]) -> None:
    """Validate that configuration values are consistent with each other."""
    has_elasticsearch = config.get("elasticsearch_address")
    has_index_name = config.get("index_name")

    if has_elasticsearch and not has_index_name:
        logging.warning(
            "Elasticsearch address provided but index_name is missing")
    elif has_index_name and not has_elasticsearch:
        logging.warning(
            "Index name provided but elasticsearch_address is missing")
