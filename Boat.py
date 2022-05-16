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
from ControlRoom import distance
from Submersive import Submersive
from Vehicle import VehicleStates, Vehicle
from config import COASTAL_LOCATION, DRONE_MAX_COMMUNICATION_RANGE, BOAT_MAX_VELOCITY, BOAT_MAX_FUEL, BOAT_RADIUS, \
    ROTOR_RADIUS, DRONE_MAX_BATTERY, DRONE_MAX_VELOCITY, DRONE_RADIUS
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
import Sprite
import pygame


class Boat(Vehicle):

    # ID 
    Boat_num = 0

    def __init__(self, windfarm: list[Windmill], name=None, start_pos=(*COASTAL_LOCATION, 0)):

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
        # drones
        self.drones = []
        # number of drones deployed
        self.drones_deployed = 0
        # number of drones returned from deployment
        self.drones_returned = 0
        # Copy of entire Windfarm
        self.windfarm = windfarm.copy()

    def set_drones(self, drones):
        self.drones = drones

    def set_drone_returned(self, drone):
        self.drones_returned += 1
        drone.hide = True
        self.drones.append(drone)

    def step(self):
        super().step()

        if self.state == VehicleStates.HOLDSTATE:
            if self.distance_travelled != 0:
                print(self.distance_travelled / 1000, "kilometers")
                self.distance_travelled = 0
                print(self.hours_at_sea, "hours")
                self.hours_at_sea = 0

                print(175 - len(self.windfarm), 'turbines checked.')
                print(len(self.windfarm), 'turbines remain unchecked.')

                if self.fuel_level < BOAT_MAX_FUEL:
                    self.fuel_level += 1
        elif self.state == VehicleStates.MOVESTATE:
            if self.target is not None:
                if type(self.target) is Windmill:
                    if self.move(self.target.pos[:2], BOAT_RADIUS + ROTOR_RADIUS):
                        self.set_detect_state()
                    else:
                        self.hours_at_sea += 1
                else:
                    if self.move(self.target, BOAT_RADIUS):
                        self.set_detect_state()
                    else:
                        self.hours_at_sea += 1
        elif self.state == VehicleStates.DETECTSTATE:
            if self.drones_deployed == 0:
                max_distance = (DRONE_MAX_VELOCITY * (DRONE_MAX_BATTERY / 2)) - (DRONE_RADIUS + ROTOR_RADIUS)
                windmills = list(filter(lambda i: distance(self.pos[0], self.pos[1], i.pos[0], i.pos[1]) < max_distance, self.windfarm))
                while len(windmills) > 0 and len(self.drones) > 0:
                    target, windmills = windmills[0], windmills[1:]
                    self.windfarm.remove(target)
                    drone, self.drones = self.drones[0], self.drones[1:]
                    drone.set_target(target)
                    drone.hide = False
                    self.drones_deployed += 1
                self.hours_at_sea += 1
                self.fuel_level -= 1
            if self.drones_returned == self.drones_deployed:
                self.drones_deployed, self.drones_returned = 0, 0
                self.target = None
                self.next_target()
        elif self.state == VehicleStates.RETURNSTATE:
            if self.move(COASTAL_LOCATION, BOAT_RADIUS):
                self.set_hold_state()
            else:
                self.hours_at_sea += 1
                self.fuel_level -= 1

    def __str__(self) -> str:
        return f"Boat: {self.name} \n {self.pos} with state {self.state}"


class BoatSprite(Sprite.Sprite):

    def __init__(self, boat: Boat):
        super(BoatSprite, self).__init__()
        # Add sprite
        # TODO update image to a new image
        self.image = pygame.image.load('./sprites/boat-black.png')
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
            self.image = pygame.image.load('./sprites/boat-blue.png')
        return self.image

    def getPower(self):
        percentage = (self.boat.fuel_level / BOAT_MAX_FUEL) * 100
        if percentage > (100 + 75) / 2:
            return pygame.image.load('./sprites/battery-100.png')
        elif percentage > (75 + 50) / 2:
            return pygame.image.load('./sprites/battery-75.png')
        elif percentage > (50 + 25) / 2:
            return pygame.image.load('./sprites/battery-50.png')
        elif percentage > 25 / 2:
            return pygame.image.load('./sprites/battery-25.png')
        else:
            return pygame.image.load('./sprites/battery-0.png')

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
