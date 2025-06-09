from typing import Generator
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

    def load_csv_files(self)-> Generator[callLog.CallLog, None, None]:
       
        """
        Loads and parses all CSV files in the specified folder into CallLog objects.

        Yields:
            CallLog: An instance of CallLog for each valid row in the CSV files.

        Notes:
            - Files are processed in sorted order.
            - If a row cannot be parsed, an error message is printed and the row is skipped.
        """
        import csv
        csv_files = sorted(self.__folder_path.glob('*.csv'))

        for csv_file in csv_files:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try: 
                        yield callLog.CallLog(
                            timestamp=datetime.fromisoformat(row['timestamp']),
                            caller=row['caller'],
                            receiver=row['receiver'],
                            duration=int(row['duration']),
                            status=row['status'],
                            uniqueCallReference=row['uniqueCallReference']
                        )
                    except Exception as e:
                        print(f"Error parsing log entry: {row}. Error: {e}")
