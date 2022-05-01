from config import WIDTH, HEIGHT
from locations import locations

from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame

# Faults
faults = [ {"name": "structural-damage", "probability": 0.0001, "timeToDetect": 100 } ]

# Create windmills according to the generated locations
windfarm=[]
for location in locations:
    x = location[0]
    y = location[1]
    windfarm.append(Windmill(faults, (x, y), str(len(windfarm)+1)))




# Create submersive
submersive=Submersive(start_pos=(0,0,0))




subSprite=SubmersiveSprite(submersive)

sprites=[]
sprites.append(subSprite)
for windmill in windfarm:
    sprites.append(WindmillSprite(windmill))


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
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
        #Update sprite for animation
        sprite.update()
        
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