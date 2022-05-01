from config import N_WINDMILLS_X, N_WINDMILLS_Y, DISTANCE_FROM_SHORE, WINDFARM_WIDTH, WINDFARM_HEIGHT
from math import sin, cos, pi

# the control centre / coast is located at (0,0) and the windfarm at a 45° angle
start_x = int(DISTANCE_FROM_SHORE * sin(pi / 4))
start_y = int(DISTANCE_FROM_SHORE * cos(pi / 4))

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
