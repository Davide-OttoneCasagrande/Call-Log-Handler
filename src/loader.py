from typing import Generator
from datetime import datetime
from pathlib import Path
import callLog
import logging

# Set up module-level logger.
logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class CallLogLoader:
    """
    Loads call logs from CSV files in a specified folder and converts them into CallLog objects.
    """

    def __init__(self, folder_path: str):
        """
        Initialize the CallLogLoader with the path to the folder containing call log files.

        Args:
            folder_path (str): Path to the folder containing call log files.
        """
        logger.info(f"Initializing CallLogLoader from folder: {folder_path}")
        self.__folder_path = Path(folder_path)

    def load_csv_files(self)-> Generator[callLog.CallLog, None, None]:
       
        """
        Loads and parses all CSV files in the specified folder into CallLog objects.

        Yields:
            CallLog: An instance of CallLog for each valid row in the CSV files.

        Notes:
            - Files are processed in sorted order.
            - If a row cannot be parsed, an error message is logged and the row is skipped.
            - If a file cannot be read, an error is logged and the file is skipped.
        """
        import csv
        csv_files = sorted(self.__folder_path.glob('*.csv'))

        for csv_file in csv_files:
            try:
                with open(csv_file, mode='r', encoding='utf-8') as file:
                    logger.debug(f"Processing file: {csv_file}")
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
                            error_msg:str = f"Error parsing log entry: {row}. Error: {e}"
                            logger.exception(error_msg)
            except OSError as e:
                error_msg:str = f"Error reading file {csv_file}: {e}"
                logger.exception(error_msg)
                continue
