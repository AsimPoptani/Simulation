import math

WIDTH = 768
HEIGHT = 768

N_WINDMILLS_X = 22
N_WINDMILLS_Y = 13

MIN_AREA_X = 0
MIN_AREA_Y = 0
MAX_AREA_X = 370000
MAX_AREA_Y = 370000
COASTAL_LOCATION = (0, 350000)
DISTANCE_FROM_SHORE = 120000
WINDFARM_WIDTH = 252000 #252km
WINDFARM_HEIGHT = WINDFARM_WIDTH
DIRECTION_OF_WINDFARM = math.radians( 45 )

# Width of the turbines
ROTOR_DIAMETER = 154 
ROTOR_RADIUS = ROTOR_DIAMETER // 2
TURBINE_HEIGHT = 190

MAX_POWER = 7000000
AIR_DENSITY = 1.225 # At sea level

# TODO fix these values
DRONE_MAX_VELOCITY = 1000
# km
DRONE_MAX_BATTERY = 100
# km
DRONE_MAX_COMMUNICATION_RANGE = 10000

DRONE_MAX_DETECTION_RANGE = 10

DRONE_RADIUS = 1
DRONE_SAFE_ZONE = 2

DATA_UPDATE_INTERVAL = 20
FAULT_RATE_DIVISOR = 24 * 60 * 60
