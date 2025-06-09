from elasticsearch import Elasticsearch
import iDataStore as interface

class DataStore(interface.IDataStore):
    """
    A implementation of the IDataStore interface for a elasticsearch collection.
    """

    def __init__(self, export_path: str, index_name: str):
        """
        Initialize the DataStore instance.

        Args:
            export_path (str): URL to the Elasticsearch instance.
            index_name (str): Name of the Elasticsearch index.
        """
        self.es = Elasticsearch(export_path, verify_certs=False)
        self.index_name: str = index_name
        self.index_exists = self.es.indices.exists(index=index_name)

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
        self.es.indices.create(index=self.index_name, body=mapping)
        self.index_exists = True
        print(f"Index '{self.index_name}' created.")

    def insert(self, jsonLog: str):
        """
        Indexes a single JSON-formatted log entry into the Elasticsearch index.

        Args:
            jsonLog (str): A JSON-formatted string representing a call log entry.
            
        Raises:
            elasticsearch.ElasticsearchException: If indexing fails.
        """
        self.es.index(index=self.index_name, body=jsonLog)