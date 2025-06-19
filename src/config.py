from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional
import logging
import json

# Set up module-level logger.
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class Config:

    def __init__(self, section: str = 'handler') -> None:
        """
        Loads and validates configuration settings from the config.ini file.

        Args:
            - section(str): Configuration section name to load settings from.Defaults to 'handler'.
        
        Attributes:
            - folder_path (str): Path to folder containing CSV files
            - export_path (Optional[str]): Export destination path (optional)
            - elasticsearch_address (Optional[str]): Elasticsearch server address (optional)
            - index_name (Optional[str]): Elasticsearch index name (optional)
            - mapping (Optional[Dict]): Database mapping schema (optional)
            - destinations (list[str]): List of configured output destinations.
            - delta_T_for_file(int): Time delta for file processing (non-default sections only).

        Raises:
            - FileNotFoundError: If required files are missing.
            - ValueError: If required config values are missing.
            - NotADirectoryError: If the folder path is not a valid directory.

        Note:
            - When section is not 'handler', only folder_path and delta_T_for_file are configured.
        """
        config_path: Path = Path("src/data/config.ini")
        self.DEFAULT_SECTION: str = 'handler'
        self.section: str = section
        if not config_path.is_file():
            error_msg: str = f"Config file not found at: {config_path}"
            logger.critical(error_msg)
            raise FileNotFoundError(error_msg)

        parser = ConfigParser()
        parser.read(config_path)

        folder_path = self.__get_config(parser, 'folder_path')
        if not folder_path:
                error_msg: str = f"Missing required configuration: [handler] folder_path"
                logger.critical(error_msg)
                raise ValueError(error_msg)
        else:
            self.folder_path = self.__validate_path(folder_path, ".csv")
        if self.section is not self.DEFAULT_SECTION:
                self.delta_T_for_file = int(parser.get(self.section, 'delta_T_for_file', fallback="1"))
                return

        self.export_path = self.__get_config(
            parser, 'export_path')
        if self.export_path:
            self.export_path = self.__validate_path(
                self.export_path, create_if_missing=True)
        self.elasticsearch_address = self.__get_config(
            parser, 'elasticsearch_address')
        self.index_name = self.__get_config(
            parser, 'index_name')

        self.__get_mapping(parser)
        self.__validate_configuration_consistency()

    
    def __get_config(self, parser: ConfigParser, key: str, fallback = None) -> Optional[str]:
        """
        Retrieve an optional configuration value from the config file.

        Args:
            - parser (ConfigParser): The config parser instance.
            - key (str): The key to retrieve.
            - fallback: Fallback value if the key is not found.

        Returns:
            - Configuration value stripped of whitespace, or None if empty/missing.
        """
        value = parser.get(self.section, key, fallback=fallback)
        return value.strip() if value and value.strip() else None

    def __validate_path(self, folder_path: str, file_extension: str | None = None, create_if_missing: bool = False) -> str:
        """
        Validate a folder path and optionally check for files with a specific extension.

        Args:
            - folder_path (str): The path to validate.
            - file_extension (Optional[str]): File extension to check for (e.g., '.csv').
            - create_if_missing (bool): Whether to create the directory if it doesn't exist.

        Returns:
            - str: The validated absolute path.

        Raises:
            - NotADirectoryError: If the path is not a directory.
            - FileNotFoundError: If no files with the given extension are found.
        """
        path = Path(folder_path).resolve()
        if create_if_missing:
            path.parent.mkdir(parents=True, exist_ok=True)
            return str(path)

        if not path.is_dir():
            error_msg: str = f"Folder path is not a directory: {path}"
            logger.critical(error_msg)
            raise NotADirectoryError(error_msg)

        if file_extension is not None and not any(path.glob(f"*{file_extension}"))and self.section is self.DEFAULT_SECTION:
            error_msg: str = f"No files with extension '{file_extension}' found in {path}"
            logger.warning(error_msg)
            raise FileNotFoundError(error_msg)
        return str(path)

    def __get_mapping(self, parser:ConfigParser) -> Optional[Dict[str, Any]]:
        """
        Load and parse JSON mapping file.
        
        Args:
            - parser (ConfigParser): The config parser instance.
            
        Returns:
            - Optional[Dict[str, Any]]: Parsed mapping dictionary or None if not found.
        """
        self.mapping = None
        mapping_path_string: str | None = self.__get_config(parser, 'mapping')
        if mapping_path_string:
            path = Path(mapping_path_string).resolve()
            if not path.is_file():
                logging.warning(f"Mapping file not found: {path}")
            else:
                try:
                    with open(path, "r") as f:
                        logging.info(f"Loaded mapping from: {path}")
                        self.mapping = json.load(f)
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON in mapping file {path}: {e}", exc_info=True)
                except Exception as e:
                    logger.warning(f"Error reading mapping file {path}: {e}", exc_info=True)

    def __validate_configuration_consistency(self) -> None:
        """
        Validate that configuration values are consistent with each other.
        
        Validation Rules:
            - If elasticsearch_address is provided, index_name should also be provided
            - If index_name is provided without elasticsearch_address, warning is logged
            - At least one of elasticsearch_address or export_path must be configured
            - Valid configurations: elasticsearch only, export_path only, or both
        
        returns:
            - None. Sets self.destinations attribute as side effect.
        """
        has_elasticsearch = self.elasticsearch_address is not None
        has_index_name = self.index_name is not None
        has_export_path = self.export_path is not None
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
        self.destinations = []
        self.destinations.append(self.elasticsearch_address) if self.elasticsearch_address else None
        self.destinations.append(self.export_path) if self.export_path else None
        logger.info(f"Configured output destinations: {self.destinations}")