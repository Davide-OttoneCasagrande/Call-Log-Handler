from datetime import datetime

class CallLog:
    """
    Initialize a CallLog instance.

        Args:
            timestamp (datetime): Call timestamp.
            caller (str): Caller ID.
            receiver (str): Receiver ID.
            duration (int): Call duration in seconds.
            status (str): Call status (e.g., 'completed', 'missed').
            uniqueCallReference (str): Unique identifier for the call.
    """

    def __init__(self, timestamp:datetime, caller:str, receiver:str, duration:int, status:str, uniqueCallReference:str):
        self.timestamp:datetime = timestamp    #expected format: '2025-05-14T10:23:00'
        self.caller: str = caller
        self.receiver: str = receiver
        self.duration: int = duration
        self.status: str = status
        self.uniqueCallReference: str = uniqueCallReference

    def __json__(self) -> dict:
        """Convert the CallLog instance to a JSON-serializable dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "caller": self.caller,
            "receiver": self.receiver,
            "duration": self.duration,
            "status": self.status,
            "UniqueCallReference": self.uniqueCallReference
        }