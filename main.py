
from Boat import Boat, BoatSprite
from ControlRoom import ControlRoom
from Vehicle import VehicleStates
from config import WIDTH, HEIGHT, BOAT_N_DRONES, BOAT_MAX_FUEL, SIMULATION_TIME_FAULTS
from config import TIME_SCALAR, BG_COLOUR, FG_COLOUR, SAVE_IMAGES, HIDEF, QUICK_VIEW, IMAGE_DIR
from locations import locations, coastal_location
from faults import FAULTS
from colorsys import hsv_to_rgb
from Windmill import Windmill, WindmillSprite
from Submersive import Submersive, SubmersiveSprite
import pygame, os
# Current time
from time_utilities import nanosecond_string, NANOSECONDS_IN_HOUR, NANOSECONDS_IN_DAY

# Get pwd
pwd = os.getcwd()
# Os join Opens a file and returns a file object.
url = os.path.join(pwd, "./OpenSans-Regular.ttf")

# make directory for saving images
if SAVE_IMAGES:
    try:
        os.mkdir(IMAGE_DIR)
    except FileExistsError:
        pass

current_time = 0
text_width = 0

def initialise_windfarm(sim_sprites) -> list [Windmill]:
    windfarm = []
    for location in locations:
        turbine = Windmill(location, str(len(windfarm) + 1))
        windfarm.append(turbine)
        sim_sprites.append(WindmillSprite(turbine))

    # Run for SIMULATION_TIME_FAULTS number of ticks to generate faults in Windmills
    for i in range(SIMULATION_TIME_FAULTS):
        for turbine in windfarm:
            # TODO inside step add faults for each day etc
            turbine.step()

    return windfarm


def initialise_aquatic_crafts(sim_sprites) -> (Boat, [Submersive]):
    adv = Boat(windfarms, name="ADV", start_pos=(*coastal_location, 0))
    adv_sprite = BoatSprite(adv)
    sim_sprites.append(adv_sprite)
    auvs = []
    for i in range(BOAT_N_DRONES):
        auv = Submersive(windfarms, adv, name="AUV" + str(i), start_pos=adv.pos)
        auvs.append(auv)
        auv_sprite = SubmersiveSprite(auv)
        sim_sprites.append(auv_sprite)
    adv.set_drones(auvs)

    return adv, auvs


def create_path(control_room, adv):
    destination = control_room.new_path()
    if len(destination) == 0:
        print('Schedular returned no positions.', 'Reverting to hand-rolled scheduling.')
        destination = control_room.find_path()

    adv.set_targets(destination)


