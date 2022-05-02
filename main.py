from math import inf, sqrt, pow

from config import WIDTH, HEIGHT , COASTAL_LOCATION
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
submersive=Submersive(start_pos=(*COASTAL_LOCATION,0))




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

    destination = submersive.pos[:2]
    smallest_distance = inf
    for windmill in windfarm:
        if windmill.collision(submersive.pos[0], submersive.pos[1]):
            if windmill.has_fault():
                windmill.fix_fault()
            else:
                print("cRaSh !!")
        if windmill.has_fault():
            x_diff = pow(submersive.pos[0] - windmill.pos[0], 2)
            y_diff = pow(submersive.pos[1] - windmill.pos[1], 2)
            diff = x_diff + y_diff
            distance = sqrt(diff)
            if distance < smallest_distance:
                smallest_distance = distance
                destination = windmill.pos
    submersive.set_move_state((*destination, 5000))
    submersive.step(windfarm)

    for windmill in windfarm:
        windmill.step()

    # Update the display
    pygame.display.flip()

    clock.tick(30)

    

# Done! Time to quit.
pygame.quit()