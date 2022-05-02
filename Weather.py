import numpy as np
import random

# Horsea wind speed data from https://power.larc.nasa.gov/data-access-viewer/
path = open('./hornsea-ws-wd.csv')
array = np.loadtxt(path, delimiter=",", dtype='float', skiprows=11)
array = array[:,1:]

# Gets wind speed and direction (speed, direction) for a given month,day,hour
class Windspeed():
    def __init__(self) -> None:
        self.counter = 0
        self.speed = 0
        self.direction = 0

    # call get_speed to get the speed and direction for a given month day and hour
    def get_speed(self, month, day, start_hour):
        for row in array:
            self.counter += 1
            if int(row[0]) == month and int(row[1]) == day and int(row[2]) == start_hour:
                self.speed = row[3]
                self.direction = row[4]
                return self.speed,self.direction

    # Account for noise / slight variations in speed across wind turbines
    def update(self):
        self.speedu = round(self.speed * random.uniform(0.95,1.05),2)
        self.directionu = round(self.direction * random.uniform(0.95,1.05),2)
        return self.speedu, self.directionu

    # call update_hour only after get_speed. Updates the widn speed and direction by an hour when called. If get_speed is not called then default is the 1/1 hour 0
    def update_hour(self):
        self.counter += 1
        if self.counter > 8760:
            self.counter = 0
        self.speed = array[self.counter, 3]
        self.direction = array[self.counter, 4]
        return self.speed,self.direction
