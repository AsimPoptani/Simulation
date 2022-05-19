from Boat import Boat, BoatSprite
from ControlRoom import ControlRoom
from Vehicle import VehicleStates
from config import WIDTH, HEIGHT, COASTAL_LOCATION, BOAT_N_DRONES, BOAT_MAX_FUEL, SIMULATION_TIME_FAULTS
from locations import locations
from faults import FAULTS
from colorsys import hsv_to_rgb
from Submersive import SubmersiveSprite
from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame, datetime,os
# Get pwd
pwd = os.getcwd()
# Os join Opens a file and returns a file object.
url=os.path.join(pwd,"./OpenSans-Regular.ttf")

# Current time
current_time = datetime.datetime.now()

# Remove hours, mins, seconds to 9:00
current_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)

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
        destination = control_room.find_path()
    adv.set_targets(destination)


sprites = []
windfarms = initialise_windfarm(sprites)
boat, drones = initialise_aquatic_crafts(sprites)
control = ControlRoom(boat, windfarms)
create_path(control, boat)


pygame.init()
font=pygame.font.Font(url, 15)

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
            prob_pos = position[0] - name.get_width() + 20, position[1] + 15
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

    total_power = 0
    for windmill in windfarms:
        windmill.step()
        total_power += windmill.data["Power"]

    # Create legend
    box_size = (int(WIDTH / 3), int(HEIGHT / 2.2))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((WIDTH - box_size[0], HEIGHT - box_size[1]), box_size), width=2)
    dot_pos = 0
    # font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render("Faults", 1, (0, 0, 0))
    screen.blit(text, (WIDTH - box_size[0]/2 - text.get_width(), HEIGHT - box_size[1] + 5))
    for fault in FAULTS:
        hue_diff = 0.9 / len(FAULTS)
        hue = fault["id"] * hue_diff
        colour = hsv_to_rgb(hue, 1, 1)
        colour = tuple(map(lambda x: round(x * 255), colour))
        pygame.draw.circle(screen, colour, (WIDTH - box_size[0] + 10, HEIGHT - box_size[1] + 37 + dot_pos), 8)
        # font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(fault["name"], 1, (0, 0, 0))
        screen.blit(text, (WIDTH - box_size[0] + 25, HEIGHT - box_size[1] + 29 + dot_pos))
        dot_pos += int((box_size[1] - 30) / len(FAULTS))

    
    # Create summary box surface
    summary_box = (300,100)
    summary_box_surface = pygame.Surface(summary_box)
    # White background
    summary_box_surface.fill((255, 255, 255))
    # Add text "Ship summary"
    # font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render("Ship summary", 1, (0, 0, 0))
    summary_box_surface.blit(text,(0,0),text.get_rect())

    # Get ship battery level
    battery_level = boat.fuel_level

    # Get boat sprite
    boat_sprite = BoatSprite(boat)
    battery_icon = boat_sprite.getBattery()

    # Add text "Total power"
    # font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render(f"Total power:{((battery_level/BOAT_MAX_FUEL)*100):.2f}%", 1, (0, 0, 0))
    summary_box_surface.blit(text,(20,20),text.get_rect())

    # Add Icon next to Total power
    summary_box_surface.blit(battery_icon,(0,15))


    
    # Number of drones out
    # Count number of drones out
    num_out = 0
    for drone in drones:
        if drone.state == VehicleStates.MOVESTATE or drone.state == VehicleStates.HOLDSTATE:
            num_out += 1

    text=font.render(f"Drones out:{len(drones)-num_out} | Drones in: {num_out}", 1, (0, 0, 0))
    summary_box_surface.blit(text,(20,40),text.get_rect())

    # Get image of drone
    drone_sprite=SubmersiveSprite(drones[0])
    # Add Icon next to drones out
    summary_box_surface.blit(drone_sprite.image,(0,35))

    # Blit summary box to screen
    screen.blit(summary_box_surface, (0, HEIGHT - summary_box[1]))


    # Create data graphic legend thing
    data_graphic_box = (175, 175)
    # Draw Box
    # pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((0, 0), data_graphic_box), width=2)
    # Write Title
    # text = pygame.font.Font('freesansbold.ttf', 25).render("Data", 1, (0, 0, 0))
    # screen.blit(text, (int(data_graphic_box[0]/2 - text.get_width() + 20) , 5))
    # Show Wind Speed
    wind_speed = windfarms[0].data["Wind Speed"]
    # Opensans font

    # font = pygame.font.Font('freesansbold.ttf', 15)
    text = font.render("Wind Speed: "+str(wind_speed) + " m/s", 1, (0, 0, 0))
    screen.blit(text, (5, 30))
    # Show Total Power
    text = font.render("Total Power: "+str(int(total_power/ 1000000)) + " MW", 1, (0, 0, 0))
    screen.blit(text, (5, 45))
    # Wind Direction
    wind_direction = windfarms[0].data["Wind Direction"]
    arrow = pygame.image.load('./sprites/up-arrow.png')
    arrow = pygame.transform.rotate(arrow, 360 - int(wind_direction))
    screen.blit(arrow, (84 - int(arrow.get_width()/2), 120 - int(arrow.get_height()/2)))
    text = font.render("Direction:" + str(wind_direction), 1, (0, 0, 0))
    screen.blit(text, (5, 60))


    # If current time is 1800 skip to next day to 9 am 
    if current_time.hour == 18 and current_time.minute == 0:
        current_time = current_time + datetime.timedelta(days=1)
        current_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0)
    # Draw date and time
    text=font.render(current_time.strftime("%d/%m/%Y %H:%M:%S"), 1, (0, 0, 0))
    # Step time
    current_time += datetime.timedelta(hours=1)
    # Center text
    screen.blit(text,(WIDTH - text.get_width() - 5,5))

    # Update the display
    pygame.display.flip()

    clock.tick(10)

# Done! Time to quit.
pygame.quit()
