


# Takes in a list of windmills and number of drones and boat location


# Expect windmills to be a list of windmill objects


# Returns a schedule for the drones

from cmath import inf
from traceback import print_tb
from ortools.sat.python import cp_model
import random

class SchedulerCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        pass


class BoatScheduler:
    def __init__(self, windmills:list, x_bound:int, y_bound:int, boat_range:int, max_boat_speed:int, faulty_windmills_index:list,horizon=100,return_to_coastal=True,start_at_coastal=True,coastal=(0,0)):
        self._model=cp_model.CpModel()
        self._windmills=windmills
        self._horizon=horizon
        self.__return_to_coastal=return_to_coastal
        self.__start_at_coastal=start_at_coastal
        self._x_bound=x_bound
        self._y_bound=y_bound
        self._boat_range=boat_range
        self._max_boat_speed=max_boat_speed
        self._coastal=coastal
        self._faulty_windmills_index=faulty_windmills_index

        self._x_pos=[]
        self._y_pos=[]
        
    def _start_at_coastal(self):
        self._model.Add(self._x_pos[0]==self._coastal[0])
        self._model.Add(self._y_pos[0]==self._coastal[1])

    def _return_to_coastal(self):
        self._model.Add(self._x_pos[self._horizon-1]==self._coastal[0])
        self._model.Add(self._y_pos[self._horizon-1]==self._coastal[1])

    def _set_pace(self):
        for time in range(self._horizon-1):
            x_max_diff=self._model.NewIntVar(0,self._max_boat_speed,'x_max_diff'+str(time))
            y_max_diff=self._model.NewIntVar(0,self._max_boat_speed,'y_max_diff'+str(time))
            # a^2+b^2<=c^2
            # Get distance between two points
            self._model.AddAbsEquality(x_max_diff,self._x_pos[time+1]-self._x_pos[time])
            self._model.AddAbsEquality(y_max_diff,self._y_pos[time+1]-self._y_pos[time])
            # Square a and b
            x_max_squared=self._model.NewIntVar(0,self._max_boat_speed**2,'x_max_squared'+str(time))
            y_max_squared=self._model.NewIntVar(0,self._max_boat_speed**2,'y_max_squared'+str(time))
            self._model.AddMultiplicationEquality(x_max_squared,[x_max_diff,x_max_diff])
            self._model.AddMultiplicationEquality(y_max_squared,[y_max_diff,y_max_diff])
            # Check if the distance is greater than 5m/s
            self._model.Add(x_max_squared+y_max_squared<=self._max_boat_speed**2)

    def _go_through_broken_windmills(self):
        # For every broken windmill
        for index_broken_windmill in self._faulty_windmills_index:
            bools=[]
            for time in range(self._horizon):
                broken_windmill_bool=self._model.NewBoolVar('broken_windmill'+str(index_broken_windmill)+'_'+str(time))
                # X^2 + Y^2 <= radius^2
                # radius_constraint_x
                radius_constraint_x=self._model.NewIntVar(0,self._x_bound**2,'radius_constraint_x'+str(index_broken_windmill)+'_'+str(time))
                # radius_constraint_x_diffrence
                radius_constraint_x_difference=self._model.NewIntVar(-self._x_bound,self._x_bound,'radius_constraint_x_difference'+str(index_broken_windmill)+'_'+str(time))
                
                # radius_constraint_y
                radius_constraint_y=self._model.NewIntVar(0,self._y_bound**2,'radius_constraint_y'+str(index_broken_windmill)+'_'+str(time))
                # radius_constraint_y_diffrence
                radius_constraint_y_difference=self._model.NewIntVar(-self._y_bound,self._y_bound,'radius_constraint_y_difference'+str(index_broken_windmill)+'_'+str(time))
                
                #    Calculate the difference between the windmill and the boat
                #  radius_constraint_x_diffrence=windmill_x - boat_x
                self._model.Add(radius_constraint_x_difference==(self._x_pos[time]-self._windmills[index_broken_windmill][0]))

                # radius_constraint_x=radius_constraint_x_diffrence^2
                self._model.AddMultiplicationEquality(radius_constraint_x,[radius_constraint_x_difference,radius_constraint_x_difference])

                # radius_constraint_y_diffrence=windmill_y - boat_y
                self._model.Add(radius_constraint_y_difference==(self._y_pos[time]-self._windmills[index_broken_windmill][1]))

                # radius_constraint_y=radius_constraint_y_diffrence^2
                self._model.AddMultiplicationEquality(radius_constraint_y,[radius_constraint_y_difference,radius_constraint_y_difference])

                # radius_constraint=radius_constraint_x+radius_constraint_y
                self._model.Add(radius_constraint_x+radius_constraint_y<=self._boat_range**2).OnlyEnforceIf(broken_windmill_bool)
                

                bools.append(broken_windmill_bool)

            # We can visit the windmill multiple times but we must visit at least once
            self._model.Add(sum(bools)>=1)
        
    def _set_bonus_windmills(self):
        bonus_windmills=self._model.NewIntVar(0,len(self._windmills),'bonus_windmills')
        bonus_bools=[]
        for index_of_windmill in range(len(self._windmills)):
            # Check if the windmill is broken
            if index_of_windmill in self._faulty_windmills_index:
                continue
            bonus_bool=self._model.NewBoolVar('bonus_windmill'+str(index_of_windmill))
            bonus_bools.append(bonus_bool)
            reached_bools=[]
            for time in range(self._horizon):
                reached=self._model.NewBoolVar('reached_windmill'+str(index_of_windmill)+'_'+str(time))

                # X^2 + Y^2 <= radius^2
                # radius_constraint_x
                radius_constraint_x=self._model.NewIntVar(0,self._x_bound**2,'radius_reached_constraint_x'+str(index_of_windmill)+'_'+str(time))
                # radius_constraint_x_diffrence
                radius_constraint_x_diffrence=self._model.NewIntVar(-self._x_bound,self._x_bound,'radius_reached_constraint_x_diffrence'+str(index_of_windmill)+'_'+str(time))
                
                # radius_constraint_y
                radius_constraint_y=self._model.NewIntVar(0,self._y_bound**2,'radius_reached_constraint_y'+str(index_of_windmill)+'_'+str(time))
                # # radius_constraint_y_diffrence
                radius_constraint_y_diffrence=self._model.NewIntVar(-self._y_bound,self._y_bound,'radius_reached_constraint_y_diffrence'+str(index_of_windmill)+'_'+str(time))
                
                #    Calculate the difference between the windmill and the boat
                #  radius_constraint_x_diffrence=windmill_x - boat_x
                self._model.Add(radius_constraint_x_diffrence==(self._x_pos[time]-self._windmills[index_of_windmill][0]))

                # radius_constraint_x=radius_constraint_x_diffrence^2
                self._model.AddMultiplicationEquality(radius_constraint_x,[radius_constraint_x_diffrence,radius_constraint_x_diffrence])

                # radius_constraint_y_diffrence=windmill_y - boat_y
                self._model.Add(radius_constraint_y_diffrence==(self._y_pos[time]-self._windmills[index_of_windmill][1]))

                # radius_constraint_y=radius_constraint_y_diffrence^2
                self._model.AddMultiplicationEquality(radius_constraint_y,[radius_constraint_y_diffrence,radius_constraint_y_diffrence])

                # radius_constraint=radius_constraint_x+radius_constraint_y
                self._model.Add(radius_constraint_x+radius_constraint_y<=self._boat_range**2).OnlyEnforceIf(reached)
                reached_bools.append(reached)
            self._model.Add(sum(reached_bools)>=1).OnlyEnforceIf(bonus_bool)
        self._model.Add(bonus_windmills==sum(bonus_bools))
        return bonus_windmills
    
    def _init_pos(self):
        for time in range(self._horizon):
            # Horizon (x,y)
            self._x_pos.append(self._model.NewIntVar(0,self._x_bound,'boat_x'+str(time)))
            self._y_pos.append(self._model.NewIntVar(0,self._y_bound,'boat_y'+str(time)))

    def setup_model(self) -> cp_model.CpModel:
        # Init the pos
        self._init_pos()
        # Start at the coastal location
        if self.__start_at_coastal:
            self._start_at_coastal()
        
        # Return to coastal if specified
        if self.__return_to_coastal:
            self._return_to_coastal()
        
        # Set pace 
        self._set_pace()

        # Go through each broken windmill once
        self._go_through_broken_windmills()

        # Set bonus windmills
        self._bonus_windmills=self._set_bonus_windmills()

        # Maximize the number of windmills visited
        self._model.Maximize(self._bonus_windmills)
    
        return self._model
        
            




# Run two solvers
# 1. Solve a path which passes through all the windmills which are faulty and pass through as many windmills as possible with a range
# 2. With path of base now known lets solve when a drone should be deployed and return



####### Example

horizon=30
boatmodel = cp_model.CpModel()
x_bound,y_bound=10,10
boat_range=1
max_boat_speed=2
windmills=[]
num_windmills=10
num_faulty_windmills=2
index_of_faulty_windmills=[]

random.seed(1)

###### DATA

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


# Scheduler
boat=BoatScheduler(windmills,x_bound,y_bound,boat_range,max_boat_speed,index_of_faulty_windmills,horizon,True,True,(0,0))
model=boat.setup_model()

solver = cp_model.CpSolver()
status = solver.Solve(model)
print(status==cp_model.FEASIBLE,status==cp_model.OPTIMAL)
# Loop through time horizon
for time in range(horizon):
    # Print location
    print(solver.Value(boat._x_pos[time]),solver.Value(boat._y_pos[time]))

print(solver.Value(boat._bonus_windmills))





