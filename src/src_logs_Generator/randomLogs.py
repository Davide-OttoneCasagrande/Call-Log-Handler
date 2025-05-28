from datetime import datetime, timedelta
import random
import string

class Logsfile:
    """
    Generates a list of random call logs.
    """
    
    def __init__(self, number_of_entries: int = None):
        """
        Initialize the Logsfile with a header and generated log entries.

        Args:
            number_of_entries (int, optional): Number of log entries to generate.
        """

        self.logs: list[str] = ["timestamp,caller,receiver,duration,status,uniqueCallReference"]
        if number_of_entries is None:
            number_of_entries = random.randint(30, 1000)
        for _ in range(number_of_entries):
            self._logGenerator()
            
    def _logGenerator(self):
        """
        Generate a single log entry and append it to the logs list.
        """
        timestamp: str = self._generate_random_timestamp()

        isGroupCall: bool =False
        if random.random() < 0.75:  # 75% chance to be a group call
            isGroupCall = True
        participants: str = self._generate_random_participants(isGroupCall)

        callStatus: str = self._generate_random_callStatus(isGroupCall)

        uniqueCallReference:str = self._generate_random_uniqueCallReference()
        self.logs.append(f"{timestamp},{participants},{callStatus},{uniqueCallReference}")


    def _generate_random_timestamp(self)-> str:        
        """
        Generate a random timestamp within the last 5 years.

        Returns:
            str: Timestamp in ISO format (YYYY-MM-DDTHH:MM).
        """

        now = datetime.now()
        five_years_ago = now - timedelta(days=5*365)
        random_datetime = five_years_ago + (now - five_years_ago) * random.random()
        return random_datetime.strftime("%Y-%m-%dT%H:%M")


    def _generate_random_participants(self, isGroupCall: bool) -> str:
        """
        Generates a random caller and receiver ID.

        Args:
            isGroupCall (bool): Whether the call is a group call.

        Returns:
            str: Comma-separated caller and receiver IDs
        """

        caller_id = random.randint(0, 1000000000)

        if isGroupCall:
            receiver_id = random.randint(0, 1000)
        else:
            receiver_id = random.randint(0, 1000000000)
            while receiver_id == caller_id:
                receiver_id = random.randint(0, 1000000000)

        return f"{caller_id},{receiver_id}"

    def _generate_random_callStatus(self, isGroupCall: bool) -> str:
        """
        Generate a random call status and duration.

        Args:
            isGroupCall (bool): Whether the call is a group call.

        Returns:
            str: Duration and status string.
        """

        chances: float = random.random()
        chances2: float = random.random()
        if random.random() < 0.6:
            status:str = "successfully_completed"
            return f"{random.randint(1, 180)},{status}"
        elif chances < 0.1:
            status:str = "interrupted_"
            if not isGroupCall:
                if chances2 < 0.5:
                    return f"{random.randint(1, 90)},{status}higerPre-emptivePriorityInterruption"
                else:
                    return f"180,{status}exceededTransmissionWindow"
            else:
                return f"{random.randint(100, 300)},{status}hostTransmissionPrivilegeExpired"
        elif chances < 0.5:
            status:str = "failed_"
            if not isGroupCall:
                if chances2 < 0.5:
                    return f"0,{status}noAnswer"
                else:
                    return f"0,{status}other"
            else:
                if chances2 < 0.5:
                    return f"0,{status}insufficientPrivilege"
                else:
                    return f"0,{status}groupNotExhist"
        else:
            status:str = "interrupted_"
            if not isGroupCall:
                if chances2 < 0.5:
                    return f"{random.randint(1, 90)},{status}connectionLost"
                else:
                    return f"{random.randint(1, 30)},{status}other"
            else:
                return f"{random.randint(1, 30)},{status}other"
            
    def _generate_random_uniqueCallReference(self, length=8):
        """
        Generate a random alphanumeric string.

        Args:
            length (int): Length of the string.

        Returns:
            str: Random string.
        """

        characters = string.ascii_letters + string.digits # A-Z, a-z, 0-9
        return ''.join(random.choices(characters, k=length))
    
    def __str__(self):
        """
        Return the logs as a list of strings.

        Returns:
            list[str]: List of log entries.
        """

        return self.logs
    
if __name__ == "__main__":
    Logs = Logsfile(10)
    print("Log file generated successfully.")
    print(Logs.logs)