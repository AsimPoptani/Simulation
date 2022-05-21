
from Vehicle import Vehicle, VehicleStates
from Windmill import Windmill
from config import DRONE_MAX_VELOCITY, DRONE_MAX_COMMUNICATION_RANGE, DRONE_MAX_BATTERY, DRONE_RADIUS, \
    ROTOR_RADIUS, BOAT_RADIUS, CIRCUMNAVIGATION_DISTANCE, TIME_SCALAR
from display import x_to_pixels, y_to_pixels
from averaging import Averaging
import Sprite
import pygame


class Submersive(Vehicle):

    # ID
    Submersive_num = 0

    def __init__(self, windfarm: list[Windmill], adv, name=None, start_pos=(0, 0, 0)):

        # initialise inherited values
        super(Submersive, self).__init__()

        # If no name is given, generate  one
        if name is None:
            self.name = "Submersive_" + str(Submersive.Submersive_num)
            Submersive.Submersive_num += 1
            print(f"No name given, generating {self.name}")
        else:
            self.name = name

        # max velocity
        self.abs_max_velocity = DRONE_MAX_VELOCITY * TIME_SCALAR
        # Communication range
        self.communication_range = DRONE_MAX_COMMUNICATION_RANGE
        # Current position X left Y up Z down
        self.pos = start_pos
        # Battery level
        self.fuel_level = DRONE_MAX_BATTERY
        # Time remaining to perform inspection
        self.detection_time = 0
        # averaging algorithm performed by drone
        self.averaging = Averaging(windfarm)
        # the host ADV
        self.adv = adv
        # whether this sprite is visible
        self.hide = True

    def detect(self):
        if self.detection_time > 0:
            self.detection_time -= 1
        else:
            self.target.faults = []

    def set_detect_state(self):
        for fault in self.target.faults:
            self.detection_time += fault["timeToDetect"]
        super().set_detect_state()

    def hold_state(self):
        if self in self.adv.drones:
            self.hide = True
            self.pos = self.adv.pos  # drone is onboard the ADV
            self.distance_travelled = 0  # reset distance
            if self.fuel_level < DRONE_MAX_BATTERY:
                self.fuel_level = min(self.fuel_level + self.abs_max_velocity, DRONE_MAX_BATTERY)
            else:
                self.distance_travelled = 0  # reset distance

    def move_state(self):
        if self.target is not None and self.fuel_level >= self.abs_max_velocity:
            collision, distance_travelled = self.move(self.target.pos[:2], DRONE_RADIUS + ROTOR_RADIUS)
            self.fuel_level = max(0, self.fuel_level - distance_travelled)
            self.distance_travelled += distance_travelled
            if collision:
                self.set_detect_state()

    def detect_state(self):
        # Give turbine faulty or not faulty based on fault detection
        self.target.fault_prob = self.averaging.check_faulty(self.target, 25)
        if self.target.has_fault():
            self.detect()
        else:
            self.target.inspected_turbine()
            self.target = None
            self.next_target()

    def return_state(self):
        if self.fuel_level >= self.abs_max_velocity:
            collision, distance_travelled = self.move(self.adv.pos[:2], DRONE_RADIUS + BOAT_RADIUS)
            self.fuel_level = max(0, self.fuel_level - distance_travelled)
            self.distance_travelled += distance_travelled
            if collision:
                self.adv.set_drone_returned(self)
                self.set_hold_state()

    def __str__(self) -> str:
        return f"Submersive: {self.name} \n {self.pos} with state {self.state}"


class SubmersiveSprite(Sprite.Sprite):

    def __init__(self, submersive: Submersive):
        super(SubmersiveSprite, self).__init__()
        # Add sprite
        self.sprites = [None] * len(VehicleStates.__members__)
        self.sprites[VehicleStates.HOLDSTATE.value] = pygame.image.load('./sprites/subwhite.png')
        self.sprites[VehicleStates.MOVESTATE.value] = pygame.image.load('./sprites/subred.png')
        self.sprites[VehicleStates.DETECTSTATE.value] = pygame.image.load('./sprites/subgreen.png')
        self.sprites[VehicleStates.RETURNSTATE.value] = pygame.image.load('./sprites/subred.png')
        self.image = self.sprites[VehicleStates.HOLDSTATE.value]
        self.rect = self.image.get_rect()
        self.submersive = submersive

    def getSprite(self):
        if self.submersive.hide:
            return None
        self.image = self.sprites[self.submersive.state.value]
        return self.image

    def getPower(self):
        percentage = (self.submersive.fuel_level / DRONE_MAX_BATTERY) * 100
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
        x = x_to_pixels(self.submersive.pos[0])
        y = y_to_pixels(self.submersive.pos[1])
        return x, y

    def getName(self):
        text = self.set_text(self.submersive.name, 0, 0, 10)[0]
        return text

    def debug(self):
        text = self.set_text(str(self.submersive), 0, 0, 10)[0]
        return text
