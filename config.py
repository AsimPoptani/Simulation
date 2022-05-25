import math

# simulation options
QUICK_VIEW = False
SAVE_IMAGES = False
HIDEF = False
IMAGE_DIR = 'images'

# display dimensions
WIDTH = 1920 if HIDEF else 1024
HEIGHT = 1080 if HIDEF else 768
HEIGHT_RATIO = 1
WIDTH_RATIO = HEIGHT / WIDTH

# number of wind turbines and layout
N_WINDMILLS = 175
N_WINDMILLS_X = 22
N_WINDMILLS_Y = 13

# physical dimensions of the simulation in meters
MIN_AREA_X = 0
MIN_AREA_Y = 0
MAX_AREA_X = (26 if HIDEF else 32) * 1000
MAX_AREA_Y = (26 if HIDEF else 32) * 1000
# top left corner of the wind farm
START_X = (7 if HIDEF else 6) * 1000
START_Y = 3 * 1000
# miscellaneous wind farm details
COASTAL_LOCATION = (0, 35 * 1000)
DISTANCE_FROM_SHORE = 120 * 1000
DISTANCE_BETWEEN_TURBINES = math.sqrt((407 * pow(1000, 2)) / N_WINDMILLS)
WINDFARM_WIDTH = N_WINDMILLS_X * DISTANCE_BETWEEN_TURBINES
WINDFARM_HEIGHT = N_WINDMILLS_Y * DISTANCE_BETWEEN_TURBINES
DIRECTION_OF_WINDFARM = math.radians(180 + 105)

# dimensions of the turbines
ROTOR_DIAMETER = 154 
ROTOR_RADIUS = ROTOR_DIAMETER // 2
TURBINE_HEIGHT = 190

MAX_POWER = 7000000
AIR_DENSITY = 1.225  # At sea level

# RGB tuple
BG_COLOUR = (0, 105, 148)
FG_COLOUR = (255, 255, 255)

# hours
TIME_SCALAR = 1 / 6

# meters per tick
DRONE_MAX_VELOCITY = 7 * 1000
# hours
DRONE_HOURS_POWER = 8
# km
DRONE_MAX_BATTERY = DRONE_HOURS_POWER * DRONE_MAX_VELOCITY
# km
DRONE_MAX_COMMUNICATION_RANGE = 6 * 1000
# ticks
DRONE_MAX_DETECTION_RANGE = 10
# dimensions of drone in meters
DRONE_RADIUS = 5
# maximum number of targets each drone can be allocated
DRONE_MAX_TARGETS = 7
# hours
INSPECTION_TIME = 1 / 6

# meters
BOAT_RADIUS = 84
# hours
BOAT_MAX_FUEL = 120 * 24
# meters per tick
BOAT_MAX_VELOCITY = 20 * 1000
# number of drones per boat
BOAT_N_DRONES = 30

# value by which the probabilities are divided
FAULT_RATE_DIVISOR = 365 * 24 * 60
# ticks
SIMULATION_TIME_FAULTS = 7 * 24 * 60

# meters
CIRCUMNAVIGATION_DISTANCE = (2 * math.pi * (DRONE_RADIUS + ROTOR_RADIUS))
# meters
MAX_SCAN_DISTANCE = (DRONE_MAX_BATTERY / 2) - (TIME_SCALAR * DRONE_MAX_VELOCITY)

# ticks
TIME_TO_NEXT_INSPECTION = round(24 / TIME_SCALAR)
