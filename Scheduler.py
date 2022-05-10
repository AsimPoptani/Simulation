# Takes in a list of windmills and number of drones and boat location


# Expect windmills to be a list of windmill objects


# Returns a schedule for the drones

from cmath import inf
from ortools.sat.python import cp_model

# Run two solvers
# 1. Solve a path which passes through all the windmills which are faulty and pass through as many windmills as possible with a range
# 2. With path of base now known lets solve when a drone should be deployed and return




class Scheduler(cp_model.CpSolverSolutionCallback):
    def __init__(self, windmills, drones, boat,horizon):
        cp_model.CpSolverSolutionCallback.__init__(self)

        self.windmills = windmills
        self.drones = drones
        self.boat = boat
        # How many steps to solve for
        self.horizon = horizon
    
    # Works the distance between two points
    def work_distance(self, pos1, pos2)->int:
        # Take the pythagorean distance (x,y)
        return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**0.5
    
    def time_to_point(self, meters, meters_per_second)->int:
        # Check if we are already there
        if meters == 0:
            return 0
        # Check if the speed is 0
        if meters_per_second==0:
            return inf
        # Otherwise return the time
        return meters/meters_per_second



