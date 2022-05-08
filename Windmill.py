import random, pygame
from display import x_to_pixels, y_to_pixels
from config import ROTOR_RADIUS, FAULT_RATE_DIVISOR, DATA_UPDATE_INTERVAL
from Weather import Datagen
from faults import FAULTS
from colorsys import hsv_to_rgb

class Windmill():
    # A windmill has several states
    # Working Normally
    # Broken


    # Pass in faults with probability
    # TODO add time to detect with Gaussian noise

    # Faults = {"structural-damage":{"probability":0.1,"timeToDetect":100}}
    # TODO needs guesstimate of time to detect and probability of happening
    COUNTER=0
    def __init__(self,position,name=None) -> None:
        self.potential_faults = FAULTS
        self.pos = position
        self.faults=[]
        self.timer_counter = 0
        self.data = {}
        self.datagen = Datagen()
        self.wind_s_d = self.datagen.get_speed(12,31,23)
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
        # Only one fault can happen per step
        for fault in self.potential_faults:
            # print(self.potential_faults)
            if random.random() < fault["probability"] / FAULT_RATE_DIVISOR:
                # Check if fault is already present
                if fault not in self.faults:
                    self.faults.append(fault)
                    print('Windmill',self.name, 'developed fault', fault["name"])
                    return

    # Update data like windspeed only every x seconds (needs calculation)
    def update_data(self):
        if int(self.timer_counter) % DATA_UPDATE_INTERVAL == 0:
            wind_s_d_update = self.datagen.update()
            self.data.update({"Wind Speed": wind_s_d_update[0]})
            self.data.update({"Wind Direction": wind_s_d_update[1]})
            self.data.update({"Power": self.datagen.get_power(self.data["Wind Speed"])})
            self.data.update({"Vibration": self.datagen.get_vibrations(self.data["Wind Speed"])})
        self.timer_counter += 1

    def has_fault(self):
        return len(self.faults) > 0

    def fix_fault(self):
        self.faults.pop(0)

    def collision(self, x, y) -> bool:
        """is the given x and y position within this windmill's position ± rotor radius ?"""
        left = x < self.pos[0] + ROTOR_RADIUS
        rite = self.pos[0] - ROTOR_RADIUS < x
        uppp = self.pos[1] - ROTOR_RADIUS < y
        down = y < self.pos[1] + ROTOR_RADIUS
        return left and rite and uppp and down
    
    def __str__(self) -> str:
        return f"Windmill at {self.pos} \n with faults: {self.faults}"
    
    def __repr__(self) -> str:
        return str(self)

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
        self.sprites = []
        self.sprites.append(pygame.image.load('./sprites/wind-turbine1.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine2.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine3.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine4.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine5.png'))
        self.sprites.append(pygame.image.load('./sprites/wind-turbine6.png'))
        self.vis_sprite = 0
        self.image = self.sprites[self.vis_sprite]
        self.rect = self.image.get_rect()
        self.windmill=windmill
    
    def getSprite(self):
        if len(self.windmill.faults)>0:
            # Apply color circles to see the faults move each circle by 5 if there is a circle there
            x = 2
            for fault in self.windmill.faults:
                hue_diff = 359 / len(FAULTS)
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