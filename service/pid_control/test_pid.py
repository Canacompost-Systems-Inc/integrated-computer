
from service.pid_control.pid import PID
import time
import matplotlib.pyplot as plt
import random

# Test function
def testPid(kP = 0.2,  kI = 0.0, kD= 0.0, numberIterations=100):
    """Self-test PID class
    """
    # Initialize Class
    pid = PID(kP, kI, kD)

    pid.setpoint=0.0
    pid.setSampleTime(0.01)

    endIteration = numberIterations

    feedbackValue = 0

    # Arrays for plotting
    setpointList = []
    feedbackList = []
    # This uses iteration, but can include time instead
    timeList = []
   

    for i in range(1, endIteration):
        # calculate
        outputValue = pid.calculateOutput(feedbackValue)

        # Randomly change the setpoint every 50 iterations
        if (i%50==0):
            pid.setpoint = random.randrange(0,50)

        # Add some extra noise
        if pid.setpoint > 0:
            # Random noise between -3 to 3 %
            noise = outputValue * (random.randrange(-3,3)/100)
            feedbackValue += (outputValue + noise)

        # Delay between readings 
        time.sleep(0.01)

        # Create array of points for setpoint and feedback
        feedbackList.append(feedbackValue)
        setpointList.append(pid.setpoint)
        timeList.append(i)

        #print(pid.pTerm, pid.iTerm, pid.dTerm)
        #print(feedbackValue, pid.setpoint)

    plt.plot(timeList, feedbackList)
    plt.plot(timeList, setpointList)
    plt.xlim((0, numberIterations))
    plt.ylim((min(feedbackList)-0.5, max(feedbackList)+0.5))
    plt.xlabel('Iteration Count')
    plt.ylabel('PID')
    plt.title('Test PID Class')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    testPid(kP=1.2, kI=0.2, kD=0.001, numberIterations=250)
    