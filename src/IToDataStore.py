from abc import ABC, abstractmethod
#? The insert method would typically be called to store the logs in a data store.
class IToDataStore(ABC):
    """
    Interface for data store operations.
    """
    @abstractmethod
    def insert(self, arg) -> None:
       pass