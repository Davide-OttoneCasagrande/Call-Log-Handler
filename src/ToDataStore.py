import IToDataStore as interface
import configparser
import os
import json

class ToDataStore(interface.IToDataStore):
    """
    Temporary implementation of IToDataStore for testing.

    Saves data to a JSON file as specified in the config.
    """

    @staticmethod
    def insert(jsonList) -> None:
        config = configparser.ConfigParser()
        config.read(os.path.join("src", "data", "config.ini"))
        file_path = config.get('Settings', 'export_file_path', fallback=None)           
        if not file_path:
            raise ValueError("extportedLogs.json file path could not be read from config.")
        file_path = os.path.abspath(os.path.normpath(file_path))
        with open(file_path, 'w') as json_file:
            json.dump(jsonList, json_file, indent=4)