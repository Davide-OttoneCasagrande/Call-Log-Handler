from abc import ABC, abstractmethod


class IDataStore(ABC):
    """
    Interface for data store operations.
    Classes implementing this interface should define how data is inserted into the store.
    """
    @abstractmethod
    def insert(self, json_log) -> None:
        """
        Insert a list of JSON strings into the data store.

        Args:
            jsonList (list[str]): A list of JSON-formatted strings representing call logs.
        """
        pass
