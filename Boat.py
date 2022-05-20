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
from Vehicle import VehicleStates, Vehicle
from config import COASTAL_LOCATION, DRONE_MAX_COMMUNICATION_RANGE, BOAT_MAX_VELOCITY, BOAT_MAX_FUEL, BOAT_RADIUS, \
    ROTOR_RADIUS, MAX_SCAN_DISTANCE, TIME_SCALAR
from display import x_to_pixels, y_to_pixels
from Windmill import Windmill
import Sprite
import pygame

from locations import coastal_location


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
        # for restoring working copy
        self.windfarm_cache = windfarm.copy()

    def set_drones(self, drones):
        self.drones = drones

    def set_drone_returned(self, drone):
        self.drones_returned += 1
        drone.hide = True
        self.drones.append(drone)

    def hold_state(self):
        if self.distance_travelled != 0:
            print(self.distance_travelled / 1000, "kilometers")
            self.distance_travelled = 0
            print(self.hours_at_sea, "hours")
            self.hours_at_sea = 0

            print(175 - len(self.windfarm), 'turbines checked.')
            print(len(self.windfarm), 'turbines remain unchecked.')

            # refresh copy of windfarm
            self.windfarm = self.windfarm_cache.copy()

        if self.fuel_level < BOAT_MAX_FUEL:
            self.fuel_level = min(self.fuel_level + 4 * TIME_SCALAR, BOAT_MAX_FUEL)

    def update_fuel_time(self):
        self.hours_at_sea += 1 * TIME_SCALAR
        self.fuel_level -= 1 * TIME_SCALAR

    def move_state(self):
        if self.target is not None:
            if type(self.target) is Windmill:
                if self.move(self.target.pos[:2], BOAT_RADIUS + ROTOR_RADIUS):
                    self.set_detect_state()
                else:
                    self.update_fuel_time()
            else:
                if self.move(self.target, BOAT_RADIUS):
                    self.set_detect_state()
                else:
                    self.update_fuel_time()

    def detect_state(self):
        if self.drones_deployed == 0:
            max_distance = MAX_SCAN_DISTANCE
            windmills = list(filter(lambda i: distance(*self.pos[:2], *i.pos[:2]) < max_distance, self.windfarm))
            while len(windmills) > 0 and len(self.drones) > 0:
                target, windmills = windmills[0], windmills[1:]
                self.windfarm.remove(target)
                drone, self.drones = self.drones[0], self.drones[1:]
                drone.set_target(target)
                drone.hide = False
                self.drones_deployed += 1
            self.update_fuel_time()
        elif self.drones_returned != self.drones_deployed:
            self.update_fuel_time()
        if self.drones_returned == self.drones_deployed:
            self.drones_deployed, self.drones_returned = 0, 0
            self.target = None
            self.next_target()

    def return_state(self):
        if self.move(coastal_location, BOAT_RADIUS):
            self.set_hold_state()
        else:
            self.update_fuel_time()

    def __str__(self) -> str:
        return f"Boat: {self.name} \n {self.pos} with state {self.state}"


class BoatSprite(Sprite.Sprite):

    def __init__(self, boat: Boat):
        super(BoatSprite, self).__init__()
        # Add sprite
        self.sprites = [None] * len(VehicleStates.__members__)
        self.sprites[VehicleStates.HOLDSTATE.value] = pygame.image.load('./sprites/boat-white.png')
        self.sprites[VehicleStates.MOVESTATE.value] = pygame.image.load('./sprites/boat-red.png')
        self.sprites[VehicleStates.DETECTSTATE.value] = pygame.image.load('./sprites/boat-yellow.png')
        self.sprites[VehicleStates.RETURNSTATE.value] = pygame.image.load('./sprites/boat-red.png')
        self.image = self.sprites[VehicleStates.HOLDSTATE.value]
        self.rect = self.image.get_rect()
        self.boat = boat

    def getSprite(self):
        self.image = self.sprites[self.boat.state.value]
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
