# Detects which wind turbines are faulty based on the n nearest neighbours
from Windmill import Windmill
from config import ROTOR_RADIUS, MAX_POWER, AIR_DENSITY, TURBINE_HEIGHT
from math import sqrt
import numpy as np

POWER_COEFFICIENT = 0.4

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
        # Use median to prevent being masssively affected by outliers
        diff = selected_turbine_vib - np.median(self.vibrations)
        prob = round(max(0,min(20 * diff, 99)))
        if selected_turbine_vib > 3:
            prob += 10

        area = np.pi * (ROTOR_RADIUS**2)
        expected_power = round((0.5 * AIR_DENSITY * area * (self.target_turbine.data["Wind Speed"]**3) * POWER_COEFFICIENT),2)
        expected_power = min(expected_power, MAX_POWER)
        if self.target_turbine.data["Power"] < expected_power:
            prob += 10
        return round(min(prob, 99))
            
            

