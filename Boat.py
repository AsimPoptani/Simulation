# TODO CHANGE ME TO BOAT WHO CAN CARRY Submersives
# Destination
# Current position
# Current state
# Name
# Maximum velocity
# Fuel
# Fuel consumption
# Home position
# Communication drone range
# drones
# max_drones_capacity

# Class functions
# 
# Recive a path of points[x,y]
# Deploy drone (destinations[],rendevous[])
# Recieve drone
# Charge drone
from Vehicle import VehicleStates, Vehicle
from config import COASTAL_LOCATION, DRONE_MAX_COMMUNICATION_RANGE, BOAT_MAX_VELOCITY, BOAT_MAX_FUEL, BOAT_RADIUS
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
import Sprite
import pygame


class Boat(Vehicle):

    # ID 
    Boat_num = 0

    def __init__(self, name=None, start_pos=(*COASTAL_LOCATION, 0)):

        # initialise inherited values
        super(Boat, self).__init__()

        # If no name is given, generate  one
        if name is None:
            self.name = "Boat_" + str(Boat.Boat_num)
            Boat.Boat_num += 1
            print(f"No name given, generating {self.name}")
        else:
            self.name = name

        # max velocity
        self.abs_max_velocity = BOAT_MAX_VELOCITY
        # Communication range
        self.communication_range = DRONE_MAX_COMMUNICATION_RANGE
        # Current position X left Y up Z down
        self.pos = start_pos
        # Fuel level
        self.fuel_level = BOAT_MAX_FUEL

    def step(self):
        super().step()

        if self.state == VehicleStates.HOLDSTATE:
            pass
        elif self.state == VehicleStates.MOVESTATE:
            if self.target is not None:
                if self.target.collision(self.pos[0], self.pos[1], BOAT_RADIUS):
                    self.target = None
                    self.next_target()
                else:
                    self.move(self.target.pos[:2])
        elif self.state == VehicleStates.DETECTSTATE:
            # Boat doesn't do detection
            print('Error', u"shouldn't be in detect state ¯\\_(ツ)_/¯")
        elif self.state == VehicleStates.RETURNSTATE:
            if self.pos[:2] != COASTAL_LOCATION:
                self.move(COASTAL_LOCATION)
            else:
                self.set_hold_state()

    def __str__(self) -> str:
        return f"Boat: {self.name} \n {self.pos} with state {self.state}"


class BoatSprite(Sprite.Sprite):

    def __init__(self, boat: Boat):
        super(BoatSprite, self).__init__()
        # Add sprite
        # TODO update image to a new image
        self.image = pygame.image.load('./sprites/subblack.png')
        self.rect = self.image.get_rect()
        self.boat = boat

    def getSprite(self):
        if self.boat.state == VehicleStates.HOLDSTATE:
            self.image = pygame.image.load('./sprites/boat-black.png')
        elif self.boat.state == VehicleStates.MOVESTATE:
            self.image = pygame.image.load('./sprites/boat-red.png')
        elif self.boat.state == VehicleStates.DETECTSTATE:
            self.image = pygame.image.load('./sprites/boat-green.png')
        elif self.boat.state == VehicleStates.RETURNSTATE:
            self.image = pygame.image.load('./sprites/boat-red.png')
        return self.image

    def getPower(self):
        return pygame.image.load('./sprites/battery-100.png')

    def getPosition(self):
        x = x_to_pixels(self.boat.pos[0])
        y = y_to_pixels(self.boat.pos[1])
        return x, y

    def getName(self):
        text = self.set_text(self.boat.name, 0, 0, 10)[0]
        return text

    def debug(self):
        text = self.set_text(str(self.boat), 0, 0, 10)[0]
        return text
