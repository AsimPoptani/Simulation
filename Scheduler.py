


# Takes in a list of windmills and number of drones and boat location


# Expect windmills to be a list of windmill objects


# Returns a schedule for the drones

from cmath import inf
from traceback import print_tb
from ortools.sat.python import cp_model
import random

class Scheduler(cp_model.CpSolverSolutionCallback):
    def __init__(self, windmills, drones, boat,horizon):
        cp_model.CpSolverSolutionCallback.__init__(self)

        self.windmills = windmills
        self.drones = drones
        self.boat = boat
        # How many steps to solve for
        self.horizon = horizon
    
    # Works the distance between two points
    def work_distance( pos1, pos2)->int:
        # Take the pythagorean distance (x,y)
        print(pos1,pos2)
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


# Run two solvers
# 1. Solve a path which passes through all the windmills which are faulty and pass through as many windmills as possible with a range
# 2. With path of base now known lets solve when a drone should be deployed and return


horizon=150
boatmodel = cp_model.CpModel()
x_bound,y_bound=10,10
boat_range=2
max_boat_speed=1
x_pos=[]
y_pos=[]
windmills=[]
num_windmills=10
num_faulty_windmills=2
index_of_faulty_windmills=[]

random.seed(1)

# Create windmills randomly
for i in range(num_windmills):
    x=random.randint(0,x_bound)
    y=random.randint(0,y_bound)
    # Check if the windmill is already there
    while (x,y) in windmills:
        x=random.randint(0,x_bound)
        y=random.randint(0,y_bound)
    windmills.append((x,y))

for i in range(num_faulty_windmills):
    # Choose a random index of windmills
    index=random.randint(0,num_windmills-1)
    # Check if the windmill index is already there
    while index in index_of_faulty_windmills:
        index=random.randint(0,num_windmills-1)
    index_of_faulty_windmills.append(index)

# Time, position
for time in range(horizon):
    # Horizon (x,y)
    x_pos.append(boatmodel.NewIntVar(0,x_bound,'boat_x'+str(time)))
    y_pos.append(boatmodel.NewIntVar(0,y_bound,'boat_y'+str(time)))


# Set coastal location
boatmodel.Add(x_pos[0]==0)
boatmodel.Add(y_pos[0]==0)


x_pos_const=[]
y_pos_const=[]
# Loop through windmills and set to Constant
for i in range(num_windmills):
    x_pos_const.append(boatmodel.NewConstant(windmills[i][0]))
    y_pos_const.append(boatmodel.NewConstant(windmills[i][1]))

print(windmills,index_of_faulty_windmills)
# For every broken windmill
for i in index_of_faulty_windmills:
    bools=[]
    for time in range(horizon):
        broken_windmill_bool=boatmodel.NewBoolVar('broken_windmill'+str(i)+'_'+str(time))
        # Todo change so it works on a radius
        boatmodel.Add(x_pos[time]==windmills[i][0]).OnlyEnforceIf(broken_windmill_bool)
        boatmodel.Add(y_pos[time]==windmills[i][1]).OnlyEnforceIf(broken_windmill_bool)
        

        bools.append(broken_windmill_bool)

    # TODO change to how many it can reach
    boatmodel.Add(sum(bools)>=1)

bonus_windmills=boatmodel.NewIntVar(0,num_windmills,'bonus_windmills')

bonus_bools=[]
for i in range(num_windmills):
    # Check if the windmill is broken
    if i in index_of_faulty_windmills:
        continue
    bonus_bool=boatmodel.NewBoolVar('bonus_windmill'+str(i)+'_'+str(time))
    bonus_bools.append(bonus_bool)
    reached_bools=[]
    for time in range(horizon):
        reached=boatmodel.NewBoolVar('reached_windmill'+str(i)+'_'+str(time))
        # Todo change so it works on a radius
        boatmodel.Add(x_pos[time]==windmills[i][0]).OnlyEnforceIf(reached)
        boatmodel.Add(y_pos[time]==windmills[i][1]).OnlyEnforceIf(reached)
        reached_bools.append(reached)
    boatmodel.Add(sum(reached_bools)>=1).OnlyEnforceIf(bonus_bool)
        

boatmodel.Add(bonus_windmills==sum(bonus_bools))


# The boat can only go a certain pace of 5m/s
# Make sure that each time step is at max 5m/s
for time in range(horizon-1):
    x_max_diff=boatmodel.NewIntVar(0,max_boat_speed,'x_max_diff'+str(time))
    y_max_diff=boatmodel.NewIntVar(0,max_boat_speed,'y_max_diff'+str(time))
    # Get distance between two points
    boatmodel.AddAbsEquality(x_max_diff,x_pos[time+1]-x_pos[time])
    boatmodel.AddAbsEquality(y_max_diff,y_pos[time+1]-y_pos[time])
    # Check if the distance is greater than 5m/s
    boatmodel.Add(x_max_diff+y_max_diff<=max_boat_speed)

boatmodel.Maximize(bonus_windmills)
# print(boatmodel)
solver = cp_model.CpSolver()
status = solver.Solve(boatmodel)
print(status==cp_model.FEASIBLE,status==cp_model.OPTIMAL)
# Loop through time horizon
for time in range(horizon):
    # Print location
    print(solver.Value(x_pos[time]),solver.Value(y_pos[time]))

print(solver.Value(bonus_windmills))




