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

from ControlRoom import distance, n_nearest_targets
from Vehicle import VehicleStates, Vehicle
from config import COASTAL_LOCATION, DRONE_MAX_COMMUNICATION_RANGE, BOAT_MAX_VELOCITY, BOAT_MAX_FUEL, BOAT_RADIUS, \
    ROTOR_RADIUS, MAX_SCAN_DISTANCE, TIME_SCALAR, BOAT_N_DRONES, DRONE_MAX_TARGETS, DRONE_MAX_VELOCITY, INSPECTION_TIME
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
        self.abs_max_velocity = BOAT_MAX_VELOCITY * TIME_SCALAR
        # Communication range
        self.communication_range = DRONE_MAX_COMMUNICATION_RANGE
        # Current position X left Y up Z down
        self.pos = start_pos
        # Fuel level
        self.fuel_level = BOAT_MAX_FUEL
        # drones
        self.drones = []
        self.auvs = []  # copy
        # number of drones deployed
        self.drones_deployed = 0
        # Copy of entire Windfarm
        self.windfarm = windfarm.copy()
        # for restoring working copy
        self.windfarm_cache = windfarm.copy()
        # work list
        self.windmills = []
        # stats
        self.total_distance_travelled = 0
        self.total_hours_at_sea = 0
        self.total_turbines_checked = 0

    def set_drones(self, drones):
        self.drones = drones.copy()
        self.auvs = drones.copy()

    def set_drone_returned(self, drone):
        self.drones.append(drone)

    def hold_state(self):
        if self.distance_travelled != 0:
            print(self.distance_travelled / 1000, "kilometers")
            self.total_distance_travelled += self.distance_travelled
            self.distance_travelled = 0
            print(self.hours_at_sea, "hours")
            self.total_hours_at_sea += self.hours_at_sea
            self.hours_at_sea = 0

            turbines_checked = 175 - len(self.windfarm)
            self.total_turbines_checked += turbines_checked
            print(turbines_checked, 'turbines checked.')
            print(len(self.windfarm), 'turbines remain unchecked.')

            # refresh copy of windfarm
            self.windfarm = self.windfarm_cache.copy()

        if self.fuel_level < BOAT_MAX_FUEL and distance(*self.pos[:2], *coastal_location) < 1000:
            # estimate a rate of 3500 gallons per hour, takes ~90 hours
            self.fuel_level = min(self.fuel_level + (BOAT_MAX_FUEL / 90) * TIME_SCALAR, BOAT_MAX_FUEL)
        elif self.fuel_level < TIME_SCALAR and distance(*self.pos[:2], *coastal_location) > 1000:
            print("Lost at sea")
            print("last known position ", self.pos[:2])
            print(self.total_distance_travelled / 1000, "kilometers", "total distance")
            print(self.total_hours_at_sea, "hours", "total hours at sea")
            print(self.total_turbines_checked, 'total turbines checked.')
            exit(-1)

    def update_fuel_time(self):
        self.hours_at_sea += TIME_SCALAR
        self.fuel_level = max(0, self.fuel_level - TIME_SCALAR)

    def move_state(self):
        if self.target is not None and self.fuel_level > TIME_SCALAR:
            if type(self.target) is Windmill:
                collision, _ = self.move(self.target.pos[:2], BOAT_RADIUS + ROTOR_RADIUS)
                if collision:
                    self.set_detect_state()
                else:
                    self.update_fuel_time()
            else:
                collision, _ = self.move(self.target, BOAT_RADIUS)
                if collision:
                    self.set_detect_state()
                else:
                    self.update_fuel_time()
        else:
            self.set_hold_state()

    def detect_state(self):
        max_distance = MAX_SCAN_DISTANCE

        # if there isn't a work list, and no drones have been deployed, make a work list
        if self.drones_deployed == 0 and len(self.windmills) == 0:
            self.windmills = list(filter(lambda i: distance(*self.pos[:2], *i.pos[:2]) < max_distance, self.windfarm))
            self.windmills.sort(key=lambda i: distance(*self.pos[:2], *i.pos[:2]), reverse=False)

        # if there are turbines still on the work list
        if len(self.windmills) > 0:
            drones_to_remove = []

            for drone in self.drones:
                # targets for this drone
                targets = []
                # running tally of distance this drone will travel
                reach = drone.fuel_level / 2
                # initial target is the ADV for sorting purposes
                target = self
                # limit the number of targets each drone can have
                count = 0
                # while there are turbines still on the work list, and the reach is still greater than the smallest step
                while reach > drone.abs_max_velocity and len(self.windmills) > 0:
                    # sort available targets by distance from the current one
                    self.windmills.sort(key=lambda i: distance(*target.pos[:2], *i.pos[:2]), reverse=False)
                    # select the closest target to the current one
                    next_target = self.windmills[0]
                    # the interval is the distance to that target from this one
                    interval = distance(*target.pos[:2], *next_target.pos[:2])
                    # the stretch is that distance plus the amount the battery will be depleted by inspecting the target
                    stretch = interval + (INSPECTION_TIME * DRONE_MAX_VELOCITY)
                    # if the difference between the reach and the stretch is greater than the smallest step
                    if reach - stretch > drone.abs_max_velocity:
                        # subtract the stretch from the reach
                        reach -= stretch
                        # remove the next target from the work list
                        self.windmills.remove(next_target)
                        self.windfarm.remove(next_target)
                        # append it to this drones targets
                        targets.append(next_target)
                        # and make the next target the current one for the next iteration
                        target = next_target
                        # check that the number of targets assigned to this drone is below the allowed threshold
                        if count < DRONE_MAX_TARGETS:
                            count += 1
                        else:
                            # if the threshold has been reached, break out of the while loop for this drone
                            break
                    else:
                        # if the stretch exceeds the reach, break out of the while loop for this drone
                        break

                # allocate the targets to the drone and deploy
                if len(targets) > 0:
                    drone.set_targets(targets)
                    self.drones_deployed += 1
                    drones_to_remove.append(drone)

            # remove the deployed drones from the queue
            for drone in drones_to_remove:
                self.drones.remove(drone)
            # update fuel consumed and time at sea
            self.update_fuel_time()
            # check all drones are within communications range
            if not self.drones_in_communications_range():
                print('Drones out of communications range !')
        # else if no drones have been deployed
        elif len(self.drones) == BOAT_N_DRONES:
            self.drones_deployed = 0
            self.target = None
            self.next_target()
        # else drones have been deployed, hold position
        else:
            # update fuel consumed and time at sea
            self.update_fuel_time()
            # check all drones are within communications range
            if not self.drones_in_communications_range():
                print('Drones out of communications range !')

    def return_state(self):
        if self.fuel_level > TIME_SCALAR:
            collision, _ = self.move(coastal_location, BOAT_RADIUS)
            if collision:
                self.set_hold_state()
            else:
                self.update_fuel_time()
        else:
            self.set_hold_state()

    def drones_in_communications_range(self) -> bool:
        all_in_range = True
        not_holding = list(filter(lambda i: i.state != VehicleStates.HOLDSTATE, self.auvs))
        for drone in not_holding:
            in_range_of_boat = distance(*drone.pos[:2], *self.pos[:2]) < DRONE_MAX_COMMUNICATION_RANGE
            if not in_range_of_boat:
                in_range = list(filter(lambda other: distance(*drone.pos[:2], *other.pos[:2]) < DRONE_MAX_COMMUNICATION_RANGE, not_holding))
                in_range.remove(drone)
                if len(in_range) == 0:
                    all_in_range = False
                    break
        return all_in_range

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
