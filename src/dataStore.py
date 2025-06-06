import iDataStore as interface
import os

class DataStore(interface.IDataStore):
    """
    A simple implementation of the IDataStore interface for testing purposes.

    Appends individual JSON-formatted log entries to a specified output file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the DataStore instance.
        
        Args:
            file_path (str): Path to the output JSON file.
        """
        self.file_path = file_path

    def insert(self, jsonLog: str):
        """
        Appends a single JSON-formatted log entry to the output file.

        Args:
            jsonLog (str): A JSON-formatted string representing a call log entry
        """
        self.file_path = os.path.abspath(os.path.normpath(self.file_path))
        with open(self.file_path, 'a', encoding='utf-8') as json_file:
            json_file.write(jsonLog + '\n')