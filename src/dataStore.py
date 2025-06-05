import iDataStore as interface
import json
import os

class DataStore(interface.IDataStore):
    """
    Temporary implementation of IToDataStore for testing.

    Saves a list of JSON strings to a file specified by the configuration.
    """
    def __init__(self, file_path: str):
        """
        Initialize the DataStore instance.
        
        Args:
            file_path (str): Path to the output JSON file.
        """
        self.file_path = file_path

    def insert(self, jsonList: list[str]):
        """
        Write the list of JSON strings to the specified file.

        Args:
            jsonList (list[str]): List of JSON-formatted strings to be saved.
        """

        self.file_path = os.path.abspath(os.path.normpath(self.file_path))
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(jsonList, json_file, indent=4, ensure_ascii=False)