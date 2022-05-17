


# Takes in a list of windmills and number of drones and boat location


# Expect windmills to be a list of windmill objects


# Returns a schedule for the drones

from cmath import inf
from traceback import print_tb
from ortools.sat.python import cp_model
import random
from tqdm import tqdm

class SchedulerCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        pass

# Windmill [(1,2), (3,4), (5,6)]
# faulty_windmills_index =[0]
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
        for index_of_windmill in tqdm(range(len(self._windmills))):
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
        print('Init the pos')
        self._init_pos()
        # Start at the coastal location
        if self.__start_at_coastal:
            print('Start at the coastal location')
            self._start_at_coastal()
        
        # Return to coastal if specified
        if self.__return_to_coastal:
            print('Return to coastal if specified')
            self._return_to_coastal()
        
        # Set pace 
        print('Set pace')
        self._set_pace()

        # Go through each broken windmill once
        print('Go through each broken windmill once')
        self._go_through_broken_windmills()

        # Set bonus windmills
        print('Set bonus windmills')
        # self._bonus_windmills=self._set_bonus_windmills()

        # Maximize the number of windmills visited
        print('Maximize the number of windmills visited')
        # self._model.Maximize(self._bonus_windmills)

        print('Model setup done')
        return self._model
        
            

class DronesScheduler():
    def __init__(self,num_drones:int,windmills:list,boat_path:list,index_priority_windmills:list,max_distance_from_boat:int,fuel:int,max_fuel:int,charge_rate:int,discharge_rate:int):
        self._num_drones=num_drones
        self._fuel=fuel
        self._windmills=windmills
        self._boat_path=boat_path
        self._charge_rate=charge_rate
        self._discharge_rate=discharge_rate
        self._index_priority_windmills=index_priority_windmills
        self._max_distance_from_boat=max_distance_from_boat
        self._max_fuel=max_fuel
        self._model=cp_model.CpModel()
        self._horizon=len(self._boat_path)
        # 2D array of drones vs horizon representing the position of the drone [(x,y),(x,y),...]
        self.drone_positions=[]
        # 2D array of drones vs horizon representing if the drone is on the boat
        self.drone_boat=[]
        # 2D array of drones vs horizon with fuel
        self.drone_fuel=[]
        # 2D array of drones vs horizon with the distance from the boat
        self.drone_distance_from_boat=[]

    def _init_drones(self):    
        # Create a 2D array of drones vs horizon representing the position of the drone [(x,y),(x,y),...]
        for drone in range(self._num_drones):
            # loop through the horizon
            drone_positions=[]
            for time in range(self._horizon):
                # Create x,y
                x=self._model.NewIntVar(0,self._max_distance_from_boat,'drone_x'+str(drone)+'_'+str(time))
                y=self._model.NewIntVar(0,self._max_distance_from_boat,'drone_y'+str(drone)+'_'+str(time))
                drone_positions.append((x,y))
            self.drone_positions.append(drone_positions)
                
        # Create a 2D array of drones vs horizon representing if the drone is on the boat
        for drone in range(self._num_drones):
            # loop through the horizon
            drone_boat=[]
            for time in range(self._horizon):
                # Create bool
                drone_boat.append(self._model.NewBoolVar('drone_boat'+str(drone)+'_'+str(time)))
            self.drone_boat.append(drone_boat)

        # Create a 2D array of drones vs horizon with fuel
        for drone in range(self._num_drones):
            # loop through the horizon
            drone_fuel=[]
            for time in range(self._horizon):
                # Create fuel
                drone_fuel.append(self._model.NewIntVar(0,self._max_fuel,'drone_fuel'+str(drone)+'_'+str(time)))
            self.drone_fuel.append(drone_fuel)
        
    def _on_boat_constraint(self):
        # If on the boat the drone moves to the next position the boat goes to
        for drone in range(self._num_drones):
            for time in range(self._horizon-1):
                # bool x and y
                x_bool=self._model.NewBoolVar('x_bool_boat_'+str(drone)+'_'+str(time))
                y_bool=self._model.NewBoolVar('y_bool_boat_'+str(drone)+'_'+str(time))
                # Next position is the next boat position
                self._model.Add(self.drone_positions[drone][time+1][0]==self._boat_path[time+1][0]).OnlyEnforceIf(x_bool)
                self._model.Add(self.drone_positions[drone][time+1][1]==self._boat_path[time+1][1]).OnlyEnforceIf(y_bool)
                self._model.AddBoolAnd([x_bool,y_bool]).OnlyEnforceIf(self.drone_boat[drone][time])
                


    def _fuel_constraint(self):
        # If on the boat the drone can charge up to the max fuel
        # If max fuel is reached then max fuel is maintained
        # If not on the boat the drone discharges fuel
        for drone in range(self._num_drones):
            for time in range(self._horizon-1):
                charged=self._model.NewBoolVar('drone_charged'+str(drone)+'_'+str(time))
                # Charge
                self._model.Add(self.drone_fuel[drone][time+1]==self.drone_fuel[drone][time]+self._charge_rate).OnlyEnforceIf(self.drone_boat[drone][time]).OnlyEnforceIf(charged.Not())
                # Max fuel and on the boat
                self._model.Add(self.drone_fuel[drone][time+1]==self._max_fuel).OnlyEnforceIf(self.drone_boat[drone][time]).OnlyEnforceIf(charged)
                # Discharge
                self._model.Add(self.drone_fuel[drone][time+1]==self.drone_fuel[drone][time]-self._discharge_rate).OnlyEnforceIf(self.drone_boat[drone][time].Not())

    def _on_boat_before_coast(self):
        # The drone must be on the boat before the horizon
        for drone in range(self._num_drones):

            pass

    def _max_speed(self):
        # The drone cannot move faster than the max speed
        pass

    def _max_distance_from_boat_constraint(self):
        # a^2+b^2=c^2
        # Calculate the distance from drone to boat and put in 
        pass

    def _reach_broken_windmill(self):
        # The drones must reach every broken windmills
        # Only one drone can reach a windmill
        pass




    def setup(self):
        # Init the drone positions
        self._init_drones()
        # Set max speed
        self._max_speed()
        # Set on boat constraint
        self._on_boat_constraint()
        # Set fuel constraint
        self._fuel_constraint()
        # Set on boat before coast
        self._on_boat_before_coast()
        # Set max distance from boat
        self._max_distance_from_boat_constraint()
        # Set reach broken windmill
        self._reach_broken_windmill()


