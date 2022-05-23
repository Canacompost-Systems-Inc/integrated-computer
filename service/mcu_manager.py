import time
from datetime import datetime, timedelta
from controller import temperature

class StateManager():
    """
    The StateManager keeps track of the recycler
    """

    # R1 = Lower Temperature
    R1_START_TEMP_THRESHOLD = 65
    R1_END_TEMP_THRESHOLD = 60

    # R2 = Lower Humidity
    R2_START_HUM_THRESHOLD_BSFL = 50
    R2_END_HUM_THRESHOLD_BSFL = 48
    R2_START_HUM_THRESHOLD_NO_BSFL = 80
    R2_END_HUM_THRESHOLD_NO_BSFL = 78

    # R3 = Raise Humidity
    R3_START_HUM_THRESHOLD_BSFL = 30
    R3_END_HUM_THRESHOLD_BSFL = 32
    R3_START_HUM_THRESHOLD_NO_BSFL = 50
    R3_END_HUM_THRESHOLD_NO_BSFL = 52

    # R4 = Raise Oxygen
    R4_START_OXYGEN_THRESHOLD = 16
    R4_END_OXYGEN_THRESHOLD = 18

    # R5 = Air Cycle
    R5_RUNTIME_MINS = 2
    R5_LAST_COMPRESSOR_STOP_MINS_THRESHOLD = 2

    def __init__(self, oxygen_service, temperature_service, humidity_service, bsfl_service, compressor_service, routines_service):
        self.oxygen_service = oxygen_service
        self.temperature_service = temperature_service
        self.humidity_service = humidity_service
        self.bsfl_service = bsfl_service
        self.compressor_service = compressor_service
        self.routines_service = routines_service

    # Manage state function is intended to be run as a looping thread. Should periodically monitor & control the recycler
    def manage_state(self):
        while True:
            time.sleep(3)
            oxygen = self.oxygen_service.getOxygen()
            temperature = self.temperature_service.getTemperature()
            humidity = self.humidity_service.getHumidity()
            bsfl = self.bsfl_service.getBSFL()
            last_compressor_start = self.compressor_service.getLastStart()
            last_compressor_stop = self.compressor_service.getLastStop()
            active_routine = self.routines_service.getActiveRoutine()
            print("--- Monitoring and controlling the recycler. Current State: ---")
            print("Oxygen: "+str(oxygen)+", Temperature: "+str(temperature)+", Humidity: "+str(humidity)+", BSFL: "+str(bsfl)+", Last Compressor Start: "+str(last_compressor_start)+", Last Compressor Stop: "+str(last_compressor_stop)+", Active Routine: "+active_routine)

            match active_routine:
                # If any non-default routines are running, check if routine should stop by going to R0 (default)
                case "R1":
                    print("Checking if routine R1 should end")
                    if temperature <= self.R1_END_TEMP_THRESHOLD:
                        self.routines_service.startR0()
                        continue

                case "R2":
                    print("Checking if routine R2 should end")
                    if bsfl and humidity <= self.R2_END_HUM_THRESHOLD_BSFL:
                        self.routines_service.startR0()
                        continue
                    elif not bsfl and humidity <= self.R2_END_HUM_THRESHOLD_NO_BSFL:
                        self.routines_service.startR0()
                        continue

                case "R3":
                    print("Checking if routine R3 should end")
                    if humidity >= self.R3_END_HUM_THRESHOLD_BSFL:
                        self.routines_service.startR0()
                        continue
                    elif not bsfl and humidity >= self.R3_END_HUM_THRESHOLD_NO_BSFL:
                        self.routines_service.startR0()
                        continue

                case "R4":
                    print("Checking if routine R4 should end")
                    if oxygen >= self.R4_END_OXYGEN_THRESHOLD:
                        self.routines_service.startR0()
                        continue

                case "R5":
                    print("Checking if routine R5 should end")
                    # if datetime.now() - timedelta(seconds=10) > last_compressor_start: # Useful for testing
                    if datetime.now() - timedelta(minutes=self.R5_RUNTIME_MINS) > last_compressor_start:
                        self.routines_service.startR0()
                        continue

                # If machine is in default state (R0), check if any routines should start
                case "R0":
                    print("Checking if any routines should start")
                    if temperature > self.R1_START_TEMP_THRESHOLD:
                        self.routines_service.startR1()
                        continue

                    if bsfl and humidity > self.R2_START_HUM_THRESHOLD_BSFL:
                        self.routines_service.startR2()
                        continue
                    if not bsfl and humidity > self.R2_START_HUM_THRESHOLD_NO_BSFL:
                        self.routines_service.startR2()
                        continue

                    if bsfl and humidity < self.R3_START_HUM_THRESHOLD_BSFL:
                        self.routines_service.startR3()
                        continue
                    if not bsfl and humidity < self.R3_START_HUM_THRESHOLD_NO_BSFL:
                        self.routines_service.startR3()
                        continue

                    if oxygen < self.R4_START_OXYGEN_THRESHOLD:
                        self.routines_service.startR4()
                        continue
                    #if datetime.now() - timedelta(seconds=10) > last_compressor_stop: # Useful for testing
                    if datetime.now() - timedelta(minutes=self.R5_LAST_COMPRESSOR_STOP_MINS_THRESHOLD) > last_compressor_stop:
                        self.routines_service.startR5()
                        continue