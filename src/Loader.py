from datetime import datetime
from pathlib import Path
import callLog

class CallLogLoader:
    """
    Loads call logs from CSV files in a specified folder and converts them into CallLog objects.
    """


    def __init__(self, folder_path: str):
        """
        Initialize the CallLogLoader with a folder path and load the call logs.

        Args:
            folder_path (str): Path to the folder containing call log files.
        """
        self.__folder_path = Path(folder_path)
        self.callLogs = []
        self.__load_csv_files()

    def __load_csv_files(self):
        """
        Load all CSV files in the folder and parse their contents into CallLog objects.
        """
        import csv
        log_entries: list[dict] = []
        csv_files = sorted(self.__folder_path.glob('*.csv'))

        for csv_file in csv_files:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    log_entries.append(row)

        self.__create_call_log_instances(log_entries)

    def __create_call_log_instances(self, log_entries: list[dict]):
        """
        Convert a list of dictionaries to CallLog instances and store them.

        Args:
            logStrings (list[dict]): List of dictionaries representing raw log data.
        """
        for log in log_entries:
            try:
                self.callLogs.append(callLog.CallLog(
                    timestamp=datetime.fromisoformat(log['timestamp']),
                    caller=log['caller'],
                    receiver=log['receiver'],
                    duration=int(log['duration']),
                    status=log['status'],
                    uniqueCallReference=log['uniqueCallReference']
                ))
            except Exception as e:
                print(f"Error parsing log entry: {log}. Error: {e}")
