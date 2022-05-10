import random, pygame
from math import sqrt

from display import x_to_pixels, y_to_pixels
from config import ROTOR_RADIUS, FAULT_RATE_DIVISOR, DATA_UPDATE_INTERVAL, DRONE_MAX_VELOCITY, DRONE_SAFE_ZONE
from Weather import Datagen
from faults import FAULTS
from colorsys import hsv_to_rgb

class Windmill():
    # A windmill has several states
    # Working Normally
    # Broken

    AMOUNT_OF_STEPS_TO_DAY=24


    # Pass in faults with probability
    # TODO add time to detect with Gaussian noise

    # Faults = {"structural-damage":{"probability":0.1,"timeToDetect":100}}
    # TODO needs guesstimate of time to detect and probability of happening
    COUNTER=0
    def __init__(self,position,name=None) -> None:
        self.potential_faults = FAULTS
        self.pos = position
        self.faults=[]
        # Data timer
        self.timer_counter = 0
        # Data generated from turbines WindSpeed in m/s, Wind direction in degrees, power in Watts, Vibration in m/s^2 (accerleration)
        self.data = {}
        # Data generator
        self.datagen = Datagen()
        self.wind_s_d = self.datagen.get_speed(1,1,0)
        self.data["Wind Speed"] = self.wind_s_d[0]
        self.data["Wind Direction"] = self.wind_s_d[1]
        self.data["Power"] = 0
        self.data["Vibration"] = 0
        if name is None:
            self.name = "Windmill_" + str(Windmill.COUNTER)
            Windmill.COUNTER += 1
        else:
            self.name = name
    
    def step(self):
        # TODO add update data here
        # 
        # Only one fault can happen per step
        for fault in self.potential_faults:
            # Looping daily rate
            if random.random() < fault["probability"] / FAULT_RATE_DIVISOR:
                # Check if fault is already present
                if fault not in self.faults:
                    self.faults.append(fault)
                    print('Windmill',self.name, 'developed fault', fault["name"], 'priority', fault["priority"])
                    return

    # Update data like windspeed only every x seconds (needs calculation)
    def update_data(self):
        if int(self.timer_counter) % DATA_UPDATE_INTERVAL == 0:
            wind_s_d_update = self.datagen.update()
            self.data.update({"Wind Speed": wind_s_d_update[0]})
            self.data.update({"Wind Direction": wind_s_d_update[1]})
            self.data.update({"Power": self.datagen.get_power(self.data["Wind Speed"])})
            # add vibrational extras check each fault in the faults and then apply a multiplier or noise based on data before updating data
            # Only the larger vibrational data fault takes effect.
            self.data.update({"Vibration": self.datagen.get_vibrations(self.data["Wind Speed"])})
        self.timer_counter += 1

    def has_fault(self):
        return len(self.faults) > 0

    # TODO change to inspect_fault pops all and sets status to inspected
    def fix_fault(self):
        self.faults.pop(0)


    def collision(self, x, y, radius) -> bool:
        """is the given x and y position and radius within this windmill's position ± rotor radius ?"""
        distance = sqrt(pow(x - self.pos[0], 2) + pow(y - self.pos[1], 2))
        radii = radius + ROTOR_RADIUS
        return distance < radii

    # TODO may not need
    def safezone(self, x, y, radius) -> bool:
        """is the given x and y position and radius within this windmill's safe zone ?"""
        distance = sqrt(pow(x - self.pos[0], 2) + pow(y - self.pos[1], 2))
        radii = radius + ROTOR_RADIUS + DRONE_MAX_VELOCITY
        safe_zone = distance < radii
        return safe_zone and not self.collision(x, y, radius * DRONE_SAFE_ZONE)

    def __str__(self) -> str:
        return f"Windmill at {self.pos} \n with faults: {self.faults}"
    
    def __repr__(self) -> str:
        return str(self)



# TODO Helper function put into another file
def set_text(string, coordx, coordy, fontSize): #Function to set text
    font = pygame.font.Font('freesansbold.ttf', fontSize) 
    #(0, 0, 0) is black, to make black text
    text = font.render(string, True, (0, 0, 0)) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)                  


class WindmillSprite(pygame.sprite.Sprite):
    def __init__(self,windmill:Windmill):
        super(WindmillSprite,self).__init__()
        #List of images for animation
        self.play = True
        # Images for animation
        self.sprites = []
        self.sprites.append(pygame.image.load('./sprites/wind-turbine1.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine2.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine3.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine4.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine5.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine6.png'))
        # Current image index
        self.vis_sprite = 0
        # Current image
        self.image = self.sprites[self.vis_sprite]
        self.rect = self.image.get_rect()
        self.windmill=windmill
    
    def getSprite(self):
        if len(self.windmill.faults)>0:
            self.image = pygame.image.load('./sprites/wind-turbine-fault.png')
            # Apply color circles to see the faults move each circle by 5 if there is a circle there
            # TODO change to use the fault color - redone
            # Also add key legend to show which color is which
            x = 2
            for fault in self.windmill.faults:
                # Get colour from fault table
                hue_diff = 1.0 / len(FAULTS)
                hue = fault["id"] * hue_diff
                colour = hsv_to_rgb(hue, 1, 1)
                colour = tuple(map(lambda x: round(x * 255), colour))
                pygame.draw.circle(self.image, colour, (x,2), 2)
                x += 5
            self.play = False
        else:
            self.image = self.sprites[int(self.vis_sprite)]
            # clear all color circles if no faults
            for x in range(2,len(self.windmill.potential_faults) * 5, 5):
                pygame.draw.circle(self.image,(0,0,0,0),(x,2),2)
            self.play = True
        return self.image
    
    #Update to change sprite for animation
    def update(self):
        if (self.play):
            self.vis_sprite += 0.5
            if (self.vis_sprite >= len(self.sprites)):
                self.vis_sprite = 0
            self.image = self.sprites[int(self.vis_sprite)]
    
    def getBattery(self):
        if self.windmill.data["Power"] > 5600000:
            return pygame.image.load('./sprites/arrow-4.png')
        elif self.windmill.data["Power"] > 4200000:
            return pygame.image.load('./sprites/arrow-3.png')
        elif self.windmill.data["Power"] > 2800000:
            return pygame.image.load('./sprites/arrow-2.png')
        elif self.windmill.data["Power"] > 1400000:
            return pygame.image.load('./sprites/arrow-1.png')
        else:
            return pygame.image.load('./sprites/arrow-empty.png')

    def getPosition(self):
        x = x_to_pixels(self.windmill.pos[0])
        y = y_to_pixels(self.windmill.pos[1])
        return x, y
    
    def getName(self):
        text=set_text(self.windmill.name,0,0,10)[0]
        return text

    def debug(self):
        text=set_text(str(self.windmill),0,0,10)[0]
        return text