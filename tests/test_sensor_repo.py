# import pytest
import time
import datetime
from repos.measurement_repo import (Datapoint, MeasurementDatapoint,
                                    MeasurementRepo)

# TODO : Will move this to pytest later this week
def testHappyCase():
    pass

measurementRepo = MeasurementRepo(dataHistoryLength=200000)
measurementName1 = 'TestA'
measurementName2 = 'TestB'
for i in range(100):
    measurementRepo.addPoint(MeasurementDatapoint(id=measurementName1, datapoint=Datapoint(value=i, timestamp=datetime.now())))
    measurementRepo.addPoint(MeasurementDatapoint(id=measurementName2, datapoint=Datapoint(value=i, timestamp=datetime.now())))
    time.sleep(0.01)

print(measurementRepo.get(id=measurementName1),measurementRepo.get(id=measurementName2))
for point in measurementRepo.list(id=measurementName1, numPoints=10):
    print('SensorId: {id} Timestamp: {timestamp} Value: {value}'.format(id=measurementName1,timestamp=point.timestamp,value=point.value))