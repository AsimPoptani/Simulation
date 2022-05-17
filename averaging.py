# Detects which wind turbines are faulty based on the n nearest neighbours
from Windmill import Windmill
from math import sqrt
import numpy as np

def distance(x1, y1, x2, y2):
    """Euclidean distance between to points."""
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

class Averaging():
    # Initialise to get access to the windmill instances
    def __init__(self, windfarm: list[Windmill]) -> None:
        self.windfarm = windfarm
    
    # Check if the target_turbine is faulty based on an averaging algorithm with the nearest n neighbours to that turbine
    # takes the turbine to check and the number of neighbours to compare it to.
    def check_faulty(self,target_turbine,n_neighbours):
        self.target_turbine = target_turbine
        self.distances = []
        self.vibrations = []
        for windmill in self.windfarm:
            self.distances.append(distance(self.target_turbine.pos[:2][0], self.target_turbine.pos[:2][1], windmill.pos[:2][0], windmill.pos[:2][1]))
        iter = list(range(1,len(self.windfarm) + 1))
        distances_with_index =  list(zip(iter,self.distances))
        sorted_list = sorted(distances_with_index, key=lambda x: x[1])
        self.nearest_n_neighbours = sorted_list[:n_neighbours + 1]
        # get vibrations and put them into self.vibrations
        for windmill in self.nearest_n_neighbours:
            self.vibrations.append((self.windfarm[windmill[0] - 1].data["Vibration"]))
        
        selected_turbine_vib = self.vibrations[0]
        self.vibrations.pop(0)
        
        # Check if the target_turbine's vibrations data points are less than the average
        if selected_turbine_vib <= np.mean(self.vibrations) * 1.1:
            return 10
        else:
            diff = selected_turbine_vib - np.mean(self.vibrations)
            prob = min(38 * diff, 99)
            return int(prob)
            
            

