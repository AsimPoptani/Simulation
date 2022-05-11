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


class ControlRoom:

    def __init__(self, vehicle, windfarm: list[Windmill]):
        self.vehicle = vehicle
        self.windfarm = windfarm
        self.destination = None
        self.pos = COASTAL_LOCATION

    def get_windmills_with_faults(self):
        windmills = []
        for windmill in self.windfarm:
            if windmill.has_fault():
                windmills.append(windmill)
        return windmills

    def scan_farm(self):
        # Where we are going to
        destination = None
        # Maximum distance to travel
        smallest_distance = inf
        # Biggest fault
        max_priority = 0
        for windmill in self.get_windmills_with_faults():
            # otherwise, if this turbine has a fault
            # the maximum priority for this turbine
            priority = get_highest_priority_for_windmill(windmill)
            # if this fault has a higher priority than any other fault for all turbines seen so fa
            if priority > max_priority:
                # set the maximum priority for all turbines to this fault's priority
                max_priority = priority
                # and reset the smallest distance to the maximum
                smallest_distance = inf
            # if this turbine's priority is not the maximum, skip
            if priority < max_priority:
                continue
            # calculate the distance from the drone to this turbine
            x_diff = pow(self.vehicle.pos[0] - windmill.pos[0], 2)
            y_diff = pow(self.vehicle.pos[1] - windmill.pos[1], 2)
            distance = sqrt(x_diff + y_diff)
            # if the distance is smaller than smallest distance seen so far
            if distance < smallest_distance:
                # set this distance to the smallest
                smallest_distance = distance
                # and make our current target destination the location of this turbine
                destination = windmill
        # head to the next destination
        if destination != self.destination:
            self.destination = destination
        else:
            destination = None
        return destination
