import random
import shortuuid

class Call:
    def __init__(self,timestamp: str):
        """
        Initialize a Call instance with a timestamp and generate random call details.

        Args:
            timestamp (str): The timestamp of the call.
        """
        self.timestamp: str = timestamp
        self.uniqueCallReference: str = str(shortuuid.uuid())
        
        isGroupCall: bool =False
        if random.random() < 0.75:  # 75% chance to be a group call
            isGroupCall = True
        self.__generate_random_participants(isGroupCall)
        self.__generate_random_callStatus(isGroupCall)

    def __generate_random_participants(self, isGroupCall: bool) -> str:
        """
        Generates random caller and receiver IDs.

        Caller is always a 10-digit numeric string.
        Receiver is a 4-digit numeric string if it's a group call,
        otherwise a 10-digit numeric string different from the caller.

        Args:
            isGroupCall (bool): Whether the call is a group call.
        """
        self.caller = self.__generate_id(10)

        if isGroupCall:
            self.receiver = self.__generate_id(4)
        else:
            self.receiver = self.__generate_id(10)
            while self.receiver == self.caller:
                self.receiver = self.__generate_id(10)

    def __generate_id(self, lengthID: int) -> str:
        """
        Generate a random numeric ID of a specified length.

        Args:
            lengthID (int): The number of digits in the ID.

        Returns:
            str: A numeric string of the specified length.
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(lengthID)])

    def __generate_random_callStatus(self, isGroupCall: bool) -> str:
        
        """
        Generates a random call status and duration based on whether the call is a group call.

        Args:
            isGroupCall (bool): Whether the call is a group call.
        """
        chances: float = random.random()
        chances2: float = random.random()
        if random.random() < 0.6:
            self.status:str = "successfully_completed"
            self.duration:int = random.randint(1, 180)
        elif chances < 0.1:
            self.status:str = "interrupted_"
            if not isGroupCall:
                if chances2 < 0.5:
                    self.status= f"{self.status}higherPre-emptivePriorityInterruption"
                    self.duration:int = random.randint(1, 90)
                else:
                    self.status = f"{self.status}exceededTransmissionWindow"
                    self.duration:int =180
            else:
                self.status = f"{self.status}hostTransmissionPrivilegeExpired"
                self.duration:int = random.randint(100, 300)
        elif chances < 0.5:
            self.duration:int = 0
            self.status:str = "failed_"
            if not isGroupCall:
                if chances2 < 0.5:
                    self.status = f"{self.status}noAnswer"
                else:
                    self.status = f"{self.status}other"
            else:
                if chances2 < 0.5:
                    self.status = f"{self.status}insufficientPrivilege"
                else:
                    self.status = f"{self.status}groupNotExist"
        else:
            self.duration:int = random.randint(1, 30)
            self.status:str = "interrupted_"
            if not isGroupCall:
                if chances2 < 0.5:
                    self.duration:int = random.randint(1, 90)
                    self.status = f"{self.status}connectionLost"
                else:
                    self.status = f"{self.status}other"
            else:
                self.status = f"{self.status}other"

    def __str__(self):
        """
        Return the call entry as a CSV-formatted string.

        Returns:
            str: Call entry in CSV format.
        """
        return f"{self.timestamp},{self.caller},{self.receiver},{self.duration},{self.status},{self.uniqueCallReference}"