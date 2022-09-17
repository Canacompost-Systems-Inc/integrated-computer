from collections import defaultdict, deque
from datetime import datetime
from functools import partial
import logging

logger = logging.getLogger(__name__)

class Datapoint():
    def __init__(self, value: int, timestamp: datetime) -> None:
        self.value = value
        self.timestamp = timestamp

class MeasurementDatapoint():
    def __init__(self, id: str, datapoint: Datapoint) -> None:
        self.id = id
        self.datapoint = datapoint
        
class MeasurementRepo():
    def __init__(self, dataHistoryLength: int = 10000) -> None:
        # dataHistoryLength 1 point per 5 seconds = 12/min * 60 min * 24 hours = 18k points
        self.dataHistoryLength = dataHistoryLength
        self.data = defaultdict(partial(deque, maxlen=self.dataHistoryLength))

    def addPoint(self, measurementDatapoint: MeasurementDatapoint) -> None:
        id = measurementDatapoint.id
        if not id: 
            logger.warning("Logging for data for unkown measurement {id}".format(id))

        datapoint = measurementDatapoint.datapoint

        if not datapoint: 
            currentDateTime = datetime.now()
            value = None
            datapoint = Datapoint(timestamp=currentDateTime, value=value)
            logger.warning("Logging for {id} includes no data. Recording a value of {} witth current timestamp {}".format(id, currentDateTime, value))

        if not datapoint.timestamp: 
            currentDateTime = datetime.now()
            datapoint.timestamp = currentDateTime
            logger.warning("Logging for {id} includes no timestamp, setting a timestamp of {timestamp}".format(id = id, timestamp = currentDateTime))
       
        if  datapoint.value is None: 
            value = None
            logger.warning("Logging for {id} includes no measurement value, setting a value of {value}".format(id = id, value = value))

        # Add to sensor queue
        self.data[measurementDatapoint.id].append(datapoint)

    def get(self, id:str) -> Datapoint:
        if not id or id not in self.data:
            return None
        return self.data[id][-1]

    def getMultiple(self, id:str, numPoints:int) -> list[Datapoint]:
        if not id or id not in self.data:
            return None 
        if not numPoints:
            return list(self.data[id])
        # Not super efficient, but num data points is not massive
        return list(self.data[id])[-numPoints::]


