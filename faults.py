# feel free to turn this into a JSON file, pull it, parse it, and return the associated dicts ¯\_(ツ)_/¯
# Annual faults
# TODO add colours to the faults
FAULTS =\
    [
        {"id": 0,  "name": "break-system", "human": "Brake System",
            "probability": 0.0125,  "priority": 1, "timeToDetect": 1},
        {"id": 1,  "name": "cables", "human": "Cables",
            "probability": 0.01,    "priority": 0, "timeToDetect": 1},
        {"id": 2,  "name": "gearbox", "human": "Gearbox",
            "probability": 0.18,    "priority": 2, "timeToDetect": 1},
        {"id": 3,  "name": "generator", "human": "Generator",
            "probability": 0.15,    "priority": 2, "timeToDetect": 1},
        {"id": 4,  "name": "main-frame", "human": "Main Frame",
            "probability": 0.0115,  "priority": 0, "timeToDetect": 1},
        {"id": 5,  "name": "main-shaft", "human": "Main Shaft",
            "probability": 0.04,    "priority": 0, "timeToDetect": 1},
        {"id": 6,  "name": "nacelle", "human": "Nacelle",
            "probability": 0.0125,  "priority": 0, "timeToDetect": 1},
        {"id": 7,  "name": "other", "human": "Other",
            "probability": 0.26,    "priority": 0, "timeToDetect": 1},
        {"id": 8,  "name": "pitch-system", "human": "Pitch System",
            "probability": 0.0125,  "priority": 0, "timeToDetect": 1},
        {"id": 9,  "name": "power-converter", "human": "Power Converter",
            "probability": 0.07,    "priority": 1, "timeToDetect": 1},
        {"id": 10, "name": "rotor-bearings", "human": "Rotor Bearings",
            "probability": 0.01,    "priority": 1, "timeToDetect": 1},
        {"id": 11, "name": "rotor-blades", "human": "Rotor Blades",
            "probability": 0.17,    "priority": 3, "timeToDetect": 1},
        {"id": 12, "name": "rotor-hub", "human": "Rotor Hub",
            "probability": 0.1325,  "priority": 1, "timeToDetect": 1},
        {"id": 13, "name": "screws", "human": "Screws",
            "probability": 0.05,    "priority": 0, "timeToDetect": 1},
        {"id": 14, "name": "tower", "human": "Tower",
            "probability": 0.14,    "priority": 0, "timeToDetect": 1},
        {"id": 15, "name": "transformer", "human": "Transformer",
            "probability": 0.1375,  "priority": 0, "timeToDetect": 1},
        {"id": 16, "name": "yaw-system", "human": "Yaw System",
            "probability": 0.015,   "priority": 0, "timeToDetect": 1},
    ]