# Run two solvers
# 1. Solve a path which passes through all the windmills which are faulty and pass through as many windmills as possible with a range
# 2. With path of base now known lets solve when a drone should be deployed and return



####### Example

# horizon=30
# boatmodel = cp_model.CpModel()
# x_bound,y_bound=10,10
# boat_range=1
# max_boat_speed=2
# windmills=[]
# num_windmills=10
# num_faulty_windmills=2
# index_of_faulty_windmills=[]

# random.seed(1)

# ###### DATA

# # Create windmills randomly
# for i in range(num_windmills):
#     x=random.randint(0,x_bound)
#     y=random.randint(0,y_bound)
#     # Check if the windmill is already there
#     while (x,y) in windmills:
#         x=random.randint(0,x_bound)
#         y=random.randint(0,y_bound)
#     windmills.append((x,y))

# for i in range(num_faulty_windmills):
#     # Choose a random index of windmills
#     index=random.randint(0,num_windmills-1)
#     # Check if the windmill index is already there
#     while index in index_of_faulty_windmills:
#         index=random.randint(0,num_windmills-1)
#     index_of_faulty_windmills.append(index)


# # Scheduler
# boat=BoatScheduler(windmills,x_bound,y_bound,boat_range,max_boat_speed,index_of_faulty_windmills,horizon,True,True,(0,0))
# model=boat.setup_model()

# solver = cp_model.CpSolver()
# status = solver.Solve(model)
# print(status==cp_model.FEASIBLE,status==cp_model.OPTIMAL)
# # Loop through time horizon
# #  x_pos and y_pos into boat_path [(x,y),(x,y),...]
# boat_path=[]
# for time in range(horizon):
#     boat_path.append((solver.Value(boat._x_pos[time]),solver.Value(boat._y_pos[time])))

# print(boat_path)

# drone_scheduler=DronesScheduler(num_drones=1,windmills=windmills,boat_path=boat_path,index_priority_windmills=index_of_faulty_windmills,max_distance_from_boat=10,fuel=10,max_fuel=10,charge_rate=1,discharge_rate=2)
# drone_scheduler.setup()
# print(drone_scheduler._model)
