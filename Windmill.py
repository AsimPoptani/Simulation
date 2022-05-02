import random, pygame
from display import x_to_pixels, y_to_pixels
from config import ROTOR_RADIUS
from Weather import Windspeed

class Windmill():
    # A windmill has several states
    # Working Normally
    # Broken


    # Pass in faults with probability
    # TODO add time to detect with Gaussian noise

    # Faults = {"structural-damage":{"probability":0.1,"timeToDetect":100}}
    # TODO needs guesstimate of time to detect and probability of happening
    COUNTER=0
    def __init__(self,FAULTS,position,name=None) -> None:
        self.potential_faults = FAULTS
        self.pos = position
        self.faults=[]
        self.wind = Windspeed()
        self.wswd = self.wind.get_speed(12,31,23)
        if name is None:
            self.name = "Windmill_" + str(Windmill.COUNTER)
            Windmill.COUNTER += 1
        else:
            self.name = name
    
    def step(self):
        # Only one fault can happen per step
        for fault in self.potential_faults:
            # print(self.potential_faults)
            if random.random() < fault["probability"]:
                # Check if fault is already present
                if fault not in self.faults:
                    self.faults.append(fault)
                    return
        self.wswd = self.wind.update()

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
            self.image = pygame.image.load('./sprites/wind-turbine-fault.png')
            #pygame.draw.circle(self.image,(255,0,0),(1,1),5)
            self.play = False
        else:
            self.image = self.sprites[int(self.vis_sprite)]
            self.play = True
        return self.image
    
    #Update to change sprite for animation
    def update(self):
        if (self.play):
            self.vis_sprite += 0.2
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