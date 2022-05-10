import math

from config import COASTAL_LOCATION, DRONE_RADIUS
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
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


    def __init__(self,name=None,communication_range=10,detection_range=10,start_pos=(0,0,0), abs_max_velocity=1000, battery_level=1000):
        
        # If no name is given, generate  one
        if name is None:
            self.name="Submersive_"+str(Submersive.Subersive_num)
            Submersive.Subersive_num+=1
            print(f"No name given, generating {self.name}")
        else:
            self.name=name
        
        # max velocity
        self.abs_max_velocity=abs_max_velocity

        # Communication range
        self.communication_range=communication_range

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
        self.battery_level=battery_level
    
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
        distance = min(distance, self.abs_max_velocity)
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
        destination = COASTAL_LOCATION
        smallest_distance = inf
        max_priority = 0
        for windmill in windfarms:
            if windmill.collision(self.pos[0], self.pos[1], DRONE_RADIUS):
                if windmill.has_fault():
                    windmill.fix_fault()
                else:
                    print("cRaSh !!")
            if windmill.has_fault():
                priority = 0
                for fault in windmill.faults:
                    if priority < fault["priority"]:
                        priority = fault["priority"]
                    if fault["priority"] > max_priority:
                        max_priority = fault["priority"]
                        smallest_distance = inf
                if priority < max_priority:
                    continue
                x_diff = pow(self.pos[0] - windmill.pos[0], 2)
                y_diff = pow(self.pos[1] - windmill.pos[1], 2)
                diff = x_diff + y_diff
                distance = sqrt(diff)
                if distance < smallest_distance:
                    smallest_distance = distance
                    destination = windmill.pos
        self.set_move_state((*destination, 0))
    
    def step(self,windfarm:list[Windmill]):
        self.scan_farm(windfarm)

        if self.new_state==None:
            print("Error: No new state set, setting to hold state")
            self.new_state=SubmersiveStates.HOLDSTATE
        elif self.new_state==SubmersiveStates.HOLDSTATE:
            # Do nothing
            self.state=SubmersiveStates.HOLDSTATE
        
        elif self.new_state==SubmersiveStates.MOVESTATE:
            # Check if new position is set
            if self.new_pos is None:
                print("Error: No new position set, reverting to hold state")
                self.state=SubmersiveStates.HOLDSTATE
                
            else:
                # Move to new position
                self.move(self.new_pos)
                # Update state
                self.state=SubmersiveStates.MOVESTATE
            
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
            self.new_state=SubmersiveStates.HOLDSTATE
            return
        self.new_state=SubmersiveStates.MOVESTATE
        self.new_pos=destination
    
    def set_detect_state(self):
        self.new_state=SubmersiveStates.DETECTSTATE
    
    def __str__(self) -> str:
        return f"Submersive: {self.name} \n {self.pos} with state {self.state}"
    
    def __repr__(self) -> str:
        str(self)

            

def set_text(string, coordx, coordy, fontSize): #Function to set text
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)                  



class SubmersiveSprite(pygame.sprite.Sprite):
    def __init__(self,submersive:Submersive):
        super(SubmersiveSprite,self).__init__()
        # Add sprite
        self.image = pygame.image.load('./sprites/subblack.png')
        self.rect = self.image.get_rect()
        self.submersive=submersive
    
    def getSprite(self):
        if self.submersive.state==SubmersiveStates.HOLDSTATE:
            self.image = pygame.image.load('./sprites/subblack.png')
        elif self.submersive.state==SubmersiveStates.MOVESTATE:
            self.image = pygame.image.load('./sprites/subred.png')
        elif self.submersive.state==SubmersiveStates.DETECTSTATE:
            self.image = pygame.image.load('./sprites/subgreen.png')
        # Merge the text with the sprite put the text above the sprite
        

        return self.image
        # return 
    
    def getPosition(self):
        x = x_to_pixels(self.submersive.pos[0])
        y = y_to_pixels(self.submersive.pos[1])
        return x, y
    
    def getName(self):
        text=set_text(self.submersive.name,0,0,10)[0]
        return text
    
    def debug(self):
        text=set_text(str(self.submersive),0,0,10)[0]
        return text