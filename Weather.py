import numpy as np
import random
from config import ROTOR_RADIUS, MAX_POWER

# Horsea wind speed data from https://power.larc.nasa.gov/data-access-viewer/
path = open('./hornsea-ws-wd.csv')
array = np.loadtxt(path, delimiter=",", dtype='float', skiprows=11)
array = array[:,1:]
# Air density at sea level
AIR_DENSITY = 1.225
# Power efficiency. Cant be greater than 0.59. Around 0.35-0.45 for most turbines. Need research on hornsea turbines to find proper value
# to do - Power coeffecient not actually static - changes with tip speed ratio
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
    def update(self):
        self.speedu = round(self.speed * random.uniform(0.98,1.02),2)
        self.directionu = round(self.direction * random.uniform(0.98,1.02),2)
        return self.speedu, self.directionu

    # call update_hour only after get_speed. Updates the widn speed and direction by an hour when called. If get_speed is not called then default is the 1/1 hour 0
    def update_hour(self):
        self.counter += 1
        if self.counter > 8760:
            self.counter = 0
        self.speed = array[self.counter, 3]
        self.direction = array[self.counter, 4]
        return self.speed,self.direction

    # get power in Watts calculated from the wind speed. https://www.raeng.org.uk/publications/other/23-wind-turbine
    def get_power(self, windspeed):
        area = np.pi * (ROTOR_RADIUS**2)
        power = round((0.5 * AIR_DENSITY * area * (windspeed**3) * POWER_COEFFICIENT),2)
        power = min(power, MAX_POWER)
        return power

    # To do - get vibrations according to wind speed, turbine height, angle of blade, rpm, f = N/60 where N is rpm
    # A very loose model for modelling vibrations
    def get_vibrations(self, windspeed):
        #https://www.intechopen.com/chapters/57948 two main parts contribute to turbine vibrations, rotor and Post
        #https://reliabilityweb.com/articles/entry/vibration_analysis_of_wind_turbines
        #calculate the post vibration
        post_vibration = windspeed #* height / 100
        # assuming rotor vibration is a function of speed from the rotor speed (needs updating)

        rotor_vibration = windspeed ** 2
        total_vibration = round(post_vibration + rotor_vibration,2)
        return total_vibration
