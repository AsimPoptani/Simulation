import numpy as np
from config import ROTOR_RADIUS, MAX_POWER, AIR_DENSITY, TURBINE_HEIGHT

# Horsea wind speed data from https://power.larc.nasa.gov/data-access-viewer/
path = open('./hornsea-ws-wd.csv')
array = np.loadtxt(path, delimiter=",", dtype='float', skiprows=11)
array = array[:,1:]

# Power efficiency. Cant be greater than 0.59. Around 0.35-0.45 for most turbines.
POWER_COEFFICIENT = 0.4

# Gets wind speed and direction (speed, direction) for a given month,day,hour
class Datagen():
    def __init__(self) -> None:
        self.counter = 0
        self.speed = 0
        self.direction = 0

    # call get_speed to get the speed and direction for a given month day and hour. Returns wind speed in m/s and direction
    def get_speed(self, month, day, start_hour):
        for row in array:
            self.counter += 1
            if int(row[0]) == month and int(row[1]) == day and int(row[2]) == start_hour:
                self.speed = row[3]
                self.direction = row[4]
                return self.speed,self.direction

    # Account for noise / slight variations in speed across wind turbines. Returns an updated wind speed in m/s and direction
    # Call every hour to get new windspeeds
    def update(self):
        self.counter += 1
        if self.counter > 8760:
            self.counter = 0
        self.speed = array[self.counter, 3]
        self.direction = array[self.counter, 4]

        self.speedu = round(self.speed * np.random.uniform(0.98,1.02),2)
        self.directionu = round(self.direction * np.random.uniform(0.98,1.02),2)
        return self.speedu, self.directionu

    # get power in Watts calculated from the wind speed. https://www.raeng.org.uk/publications/other/23-wind-turbine
    def get_power(self, windspeed):
        if windspeed > 25 or windspeed <= 3:
            power = 0
            return power
        area = np.pi * (ROTOR_RADIUS**2)
        power = round((0.5 * AIR_DENSITY * area * (windspeed**3) * POWER_COEFFICIENT),2)
        power = min(power, MAX_POWER)
        return power

    # Model Vibrations based on https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7957485/
    # Gets the vibrations in m/s^2 (acceleration)
    def get_vibrations(self, windspeed):
        # If rotor isn't moving when above and below ceratin wind speeds it doesn't include rotor vibrations in calculation
        # If wind turbine has a fault should increase the vibrations based on the faults using data in https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7957485/
        if windspeed > 25 or windspeed <= 3:
            vibrations = round((windspeed * TURBINE_HEIGHT) / 100000,6)
            return vibrations
        vibrations = round(((windspeed ** 2) * TURBINE_HEIGHT) / 100000, 6)
        return vibrations
