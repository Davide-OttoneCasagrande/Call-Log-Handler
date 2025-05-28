from datetime import datetime
import CallLog as callLog

def CSVLoader(file_path:str) -> list[callLog.CallLog]:
    """
    Load a CSV file and return its content as CallLog objects.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list[CallLog]: List of CallLog instances.
    """

    import csv
    logStrings: list[dict] = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            logStrings.append(row)

    callLogs: callLog.CallLog = _CallLogBulkInstancer(logStrings)
    
    #logs: list[dict] = _bulkToJson(callLogs)
    
    return callLogs

def _CallLogBulkInstancer(logStrings: list[dict]) -> list[callLog.CallLog]:
    """
    Convert a list of dictionaries to CallLog instances.

    Args:
        logStrings (list[dict]): Raw log data.

    Returns:
        list[CallLog]: List of CallLog objects.
    """

    CallLogs:list[callLog.CallLog] = []
    for log in logStrings:
        CallLogs.append(callLog.CallLog(
            timestamp=datetime.fromisoformat(log['timestamp']),
            caller=log['caller'],
            receiver=log['receiver'],
            duration=int(log['duration']),
            status=log['status'],
            uniqueCallReference=log['uniqueCallReference']
        ))
    return CallLogs

def _bulkToJson(callLogs: list[callLog.CallLog]) -> list[dict]:
    """
    Convert CallLog objects to JSON-serializable dictionaries.

    Args:
        callLogs (list[CallLog]): List of CallLog objects.

    Returns:
        list[dict]: List of dictionaries.
    """
    
    logs: list[dict] = []
    for log in callLogs:
        logs.append(log.__json__())
    return logs