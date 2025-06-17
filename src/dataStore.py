from elasticsearch import Elasticsearch
import iDataStore as interface
import logging

"""Set up module-level logger."""
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logging.getLogger("elastic_transport.transport").setLevel(logging.WARNING)

class DataStore(interface.IDataStore):
    """
    Implementation of the IDataStore interface for storing logs in an Elasticsearch index or exporting them to the file system.
    """

    def __init__(self, export_path: str | None = None, elasticsearch_address: str | None = None, index_name: str | None = None):
        """
        Initialize the DataStore instance.

        Args:
            export_path (str): Path for file system export.
            elasticsearch_address (str): URL to the Elasticsearch instance.
            export_path (str): Path for file system export.
            elasticsearch_address (str): URL to the Elasticsearch instance.
            index_name (str): Name of the Elasticsearch index.

        Raises:
            ConnectionError: If connection to Elasticsearch fails.
            ValueError: If the index name is invalid or missing when required.
        """
        logger.info("Initializing DataStore...")
        self.index_exists: bool = False
        self.es = None
        self.index_name = None
        self.file_system_export = export_path
        if self.file_system_export:
            logger.info(f"File system export path set to: {self.file_system_export}")
        if not elasticsearch_address:
            self.es = None
        else:
            try:
                self.es = Elasticsearch(
                    elasticsearch_address, verify_certs=False)
                health = self.es.cluster.health()
                logger.info(
                    f"Connected to Elasticsearch. Cluster status: {health['status']}")
            except Exception as e:
                error_msg = f"Failed to connect to Elasticsearch at {elasticsearch_address}: {e}"
                logger.exception(error_msg)
                raise ConnectionError(error_msg)

            if index_name and self.__validate_index_name(index_name):
                self.index_name = index_name
                response = self.es.indices.exists(index=self.index_name)
                self.index_exists = response.meta.status == 200
            else:
                error_msg: str =  f"Invalid or missing index name: {index_name}. Must be lowercase and not contain special characters."
                logger.error(error_msg)
                raise ValueError(error_msg)
   
    def create_mapping(self, mapping: dict):
        """
        Creates a new Elasticsearch index with the specified mapping.

        Args:
            mapping (dict): A dictionary defining the index mapping schema.

        Raises:
            ValueError: If Elasticsearch is not configured, the index name is missing, or index creation fails.
        """
        if self.index_name and self.es:
            try:
                self.es.indices.create(index=self.index_name, body=mapping)
                self.index_exists = True
                logger.info(f"Index '{self.index_name}' created.")
            except Exception as e:
                error_msg = f"Failed to create index '{self.index_name}': {e}"
                logger.exception(error_msg)
                raise ValueError(error_msg)
        else:
            error_msg: str = "Elasticsearch address or index name not provided."
            logger.critical(error_msg)
            raise ValueError(error_msg)

    def insert(self, json_log) -> None:
        """
        Index a single JSON-formatted log entry into Elasticsearch and/or write to file.

        Args:
            json_log (str): A JSON-formatted string representing a call log entry.

        Raises:
            elasticsearch.ElasticsearchException: If indexing fails.
        """
        if self.index_name and self.es:
            self.es.index(index=self.index_name, body=json_log)
        if self.file_system_export:
            with open(self.file_system_export, 'a') as file:
                file.write(json_log + '\n')

    def __validate_index_name(self, index_name):
        """
        Validate the Elasticsearch the Elasticsearch index name.
        Index names must be lowercase and must not contain forbidden characters.

        Args:
            index_name (str): The index name to validate.

        Returns:
            bool: True if the index name is valid, False otherwise.
        """
        forbidden_chars = [' ', ',', '#', ':', '*', '?', '"', '<', '>', '|', '\\', '/']
        if not index_name:
            return False
        if not index_name.islower():
            logger.error(f"Invalid index name '{index_name}': must be all lowercase.")
            return False
        for char in forbidden_chars:
            if char in index_name:
                logger.error(f"Invalid index name '{index_name}': contains forbidden character '{char}'.")
                return False
        return True