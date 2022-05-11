from math import atan2, sqrt, cos, sin, pow

import numpy as np

from enum import Enum


class VehicleStates(Enum):
    # Move state - Will move to a location
    MOVESTATE = 0
    # Detect state - Will inspect a windmill
    DETECTSTATE = 1
    # Hold state - Will hold the current location
    HOLDSTATE = 2
    # Return state - will return to launch location
    RETURNSTATE = 3


class Vehicle:

    # ID
    Vehicle_num = 0

    def __init__(self):
        # set a default name
        self.name = "Vehicle_" + str(Vehicle.Vehicle_num)
        Vehicle.Vehicle_num += 1
        # max velocity
        self.abs_max_velocity = 0
        # Communication range
        self.communication_range = 0
        # Current position X left Y up Z down
        self.pos = (0, 0, 0)
        # History of positions
        self.pos_history = []
        # Current state
        self.state = VehicleStates.HOLDSTATE
        # New state
        self.new_state = None
        # History of states
        self.state_history = []
        # Fuel level
        self.fuel_level = 0

    def set_hold_state(self):
        self.new_state = VehicleStates.HOLDSTATE

    def set_move_state(self):
        self.new_state = VehicleStates.MOVESTATE

    def set_detect_state(self):
        self.new_state = VehicleStates.DETECTSTATE

    def set_return_state(self):
        self.new_state = VehicleStates.RETURNSTATE

    def step(self):
        if self.new_state is not None and self.new_state != self.state:
            self.state = self.new_state
            # Add to history
            self.state_history.append(self.state)
            # And clear the new state
            self.new_state = None

    def move(self, destination):
        # Get current position
        current_pos = self.pos[:2]
        # Add to history
        self.pos_history.append(current_pos)

        # Find the difference between the current position and the destination
        diff = np.array(destination) - np.array(current_pos)

        theta = atan2(diff[1], diff[0])
        distance = sqrt(pow(diff[0], 2) + pow(diff[1], 2))
        distance = min(distance, self.abs_max_velocity)
        opp = distance * cos(theta)
        adj = distance * sin(theta)
        # Convert to tuple
        new_pos = (current_pos[0] + opp, current_pos[1] + adj, 0)

        # Update the position
        self.pos = new_pos
        # If new position is the same as destination then return true
        return self.pos == destination

    def __repr__(self) -> str:
        str(self)
