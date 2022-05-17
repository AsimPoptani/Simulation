from Boat import Boat, BoatSprite
from ControlRoom import ControlRoom
from Vehicle import VehicleStates
from config import WIDTH, HEIGHT, COASTAL_LOCATION, BOAT_N_DRONES, BOAT_MAX_FUEL, SIMULATION_TIME_FAULTS
from locations import locations
from faults import FAULTS
from colorsys import hsv_to_rgb

from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame


def initialise_windfarm(sim_sprites) -> list [Windmill]:
    windfarm = []
    for location in locations:
        turbine = Windmill(location, str(len(windfarm) + 1))
        windfarm.append(turbine)
        sim_sprites.append(WindmillSprite(turbine))

    # Run a simulation of 1 year to generate faults in Windmills
    for i in range(SIMULATION_TIME_FAULTS):
        for turbine in windfarm:
            # TODO inside step add faults for each day etc
            turbine.step()

    return windfarm


def initialise_aquatic_crafts(sim_sprites) -> (Boat, [Submersive]):
    adv = Boat(windfarms, start_pos=(*COASTAL_LOCATION, 0))
    boat_sprite = BoatSprite(adv)
    sim_sprites.append(boat_sprite)
    auvs = []
    for i in range(BOAT_N_DRONES):
        auv = Submersive(windfarms, adv)
        auvs.append(auv)
        drone_sprite = SubmersiveSprite(auv)
        sim_sprites.append(drone_sprite)
    adv.set_drones(auvs)

    return adv, auvs


def create_path(control_room, adv):
    destination = [] ##control_room.get_boat_positions()
    if len(destination) == 0:
        print('Schedular returned no positions.', 'Reverting to hand-rolled scheduling.')
        destination = control_room.adv_positions(3)
    adv.set_targets(destination)


sprites = []
windfarms = initialise_windfarm(sprites)
boat, drones = initialise_aquatic_crafts(sprites)
control = ControlRoom(boat, windfarms)
create_path(control, boat)


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
        toBlit = sprite.getSprite()
        if toBlit == None:
            continue
        position = sprite.getPosition()
        name = sprite.getName()
        # to show probabilities of faulty after using averaging
        prob = None
        battery = None
        power = None
        if type(sprite) is SubmersiveSprite:
            battery = sprite.getBattery()
        if type(sprite) is BoatSprite:
            battery = sprite.getBattery()
        if type(sprite) is WindmillSprite:
            prob = sprite.getProb()
            power = sprite.getPower()
        
        # Update sprite for animation
        sprite.update()

        name_pos = position[0] - name.get_width()+25, position[1] - 10
        screen.blit(name, name_pos)
        screen.blit(toBlit, position)

        if prob is not None:
            prob_pos = position[0] - name.get_width() + 5, position[1] + 15
            screen.blit(prob, prob_pos)
        if battery is not None:
            battery_pos = position[0] - battery.get_width(), position[1]
            screen.blit(battery, battery_pos)
        if power is not None:
            power_pos = position[0] - power.get_width()+25, position[1] 
            screen.blit(power, power_pos)

    boat.step()
    for drone in drones:
        drone.step()

    if boat.state == VehicleStates.HOLDSTATE and boat.fuel_level == BOAT_MAX_FUEL:
        create_path(control, boat)

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

    clock.tick(10)

# Done! Time to quit.
pygame.quit()
