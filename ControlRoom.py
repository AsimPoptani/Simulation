from math import inf, sqrt

from Windmill import Windmill
from config import COASTAL_LOCATION


def get_highest_priority_for_windmill(windmill):
    priority = 0
    for fault in windmill.faults:
        # if this fault has a higher priority than the other faults seen so far for this turbine
        if priority < fault["priority"]:
            # set this turbine's priority to this new maximum
            priority = fault["priority"]
    return priority


def distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


class ControlRoom:

    def __init__(self, vehicle, windfarm: list[Windmill]):
        self.vehicle = vehicle
        self.windfarm = windfarm
        self.destinations = []
        self.pos = COASTAL_LOCATION

    def scan_farm(self):
        # select only those turbines that have faults
        windmills = list(filter(lambda x: x.has_fault(), self.windfarm))
        if len(windmills) > 1:
            # sort by distance from the vehicle
            windmills.sort(key=lambda x: distance(self.vehicle.pos[0], self.vehicle.pos[1], x.pos[0], x.pos[1]))
            # sort by fault priority
            windmills.sort(key=lambda x: get_highest_priority_for_windmill(x), reverse=True)
        # check if the destinations have changed
        if windmills != self.destinations:
            # if so update the cache
            self.destinations = windmills
        else:
            # else return an empty list
            windmills = []
        return windmills
