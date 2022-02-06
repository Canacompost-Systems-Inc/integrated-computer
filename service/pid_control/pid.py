# Place all imports here
import time

class PID():

    # Init class
    def __init__(
            self,
            kP = 0.2,
            kI = 0.0,
            kD = 0.0,
            setpoint = 0,
    ):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.sampleTime = 0
        self.currentTime = time.time()
        self.previousTime = self.currentTime
        self.setpoint = setpoint

        self.resetPID()

    def resetPID(self):
        # Reset logic
        # Clear computed values
        self.pTerm = 0
        self.iTerm = 0
        self.dTerm = 0
        self.previousError = 0.0

        # Integral Windup Guard 
        # Todo : Review number
        self.integralWindupGuard = 5

        # Reset output value
        self.outputValue = 0.0

    
    def setkP(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.kP = proportional_gain

    def setkI(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.kI = integral_gain

    def setkD(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.kD = derivative_gain
    
    def updateSetpoint(self, newSetpoint):
        """Update the setpoint for the given PID"""
        self.setpoint = newSetpoint

    def setIntegralWindupGuard(self, newIntegralWindupGuardValue):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.integralWindupGuard = newIntegralWindupGuardValue

    def calculateOutput(self, inputFeedbackValue, currentTime=None):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        """

        currentError = self.setpoint - inputFeedbackValue
        currentTime = time.time()
        timeDelta = currentTime - self.previousTime
        errorDelta = currentError - self.previousError

        # Don't process too quickly (rate limit)
        if (timeDelta >= self.sampleTime):
            self.pTerm = self.kP * currentError
            self.iTerm  += currentError * timeDelta

            if (self.iTerm < -self.integralWindupGuard):
                self.iTerm = -self.integralWindupGuard
            elif (self.iTerm > self.integralWindupGuard):
                self.iTerm = self.integralWindupGuard

            self.dTerm = 0.0

            # Protect against 0 for delta time, or erroneous time
            if timeDelta > 0:
                self.DTerm = errorDelta / timeDelta

            # Remember last time and last error for next calculation
            self.last_time = self.currentTime
            self.last_error = currentError

            #Calculate Output
            self.outputValue = self.pTerm + (self.kI * self.iTerm) + (self.kD * self.dTerm)

            return self.outputValue


        # Update 'previous' variables
        self.previousTime = currentTime
        self.previousError = currentError


    def setSampleTime(self, sampleTime):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sampleTime = sampleTime
