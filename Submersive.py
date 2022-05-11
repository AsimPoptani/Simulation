
from config import COASTAL_LOCATION, DRONE_MAX_VELOCITY, DRONE_MAX_COMMUNICATION_RANGE, DRONE_MAX_BATTERY, DRONE_RADIUS
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
import Sprite
import numpy as np
from enum import Enum
import pygame
from math import inf, sqrt, pow, atan2, sin, cos


class SubmersiveStates(Enum):
    MOVESTATE = 0
    DETECTSTATE = 1
    HOLDSTATE = 2

class Submersive():
    # A submersive has sevral states

    #####
    ### Move state - Will move to a location 
    ### Detect state - Will detect if a windmill is broken
    ### Hold state - Will hold the current location
    ####

    # Move State
    # For now we assume that it takes one step to move 1m in any direction
    # TODO - Add Gausian noise to the movement and variable speed

    # Detect State
    # There is a set number of steps to detect a  broken windmill and is determined by a faults list
    # There is a deterministic time to detect without any faults lets assume it is 50 steps


    # ID 
    Subersive_num=0

    # Standard Detection
    standard_detection_time=50


    def __init__(self, name=None, start_pos=(0, 0, 0)):
        
        # If no name is given, generate  one
        if name is None:
            self.name="Submersive_"+str(Submersive.Subersive_num)
            Submersive.Subersive_num+=1
            print(f"No name given, generating {self.name}")
        else:
            self.name=name
        
        # max velocity
        self.abs_max_velocity = DRONE_MAX_VELOCITY
        self.current_velocity = 0

        # Communication range
        self.communication_range = DRONE_MAX_COMMUNICATION_RANGE

        # Current position X left Y up Z down
        self.pos=start_pos

        # History of positions
        self.pos_history=[]

        # Current state
        self.state=SubmersiveStates.HOLDSTATE

        # New state
        self.new_state=None

        # New position
        self.new_pos=None

        # History of states
        self.state_history=[]

        # Battery level
        self.battery_level = DRONE_MAX_BATTERY
    
    def detect(self,windmill:Windmill):
        if len(windmill.faults)>0:
            # How long to detect the faults
            detection_time=0
            for fault in windmill.faults:
                detection_time+=fault["timeToDetect"]
        else:
            detection_time=Submersive.standard_detection_time
        
        return detection_time
    
    def move(self,destination):
        # Get current position
        current_pos=self.pos
        # Add to history
        self.pos_history.append(current_pos)

        # Find the difference between the current position and the destination
        diff=np.array(destination)-np.array(current_pos)

        theta = atan2(diff[1], diff[0])
        distance = sqrt(pow(diff[0], 2) + pow(diff[1], 2))
        distance = min(distance, self.current_velocity)
        opp = distance * cos(theta)
        adj = distance * sin(theta)
        # Convert to tuple
        new_pos = (current_pos[0] + opp, current_pos[1] + adj, 0)

        # Update the position
        self.pos=new_pos
        # If new position is the same as destination then return true
        if self.pos==destination:
            return True
        return False

    def scan_farm(self, windfarms:list[Windmill]):
        # Where we are going to 
        destination = COASTAL_LOCATION
        # Maximum distance to travel
        smallest_distance = inf
        # Biggest fault 
        max_priority = 0
        for windmill in windfarms:
            # if the drone has reached this windturbine
            if windmill.collision(self.pos[0], self.pos[1], DRONE_RADIUS):
                # and the turbine has a fault, inspect the fault
                if windmill.has_fault():
                    windmill.fix_fault()
            # otherwise, if this turbine has a fault
            elif windmill.has_fault():
                # the maximum priority for this turbine
                priority = 0
                for fault in windmill.faults:
                    # if this fault has a higher priority than the other faults seen so far for this turbine
                    if priority < fault["priority"]:
                        # set this turbine's priority to this new maximum
                        priority = fault["priority"]
                    # if this fault has a higher priority than any other fault for all turbines seen so far
                    if fault["priority"] > max_priority:
                        # set the maximum priority for all turbines to this fault's priority
                        max_priority = fault["priority"]
                        # and reset the smallest distance to the maximum
                        smallest_distance = inf
                # if this turbine's priority os not the maximum, skip
                if priority < max_priority:
                    continue
                # calculate the distance from the drone to this turbine
                x_diff = pow(self.pos[0] - windmill.pos[0], 2)
                y_diff = pow(self.pos[1] - windmill.pos[1], 2)
                distance = sqrt(x_diff + y_diff)
                # if the distance is smaller than smallest distance seen so far
                if distance < smallest_distance:
                    # set this distance to the smallest
                    smallest_distance = distance
                    # and make our current target destination the location of this turbine
                    destination = windmill.pos
        # head to the next destination
        self.set_move_state((*destination, 0))
    
    def step(self,windfarm:list[Windmill]):
        self.scan_farm(windfarm)

        if self.new_state==None:
            print("Error: No new state set, setting to hold state")
            self.set_hold_state()
        elif self.new_state==SubmersiveStates.HOLDSTATE:
            # Do nothing
            self.state=SubmersiveStates.HOLDSTATE
            self.current_velocity = 0
        
        elif self.new_state==SubmersiveStates.MOVESTATE:
            # Check if new position is set
            if self.new_pos is None:
                print("Error: No new position set, reverting to hold state")
                self.state=SubmersiveStates.HOLDSTATE
                self.current_velocity = 0
                
            else:
                # Update state
                self.state = SubmersiveStates.MOVESTATE
                # Move to new position
                self.move(self.new_pos)
            
        elif self.new_state==SubmersiveStates.DETECTSTATE:
            # Check for nearby windmills in range
            windmill_detected=False
            for windmill in windfarm:
                if windmill.position == self.pos:
                    self.detect(windmill)
                    windmill_detected=True
                    self.state=SubmersiveStates.DETECTSTATE
                    break
            if not windmill_detected:
                print("Error: No windmill detected, reverting to hold state")
                self.state=SubmersiveStates.HOLDSTATE
                self.current_velocity = 0
        
        # Add to history
        self.state_history.append(self.state)
        # And clear the new state
        self.new_state=None
    
    def set_hold_state(self):
        self.new_state=SubmersiveStates.HOLDSTATE
    
    def set_move_state(self,destination):
        # Check if destination is the same as position
        if self.pos==destination:
            print("Error: Destination is the same as current position, reverting to hold state")
            self.set_hold_state()
            return
        self.new_state=SubmersiveStates.MOVESTATE
        self.new_pos=destination
        self.current_velocity = self.abs_max_velocity
    
    def set_detect_state(self):
        self.new_state=SubmersiveStates.DETECTSTATE
    
    def __str__(self) -> str:
        return f"Submersive: {self.name} \n {self.pos} with state {self.state}"
    
    def __repr__(self) -> str:
        str(self)

