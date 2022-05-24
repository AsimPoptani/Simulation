from math import sin, cos

from config import N_WINDMILLS_X, N_WINDMILLS_Y, MAX_AREA_X, MAX_AREA_Y, DISTANCE_FROM_SHORE, DIRECTION_OF_WINDFARM
from config import WINDFARM_WIDTH, WINDFARM_HEIGHT
from config import HIDEF

# the windfarm bottom left corner is the distance from the control centre / coast
start_x = (7 if HIDEF else 6) * 1000
start_y = 3 * 1000

# the horizontal and vertical distances between windmills
x_space = WINDFARM_WIDTH // N_WINDMILLS_X
y_space = WINDFARM_HEIGHT // N_WINDMILLS_Y

total_size = (WINDFARM_WIDTH * WINDFARM_HEIGHT) / 1000**2

# the (generated) positions of all the windmills in meters
locations = []

min_x = MAX_AREA_X
max_x = 0
min_y = MAX_AREA_Y
max_y = 0

# code to generate positions
for j in range(N_WINDMILLS_Y):
    places = []
    for i in range(N_WINDMILLS_X):

        if j == 0 and i >= 4:
            break
        elif j == 1 and (i == 0 or i >= 5):
            continue
        elif j == 2 and (i < 2 or (8 <= i < 14) or i > 17):
            continue
        elif j == 3 and ((9 <= i < 14) or i > 17):
            continue
        elif j == 4 and i > 17:
            break
        elif j == 5 and i > 18:
            break
        elif j == 6 and i > 19:
            break
        elif j == 7 and i > 20:
            break
        elif (j == 8 or j == 9) and i > 21:
            break
        elif j == 10 and i > 10:
            break
        elif j == 11 and i > 6:
            break
        elif j == 12 and i > 3:
            break

        x = start_x + i * x_space
        y = start_y + j * y_space
        places.append((x, y))

        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    if j % 2 == 1:
        places.reverse()
    for place in places:
        locations.append(place)

coast_x = min_x + DISTANCE_FROM_SHORE * sin(DIRECTION_OF_WINDFARM)
coast_y = max_y + DISTANCE_FROM_SHORE * cos(DIRECTION_OF_WINDFARM)
coastal_location = (coast_x, coast_y)
