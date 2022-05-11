
from enum import Enum

class VehicleStates(Enum):
    # Move state - Will move to a location
    MOVESTATE = 0
    # Detect state - Will inspect a windmill
    DETECTSTATE = 1
    # Hold state - Will hold the current location
    HOLDSTATE = 2
    # Return state - will return to launch location
    RETURNSTATE = 3
