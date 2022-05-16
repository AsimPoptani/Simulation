from Boat import Boat, BoatSprite
from ControlRoom import ControlRoom
from config import WIDTH, HEIGHT, COASTAL_LOCATION, BOAT_N_DRONES
from locations import locations
from faults import FAULTS
from colorsys import hsv_to_rgb

from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame

SIMULATION_TIME_FAULTS = 365

# Create windmills according to the generated locations
windfarms = []

# Drones
drones = []

for location in locations:
    x = location[0]
    y = location[1]
    windfarms.append(Windmill((x, y), str(len(windfarms) + 1)))

sprites = []

# Create boat
boat = Boat(windfarms, start_pos=(*COASTAL_LOCATION, 0))
boat_sprite = BoatSprite(boat)
sprites.append(boat_sprite)
drones = []
for i in range(BOAT_N_DRONES):
    drone = Submersive(windfarms, boat)
    drones.append(drone)
    drone_sprite = SubmersiveSprite(drone)
    sprites.append(drone_sprite)
boat.set_drones(drones)

control = ControlRoom(boat, windfarms)
destination = control.adv_positions(2)
boat.set_targets(destination)

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
        toBlit = sprite.getSprite()
        if toBlit == None:
            continue
        position = sprite.getPosition()
        name = sprite.getName()
        # to show probabilities of faulty after using averaging
        prob = None
        if type(sprite) is SubmersiveSprite:
            prob = sprite.getProb()
        battery = sprite.getPower()
        # Update sprite for animation
        sprite.update()

        name_pos = position[0] - name.get_width(), position[1] - 10
        screen.blit(name, name_pos)

        if prob is not None:
            prob_pos = position[0] - name.get_width() + 5, position[1] + 15
            screen.blit(prob, prob_pos)

        screen.blit(toBlit, position)
        battery_pos = position[0] - battery.get_width(), position[1]
        screen.blit(battery, battery_pos)

    boat.step()
    for drone in drones:
        drone.step()

    for windmill in windfarms:
        windmill.step()

    # Create legend
    box_size = (int(WIDTH / 5), int(HEIGHT / 3))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((WIDTH - box_size[0], HEIGHT - box_size[1]), box_size), width=2)
    dot_pos = 0
    for fault in FAULTS:
        hue_diff = 0.9 / len(FAULTS)
        hue = fault["id"] * hue_diff
        colour = hsv_to_rgb(hue, 1, 1)
        colour = tuple(map(lambda x: round(x * 255), colour))
        pygame.draw.circle(screen, colour, (WIDTH - box_size[0] + 10, HEIGHT - box_size[1] + 10 + dot_pos), 5)
        font = pygame.font.Font('freesansbold.ttf', 10)
        text = font.render(fault["name"], 1, (0, 0, 0))
        screen.blit(text, (WIDTH - box_size[0] + 18, HEIGHT - box_size[1] + 5 + dot_pos))
        dot_pos += int((box_size[1] - 5) / len(FAULTS))

    # Update the display
    pygame.display.flip()

    clock.tick(30)

# Done! Time to quit.
pygame.quit()
