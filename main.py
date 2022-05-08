from ast import Sub
from math import inf, sqrt, pow

from config import WIDTH, HEIGHT , COASTAL_LOCATION
from locations import locations

from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame

SIMULATION_TIME_FAULTS=365
N_DRONES=50




# Create windmills according to the generated locations
windfarms=[]

# Drones
drones=[]



for location in locations:
    x = location[0]
    y = location[1]
    windfarms.append(Windmill((x, y), str(len(windfarms)+1)))




# Create submersive
submersive=Submersive(start_pos=(*COASTAL_LOCATION,0))




subSprite=SubmersiveSprite(submersive)

sprites=[]
sprites.append(subSprite)
for windmill in windfarms:
    sprites.append(WindmillSprite(windmill))


pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()


# Run a simulation of 1 year to generate faults in Windmills
for i in range(SIMULATION_TIME_FAULTS):
    for windmill in windfarms:
        # TODO inside step add faults for each day etc
        windmill.step()
# Generate n_drones
for _ in range(N_DRONES):
    # Set starting position
    sub=Submersive(start_pos=(*COASTAL_LOCATION,0))
    drones.append(sub)
    # Add to sprites
    sprites.append(SubmersiveSprite(sub))

# TODO Generate a plan for a set of drones to follow
for _ in range(N_DRONES):
    pass

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

    submersive.step(windfarms)

    for windmill in windfarms:
        windmill.step()
        windmill.update_data()

    # Update the display
    pygame.display.flip()

    clock.tick(30)

    

# Done! Time to quit.
pygame.quit()