# feel free to turn this into a JSON file, pull it, parse it, and return the associated dicts ¯\_(ツ)_/¯
# Annual faults
# TODO add colours to the faults
FAULTS =\
    [
        {"id" : 0,  "name": "break-system",    "probability": 0.0125,  "priority" : 1, "timeToDetect": 1},
        {"id" : 1,  "name": "cables",          "probability": 0.01,    "priority" : 0, "timeToDetect": 1},
        {"id" : 2,  "name": "gearbox",         "probability": 0.18,    "priority" : 2, "timeToDetect": 1},
        {"id" : 3,  "name": "generator",       "probability": 0.15,    "priority" : 2, "timeToDetect": 1},
        {"id" : 4,  "name": "main-frame",      "probability": 0.0115,  "priority" : 0, "timeToDetect": 1},
        {"id" : 5,  "name": "main-shaft",      "probability": 0.04,    "priority" : 0, "timeToDetect": 1},
        {"id" : 6,  "name": "nacelle",         "probability": 0.0125,  "priority" : 0, "timeToDetect": 1},
        {"id" : 7,  "name": "other",           "probability": 0.26,    "priority" : 0, "timeToDetect": 1},
        {"id" : 8,  "name": "pitch-system",    "probability": 0.0125,  "priority" : 0, "timeToDetect": 1},
        {"id" : 9,  "name": "power-converter", "probability": 0.07,    "priority" : 1, "timeToDetect": 1},
        {"id" : 10, "name": "rotor-bearings",  "probability": 0.01,    "priority" : 1, "timeToDetect": 1},
        {"id" : 11, "name": "rotor-blades",    "probability": 0.17,    "priority" : 3, "timeToDetect": 1},
        {"id" : 12, "name": "rotor-hub",       "probability": 0.1325,  "priority" : 1, "timeToDetect": 1},
        {"id" : 13, "name": "screws",          "probability": 0.05,    "priority" : 0, "timeToDetect": 1},
        {"id" : 14, "name": "tower",           "probability": 0.14,    "priority" : 0, "timeToDetect": 1},
        {"id" : 15, "name": "transformer",     "probability": 0.1375,  "priority" : 0, "timeToDetect": 1},
        {"id" : 16, "name": "yaw-system",      "probability": 0.015,   "priority" : 0, "timeToDetect": 1},
    ]
