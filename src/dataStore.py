from elasticsearch import Elasticsearch
import iDataStore as interface


class DataStore(interface.IDataStore):
    """
    A implementation of the IDataStore interface for a elasticsearch collection.
    """

    def __init__(self, export_path: str | None = None, elasticsearch_address: str | None = None, index_name: str | None = None):
        """
        Initialize the DataStore instance.

        Args:
            export_path (str): Path for file system export.
            elasticsearch_address (str): URL to the Elasticsearch instance.
            index_name (str): Name of the Elasticsearch index.
        """
        self.file_system_export = export_path
        self.index_exists: bool = False
        self.es = None
        self.index_name = None
        if elasticsearch_address:
            try:
                self.es = Elasticsearch(
                    elasticsearch_address, verify_certs=False)
                health = self.es.cluster.health()
                print(
                    f"Connected to Elasticsearch. Cluster status: {health['status']}")
            except Exception as e:
                raise ConnectionError(
                    f"Failed to connect to Elasticsearch at {elasticsearch_address}: {e}")

            if index_name and self.__validate_index_name(index_name):
                self.index_name = index_name
                response = self.es.indices.exists(index=self.index_name)
                self.index_exists = response.meta.status == 200
            else:
                raise ValueError(
                    f"Invalid  or missing index name: {index_name}. Must be lowercase and not contain special characters.")
        else:
            self.es = None

    def create_mapping(self, mapping: dict):
        """
        Creates a new Elasticsearch index with the specified mapping.

        This method initializes the index in the connected Elasticsearch instance
        using the provided mapping schema. It also updates the internal state to
        reflect that the index now exists.

        Args:
            mapping (dict): A dictionary defining the index mapping schema.

        Raises:
            elasticsearch.ElasticsearchException: If index creation fails.
        """
        if self.index_name and self.es:
            self.es.indices.create(index=self.index_name, body=mapping)
            self.index_exists = True
            print(f"Index '{self.index_name}' created.")
        else:
            raise ValueError(
                "Elasticsearch address or index name not provided.")

    def insert(self, json_log) -> None:
        """
        Indexes a single JSON-formatted log entry into the Elasticsearch index.

        Args:
            jsonLog (str): A JSON-formatted string representing a call log entry.

        Raises:
            elasticsearch.ElasticsearchException: If indexing fails.
        """
        if self.index_name and self.es:
            self.es.index(index=self.index_name, body=json_log)
        elif self.file_system_export:
            with open(self.file_system_export, 'a') as file:
                file.write(json_log + '\n')

    def __validate_index_name(self, index_name):
        # Elasticsearch index names must be lowercase and cannot contain certain characters
        if not index_name:
            return False
        if not index_name.islower():
            return False
        if any(char in index_name for char in [' ', ',', '#', ':', '*', '?', '"', '<', '>', '|', '\\', '/']):
            return False
        return True
