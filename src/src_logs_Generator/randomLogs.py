from datetime import datetime, timedelta
import logging
import random
import call

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class Logsfile:
    """
    Generates a list of random call logs within a specified time range.
    """

    def __init__(self, startingHour: datetime, deltaT: timedelta):
        """
        Initialize the Logsfile with a header and generated log entries.

        Args:
            startingHour (datetime): The start time for log generation.
            deltaT (timedelta): The duration over which logs are generated.
        """
        self.logs: list[str] = ["timestamp,caller,receiver,duration,status,uniqueCallReference"]
        self.deltaT = int(deltaT.total_seconds())
        self.number_of_logs = random.randint(100, 1000)
        logger.debug(f"Generating {self.number_of_logs} logs over a period of {self.deltaT} seconds starting from {startingHour.isoformat()}")
        timeStamps: list[str] = self.__generate_random_timestamps(startingHour)
        for timeStamp in timeStamps:
            log = call.Call(timeStamp)
            self.logs.append(str(log))

    def __generate_random_timestamps(self, startingHour: datetime) -> list[str]:
        """
        Generate random timestamps within the specified time range.

        Args:
            startingHour (datetime): The start time for generating timestamps.

        Returns:
            list[str]: Sorted list of timestamps in ISO format (YYYY-MM-DDTHH:MM:SS).
        """
        timestamps: list[datetime] = [
            startingHour + timedelta(seconds=random.randint(0, self.deltaT))
            for _ in range(self.number_of_logs)
        ]
        timestamps.sort()
        return [timestamp.strftime("%Y-%m-%dT%H:%M:%S") for timestamp in timestamps]