class SubmersiveSprite(Sprite.Sprite):

    def __init__(self, submersive: Submersive):
        super(SubmersiveSprite, self).__init__()
        # Add sprite
        # TODO update image to a new image
        self.image = pygame.image.load('./sprites/subblack.png')
        self.rect = self.image.get_rect()
        self.submersive = submersive

    def getSprite(self):
        if self.submersive.state == SubmersiveStates.HOLDSTATE:
            self.image = pygame.image.load('./sprites/subblack.png')
        elif self.submersive.state == SubmersiveStates.MOVESTATE:
            self.image = pygame.image.load('./sprites/subred.png')
        elif self.submersive.state == SubmersiveStates.DETECTSTATE:
            self.image = pygame.image.load('./sprites/subgreen.png')
        # Merge the text with the sprite put the text above the sprite

        return self.image

    def getPower(self):
        if self.submersive.battery_level > (100 + 75) / 2:
            return pygame.image.load('./sprites/battery-100.png')
        elif self.submersive.battery_level > (75 + 50) / 2:
            return pygame.image.load('./sprites/battery-75.png')
        elif self.submersive.battery_level > (50 + 25) / 2:
            return pygame.image.load('./sprites/battery-50.png')
        elif self.submersive.battery_level > 25 / 2:
            return pygame.image.load('./sprites/battery-25.png')
        else:
            return pygame.image.load('./sprites/battery-0.png')

    def getPosition(self):
        x = x_to_pixels(self.submersive.pos[0])
        y = y_to_pixels(self.submersive.pos[1])
        return x, y

    def getName(self):
        text = self.set_text(self.submersive.name, 0, 0, 10)[0]
        return text

    def debug(self):
        text = self.set_text(str(self.submersive), 0, 0, 10)[0]
        return text
