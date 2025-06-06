from datetime import datetime
import json

class CallLog:
    """
    Represents a single call log entry with metadata such as timestamp, caller, receiver, duration, status, and a unique reference.
    """
    def __init__(self, timestamp:datetime, caller:str, receiver:str, duration:int, status:str, uniqueCallReference:str):
        """
        Initialize a CallLog instance.

        Args:
            timestamp (datetime): Call timestamp.
            caller (str): Caller ID.
            receiver (str): Receiver ID.
            duration (int): Call duration in seconds.
            status (str): Call status (e.g., 'completed', 'missed').
            uniqueCallReference (str): unique identifier for the call.
    """
        self.timestamp:datetime = timestamp
        self.caller: str = caller
        self.receiver: str = receiver
        self.duration: int = duration
        self.status: str = status
        self.uniqueCallReference: str = uniqueCallReference

    def __to_dict(self) -> dict:
        """
        Convert the CallLog instance to a dictionary.

        Returns:
            dict: Dictionary representation of the call log.
        """
        return{
            "timestamp": self.timestamp.isoformat(),
            "caller": self.caller,
            "receiver": self.receiver,
            "duration": self.duration,
            "status": self.status,
            "UniqueCallReference": self.uniqueCallReference
        }

    def to_json(self) -> str:
        """
        Convert the CallLog instance to a JSON string.

        Returns:
            str: JSON representation of the call log.
        """
        return json.dumps(self.__to_dict())