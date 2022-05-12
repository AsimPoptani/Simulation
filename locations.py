from config import N_WINDMILLS_X, N_WINDMILLS_Y
from config import DISTANCE_FROM_SHORE, COASTAL_LOCATION, DIRECTION_OF_WINDFARM
from config import WINDFARM_WIDTH, WINDFARM_HEIGHT
from math import sin, cos

# the windfarm bottom left corner is the distance from the control centre / coast
start_x = abs(COASTAL_LOCATION[0] + int(DISTANCE_FROM_SHORE * sin(DIRECTION_OF_WINDFARM)))
start_y = abs(WINDFARM_HEIGHT - COASTAL_LOCATION[1] + int(DISTANCE_FROM_SHORE * cos(DIRECTION_OF_WINDFARM)))

# the horizontal and vertical distances between windmills
x_space = WINDFARM_WIDTH // N_WINDMILLS_X
y_space = WINDFARM_HEIGHT // N_WINDMILLS_Y

# the (generated) positions of all the windmills in meters
locations = []

# code to generate positions
for j in range(N_WINDMILLS_Y):
    places = []
    for i in range(N_WINDMILLS_X):

        if j == 0 and i >= 4:
            break
        elif j == 1 and (i == 0 or i >= 5):
            continue
        elif j == 2and (i < 2 or (i >= 8 and i < 14) or i > 17):
            continue
        elif j == 3 and ((i >= 9 and i < 14) or i > 17):
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
    if j % 2 == 1:
        places.reverse()
    for place in places:
        locations.append(place)