sprites = []
windfarms = initialise_windfarm(sprites)
boat, drones = initialise_aquatic_crafts(sprites)
control = ControlRoom(boat, windfarms)


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

    # start from the coast at the start of the day
    if boat.state == VehicleStates.HOLDSTATE and current_time % NANOSECONDS_IN_DAY == 0:
        create_path(control, boat)
    else:
        boat.step()
    for drone in drones:
        drone.step()

    total_power = 0
    for windmill in windfarms:
        windmill.step()
        total_power += windmill.data["Power"]


    ######## SPRITES ########

    # Fill screen with background colour
    screen.fill(BG_COLOUR)
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
        if type(sprite) is SubmersiveSprite or type(sprite) is BoatSprite:
            battery = sprite.getPower()
        if type(sprite) is WindmillSprite:
            prob = sprite.getProb()
            power = sprite.getPower()
        
        # Update sprite for animation
        sprite.update()

        name_pos = position[0] - name.get_width()+25, position[1] - 10
        screen.blit(name, name_pos)
        screen.blit(toBlit, position)

        if prob is not None:
            prob_pos = position[0] - prob.get_width() + 32, position[1] + 15
            screen.blit(prob, prob_pos)
        if battery is not None:
            battery_pos = position[0] - battery.get_width(), position[1]
            screen.blit(battery, battery_pos)
        if power is not None:
            power_pos = position[0] - power.get_width()+25, position[1] 
            screen.blit(power, power_pos)


    ######## FAULT LEGEND ########
    box_size = (int(WIDTH / (10 if HIDEF else 6)), int(HEIGHT / 2.3))
    dot_pos = 0
    text = font.render("Faults", 1, FG_COLOUR)
    screen.blit(text, (WIDTH - box_size[0]/2 - text.get_width(), HEIGHT - box_size[1] + 5))
    for fault in FAULTS:
        hue_diff = 0.9 / len(FAULTS)
        hue = fault["id"] * hue_diff
        colour = hsv_to_rgb(hue, 1, 1)
        colour = tuple(map(lambda x: round(x * 255), colour))
        pygame.draw.circle(screen, colour, (WIDTH - box_size[0] + 20, HEIGHT - box_size[1] + 41 + dot_pos), 8)
        fault_text = fault['human']
        text = font.render(fault_text, 1, FG_COLOUR)
        screen.blit(text, (WIDTH - box_size[0] + 35, HEIGHT - box_size[1] + 29 + dot_pos))
        dot_pos += int((box_size[1] - 30) / len(FAULTS))

    
    ######## SHIP SUMMARY ########
    summary_box = (300, 100)
    summary_box_surface = pygame.Surface(summary_box)
    summary_box_surface.fill(BG_COLOUR)
    text = font.render("Ship summary", 1, FG_COLOUR)
    summary_box_surface.blit(text, (5, 0), text.get_rect())
    # display state
    summary_text = "State : " + boat.state.name
    text = font.render(summary_text, 1, FG_COLOUR)
    summary_box_surface.blit(text, (5, 30), text.get_rect())
    # Get ship battery level
    fuel_level = boat.fuel_level
    # Get boat sprite
    boat_sprite = BoatSprite(boat)
    battery_icon = boat_sprite.getPower()
    # Add text "Total power"
    text = font.render(f"Total fuel : {((fuel_level / BOAT_MAX_FUEL) * 100):.2f}%", 1, FG_COLOUR)
    summary_box_surface.blit(text, (25, 50), text.get_rect())
    # Add Icon next to Total power
    summary_box_surface.blit(battery_icon, (5, 54))
    # Number of drones out
    # Count number of drones out
    num_out = BOAT_N_DRONES - len(boat.drones)
    text = font.render(f"Drones out : {num_out} | Drones in : {BOAT_N_DRONES-num_out}", 1, FG_COLOUR)
    summary_box_surface.blit(text, (25, 70), text.get_rect())
    # Get image of drone
    drone_sprite = pygame.image.load('./sprites/subwhite.png')
    # Add Icon next to drones out
    summary_box_surface.blit(drone_sprite, (5, 74))
    # Blit summary box to screen
    screen.blit(summary_box_surface, (5, HEIGHT - summary_box[1]))


    ######## DRONE LEGEND ########
    drone_box = (300, 100)
    drone_box_surface = pygame.Surface(summary_box)
    drone_box_surface.fill(BG_COLOUR)
    text = font.render("Drone states", 1, FG_COLOUR)
    drone_box_surface.blit(text, (5, 0), text.get_rect())
    # collect some stats
    holding = 0
    moving = 0
    detecting = 0
    count = 0
    for drone in boat.auvs:
        if drone.state == VehicleStates.HOLDSTATE:
            holding += 1
        elif drone.state == VehicleStates.MOVESTATE or drone.state == VehicleStates.RETURNSTATE:
            moving += 1
        elif drone.state == VehicleStates.DETECTSTATE:
            detecting += 1
    # holding drone
    drone_sprite = pygame.image.load('./sprites/subwhite.png')
    drone_box_surface.blit(drone_sprite, (5, 34))
    moving_state_text = VehicleStates.HOLDSTATE.name + ' : ' + str(holding)
    text = font.render(moving_state_text, 1, FG_COLOUR)
    drone_box_surface.blit(text, (25, 30), text.get_rect())
    # moving drone
    drone_sprite = pygame.image.load('./sprites/subred.png')
    drone_box_surface.blit(drone_sprite, (5, 54))
    moving_state_text = VehicleStates.MOVESTATE.name + ' : ' + str(moving)
    text = font.render(moving_state_text, 1, FG_COLOUR)
    drone_box_surface.blit(text, (25, 50), text.get_rect())
    # detect drone
    drone_sprite = pygame.image.load('./sprites/subgreen.png')
    drone_box_surface.blit(drone_sprite, (5, 74))
    moving_state_text = VehicleStates.DETECTSTATE.name + ' : ' + str(detecting)
    text = font.render(moving_state_text, 1, FG_COLOUR)
    drone_box_surface.blit(text, (25, 70), text.get_rect())
    # Blit drone legend to screen
    drone_legend_x = (2 * WIDTH) // 5
    screen.blit(drone_box_surface, (drone_legend_x, HEIGHT - summary_box[1]))


    ######## WEATHER ########
    data_graphic_box = (175, 175)
    # Show Wind Speed
    wind_speed = windfarms[0].data["Wind Speed"]
    # Opensans font

    text = font.render("Wind Speed : "+str(wind_speed) + " m/s", 1, FG_COLOUR)
    screen.blit(text, (5, 10))
    # Show Total Power
    text = font.render("Total Power : "+str(int(total_power / 1000000)) + " MW", 1, FG_COLOUR)
    screen.blit(text, (5, 25))
    # Wind Direction
    wind_direction = windfarms[0].data["Wind Direction"]
    arrow = pygame.image.load('./sprites/up-arrow.png')
    arrow = pygame.transform.rotate(arrow, 360 - int(wind_direction))
    screen.blit(arrow, (84 - int(arrow.get_width()/2), 100 - int(arrow.get_height()/2)))
    text = font.render("Direction : " + str(wind_direction) + u'\N{DEGREE SIGN}', 1, FG_COLOUR)
    screen.blit(text, (5, 40))

    ######## DATE & TIME ########
    text = font.render(nanosecond_string(current_time), 1, FG_COLOUR)
    # Step time
    current_time += int(NANOSECONDS_IN_HOUR * TIME_SCALAR)
    # Center text
    text_width = max(text_width, text.get_width())
    screen.blit(text,(WIDTH - text_width - 5,5))

    # Update the display
    pygame.display.flip()

    if SAVE_IMAGES:
        pygame.image.save(screen, IMAGE_DIR + "/" + str(current_time).zfill(24) + ".png")
        if QUICK_VIEW and current_time > 0:
            exit(0)
        elif current_time >= 2 * NANOSECONDS_IN_DAY:
            exit(0)

    clock.tick(30)

# Done! Time to quit.
pygame.quit()
