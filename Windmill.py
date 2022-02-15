import random, pygame
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
        # Define a small rect as the sprite
        self.image = pygame.Surface([10,10], pygame.SRCALPHA)
        pygame.draw.circle(self.image,(0,0,0),(5,5),5)
        # self.rect = self.image.get_rect()
        self.windmill=windmill
    
    def getSprite(self):
        if len(self.windmill.faults)>0:
            pygame.draw.circle(self.image,(255,0,0),(5,5),5)
        else:
            pygame.draw.circle(self.image,(0,0,0),(5,5),5)
        return self.image
    
    def getPosition(self):
        
        return self.windmill.pos[0],self.windmill.pos[1]
    
    def getName(self):
        text=set_text(self.windmill.name,0,0,10)[0]
        return text

    def debug(self):
        text=set_text(str(self.windmill),0,0,10)[0]
        return text