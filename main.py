from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite, SubmersiveStates
import random
import pygame
HEIGHT,WIDTH=500,500

# Faults
faults = [ {"name": "structural-damage", "probability": 0.01, "timeToDetect": 100 } ]


# Create windmills randomly
windfarm=[]
for i in range(0,40):
    windfarm.append(Windmill(faults,(random.randint(0,HEIGHT),random.randint(0,WIDTH),i)))




# Create submersive
submersive=Submersive(start_pos=(0,0,0))




subSprite=SubmersiveSprite(submersive)

sprites=[]
sprites.append(subSprite)
for windmill in windfarm:
    sprites.append(WindmillSprite(windmill))


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
clock = pygame.time.Clock()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    for sprite in sprites:
        toBlit=sprite.getSprite()
        position=sprite.getPosition()
        name=sprite.getName()
        
        name_pos=position[0]-name.get_width(),position[1]-10
        screen.blit(name,name_pos)
        screen.blit(toBlit,position)

    submersive.set_move_state((200,50,5))
    submersive.step(windfarm)

    for windmill in windfarm:
        windmill.step()

    # Update the display
    pygame.display.flip()

    clock.tick(30)

    

# Done! Time to quit.
pygame.quit()