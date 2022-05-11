from States import VehicleStates
from config import COASTAL_LOCATION, DRONE_MAX_VELOCITY, DRONE_MAX_COMMUNICATION_RANGE, DRONE_MAX_BATTERY, DRONE_RADIUS
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
import Sprite
import numpy as np
import pygame
from math import inf, sqrt, pow, atan2, sin, cos


class Submersive:

    # ID
    Submersive_num = 0

    def __init__(self, name=None, start_pos=(0, 0, 0)):

        # If no name is given, generate  one
        if name is None:
            self.name = "Submersive_" + str(Submersive.Submersive_num)
            Submersive.Submersive_num += 1
            print(f"No name given, generating {self.name}")
        else:
            self.name = name

        # max velocity
        self.abs_max_velocity = DRONE_MAX_VELOCITY
        # Communication range
        self.communication_range = DRONE_MAX_COMMUNICATION_RANGE
        # Current position X left Y up Z down
        self.pos = start_pos
        # History of positions
        self.pos_history = []
        # Current state
        self.state = VehicleStates.HOLDSTATE
        # New state
        self.new_state = None
        # New position
        self.new_pos = None
        # History of states
        self.state_history = []
        # Battery level
        self.battery_level = DRONE_MAX_BATTERY
        #
        self.target = None
        self.detection_time = 0

    def detect(self):
        if self.detection_time > 0:
            self.detection_time -= 1
        else:
            self.target.faults = []

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

    def step(self):
        if self.new_state is not None and self.new_state != self.state:
            self.state = self.new_state
            # Add to history
            self.state_history.append(self.state)
            # And clear the new state
            self.new_state = None

        if self.state == VehicleStates.HOLDSTATE:
            # Do nothing
            pass
        elif self.state == VehicleStates.MOVESTATE:
            if self.target is not None:
                if self.target.collision(self.pos[0], self.pos[1], DRONE_RADIUS):
                    self.set_detect_state()
                else:
                    self.move(self.target.pos[:2])
        elif self.state == VehicleStates.DETECTSTATE:
            if self.target.has_fault():
                self.detect()
            else:
                self.target = None
                self.set_return_state()
        elif self.state == VehicleStates.RETURNSTATE:
            if self.pos[:2] != COASTAL_LOCATION:
                self.move(COASTAL_LOCATION)
            else:
                self.set_hold_state()

    def set_target(self, destination):
        if destination is not None:
            self.target = destination
            self.set_move_state()

    def set_hold_state(self):
        self.new_state = VehicleStates.HOLDSTATE

    def set_move_state(self):
        self.new_state = VehicleStates.MOVESTATE

    def set_detect_state(self):
        self.new_state = VehicleStates.DETECTSTATE
        for fault in self.target.faults:
            self.detection_time += fault["timeToDetect"]

    def set_return_state(self):
        self.new_state = VehicleStates.RETURNSTATE

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
        if self.submersive.state == VehicleStates.HOLDSTATE:
            self.image = pygame.image.load('./sprites/subblack.png')
        elif self.submersive.state == VehicleStates.MOVESTATE:
            self.image = pygame.image.load('./sprites/subred.png')
        elif self.submersive.state == VehicleStates.DETECTSTATE:
            self.image = pygame.image.load('./sprites/subgreen.png')
        elif self.submersive.state == VehicleStates.RETURNSTATE:
            self.image = pygame.image.load('./sprites/subred.png')
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
