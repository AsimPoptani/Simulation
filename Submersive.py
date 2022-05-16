
from Vehicle import Vehicle, VehicleStates
from Windmill import Windmill
from config import DRONE_MAX_VELOCITY, DRONE_MAX_COMMUNICATION_RANGE, DRONE_MAX_BATTERY, DRONE_RADIUS, \
    ROTOR_RADIUS, BOAT_RADIUS
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
        self.abs_max_velocity = DRONE_MAX_VELOCITY
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
            # Once inspected give prob of faulty
            self.target.fault_prob = self.averaging.check_faulty(self.target,5)
            self.target.faults = []

    def step(self):
        super().step()

        if self.state == VehicleStates.HOLDSTATE:
            if self in self.adv.drones:
                self.pos = self.adv.pos
                if self.fuel_level < DRONE_MAX_BATTERY:
                    self.fuel_level += 1
        elif self.state == VehicleStates.MOVESTATE:
            if self.target is not None and self.fuel_level > 0:
                if self.move(self.target.pos[:2], DRONE_RADIUS + ROTOR_RADIUS):
                    self.set_detect_state()
                self.fuel_level -= 1
        elif self.state == VehicleStates.DETECTSTATE:
            if self.target.has_fault():
                self.detect()
            else:
                self.target = None
                self.next_target()
        elif self.state == VehicleStates.RETURNSTATE:
            if self.fuel_level > 0:
                if self.move(self.adv.pos[:2], DRONE_RADIUS + BOAT_RADIUS):
                    self.adv.set_drone_returned(self)
                    self.set_hold_state()
                    self.fuel_level -= 1

    def set_detect_state(self):
        for fault in self.target.faults:
            self.detection_time += fault["timeToDetect"]
        super().set_detect_state()

    def __str__(self) -> str:
        return f"Submersive: {self.name} \n {self.pos} with state {self.state}"


class SubmersiveSprite(Sprite.Sprite):

    def __init__(self, submersive: Submersive):
        super(SubmersiveSprite, self).__init__()
        # Add sprite
        # TODO update image to a new image
        self.image = pygame.image.load('./sprites/subblack.png')
        self.rect = self.image.get_rect()
        self.submersive = submersive

    def getSprite(self):
        if self.submersive.hide:
            return None
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
    
    def getProb(self):
        text = None
        return text

    def debug(self):
        text = self.set_text(str(self.submersive), 0, 0, 10)[0]
        return text
