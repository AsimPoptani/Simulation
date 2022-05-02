from config import N_WINDMILLS_X, N_WINDMILLS_Y
from config import DISTANCE_FROM_SHORE, COASTAL_LOCATION, DIRECTION_OF_WINDFARM
from config import WINDFARM_WIDTH, WINDFARM_HEIGHT
from math import sin, cos

# the windfarm top left corner is the distance from the control centre / coast
start_x = abs(COASTAL_LOCATION[0] + int(DISTANCE_FROM_SHORE * sin(DIRECTION_OF_WINDFARM)))
start_y = abs(COASTAL_LOCATION[1] + int(DISTANCE_FROM_SHORE * cos(DIRECTION_OF_WINDFARM)))

# the horizontal and vertical distances between windmills
x_space = WINDFARM_WIDTH // N_WINDMILLS_X
y_space = WINDFARM_HEIGHT // N_WINDMILLS_Y

# the (generated) positions of all the windmills in meters
locations = []

# code to generate positions
for j in range(N_WINDMILLS_Y):
    for i in range(N_WINDMILLS_X):
        x = start_x + i * x_space
        y = start_y + j * y_space
        locations.append((x, y))
