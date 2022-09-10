import itertools
import time
from collections import defaultdict, deque, namedtuple
from datetime import datetime
from functools import partial


class Datapoint():
    def __init__(self, value: int, timestamp: datetime) -> None:
        self.value = value
        self.timestamp = timestamp

class SensorDatapoint():
    def __init__(self, id: str, datapoint: Datapoint) -> None:
        self.id = id
        self.datapoint = datapoint
        
class SensorRepo():
    def __init__(self, dataHistoryLength: int = 10000):
        # dataHistoryLength 1 point per 5 seconds = 12/min * 60 min * 24 hours = 18k points
        self.dataHistoryLength = dataHistoryLength
        self.data = defaultdict(partial(deque, maxlen=self.dataHistoryLength))

    def addPoint(self, sensorDatapoint: SensorDatapoint):
        if not sensorDatapoint.id: 
            # Raise Exceptipon??
            return
        datapoint = sensorDatapoint.datapoint
        if not datapoint:
            # TO DO, do we store the value as NONE? or not
            pass
        # Add to sensor queue
        self.data[sensorDatapoint.id].append(datapoint)

    def get(self, sensorId:str):
        if not sensorId or sensorId not in self.data:
            return None
        return self.data[sensorId][-1]

    def list(self, sensorId:str, numPoints:int):
        if not sensorId or sensorId not in self.data:
            return None 
        # Not super efficient, but num data points is not massive
        return list(self.data[sensorId])[-numPoints::]


sensorRepo = SensorRepo(dataHistoryLength=200000)
sensorName1 = 'TestA'
sensorName2 = 'TestB'
for i in range(100):
    sensorRepo.addPoint(SensorDatapoint(id=sensorName1, datapoint=Datapoint(value=i, timestamp=datetime.now())))
    sensorRepo.addPoint(SensorDatapoint(id=sensorName2, datapoint=Datapoint(value=i, timestamp=datetime.now())))
    time.sleep(0.01)

print(sensorRepo.get(sensorId=sensorName1),sensorRepo.get(sensorId=sensorName2))
for point in sensorRepo.list(sensorId=sensorName1, numPoints=10):
    print('SensorId: {sensorId} Timestamp: {timestamp} Value: {value}'.format(sensorId=sensorName1,timestamp=point.timestamp,value=point.value))
