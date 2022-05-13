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
    """Euclidean distance between to points."""
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


class ControlRoom:

    def __init__(self, vehicle, windfarm: list[Windmill]):
        self.vehicle = vehicle
        self.windfarm = windfarm
        self.destinations = []
        self.pos = COASTAL_LOCATION

    def scan_farm(self):
        """return an ordered list of turbines sorted by distance and priority."""
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
            windmills = []
        return windmills

    def traverse_farm(self):
        """traverse entire wind farm in order, stopping at each turbine (adds a tick each time)."""
        # clone the wind farm into a new list
        windmills = self.windfarm.copy()
        return windmills

    def traverse_farm_edges(self):
        """traverse entire wind farm in order,
        stopping only at the turbines at the end of each row (adds a tick each time)."""
        windmills = []
        for i in [0, 3, 4, 7, 8, 17, 18, 30, 31, 48, 49, 67, 68, 87, 88, 108, 109, 130, 131, 152, 153, 163, 164, 170, 171, 174]:
            windmills.append(self.windfarm[i])
        return windmills

    def furthest(self, furthest=True):
        """return the furthest turbine from the coastal start point, or the nearest if 'furthest' keyword is False."""
        return furthest(COASTAL_LOCATION, furthest=furthest)

    def furthest(self, position, furthest=True):
        """return the furthest turbine from the given position, or the nearest if 'furthest' keyword is False."""
        # clone the wind farm into a new list
        windmills = self.windfarm.copy()
        # sort by distance to coastal start point
        windmills.sort(key=lambda x: distance(position[0], position[1], x.pos[0], x.pos[1]), reverse=furthest)
        # we only want the first item
        windmills = [windmills[0]]
        return windmills
