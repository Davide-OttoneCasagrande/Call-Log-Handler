import callLog

class LogCollector:
    """
    A class to collect and serialize call logs.
    """

    def __init__(self, logs: list[callLog.CallLog]):
        """
        Initialize the LogCollector with a list of CallLog instances.

        Args:
            logs (list[CallLog]): List of call log objects.
        """
        self.logs: list[dict] = logs

    def to_json__(self) -> list[str]:
        """
        Convert the list of CallLog instances to a list of JSON strings.

        Returns:
            list[str]: List of JSON-encoded call logs.
        """
        return [log.__json__() for log in self.logs]
    
if __name__ == "__main__":
    """
    Example usage of the LogCollector class.
    """
    # This block is not functional without actual CallLog instances.
    # Here's a placeholder example:
    from datetime import datetime

    sample_logs = [
        callLog.CallLog(
            timestamp=datetime.now(),
            caller="0123456789",
            receiver="6789012345",
            duration=120,
            status="successefully_completed",
            uniqueCallReference="abc123cwefwqt"
            )
    ]

    collector = LogCollector(sample_logs)
    print("Collected logs:")
    for log_json in collector.to_json__():
        print(log_json)
