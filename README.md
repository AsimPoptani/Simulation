# Simulation for Group C

## Project files

**requirements** - Python dependencies.

**main** - Runs the simulation.

**config** - Consolidation of all configuration variables.

**locations** - Creates a model of Hornsea One.

**display** - Helper functions for converting from kilometers to pixels and back again.

**faults** - Contains relative probabilities, and other data, associated with wind turbine faults.

**time utilities** - Useful constants, and a helper function, for converting time in nanoseconds to a human-readable string.

**Control Room Class** - Functionality for creating ADV paths.

**Schedular Class** - Constraint Solver for finding optimal paths around a wind farm.

**Schedular Test Class** - Test the Schedular class.

**Vehicle Class** - A super class with common functionality for all simulated vehicles.

**Vehicle Enum Class** - A class that enumerates the states of the vehicles.

**Submersive Class** - A subclass of Vehicle that simulates a drone.

**Boat Class** - A subclass of Vehicle that simulates the ADV that deploys the drones.

**Windmill Class** - A class that simulates a windmill.

**hornsea-ws-wd.csv** - Real weather data from NASA for the location near Hornsea One.

**Weather Class** - Simulates weather using data found in `hornsea-ws-wd.csv`

**Sprite Class** - A super class with common functionality for sprites.

**Submersive Sprite Class** - A wrapper class that takes a Submersive object and handles its sprites.

**Boat Sprite Class** - A wrapper class that takes a Boat object and handles its sprites.

**Windmill Sprite Class** - A wrapper class that takes a Windmill object and handles its sprites.

**sprites/** - Directory containing sprite images

**averaging** - Moving average calculations for fault detection.

**images/** - Created when saving images from the simulation, thus may or may not exist.

**OpenSans-Regular.ttf** - Pretty font.

**README.md** - This file.

### Few key notes:

The simulation without running the GUI (so we can quickly test the code), by calling `step()` on each object.

There is a bash script, `simulation`, that sets up the virtual environment and runs the simulation.

See `simulation -h` for details.



### TODO
- [x] Add a description of the project
- [x] Add noise to the simulation
- [x] Get the actual probabilities for windmills breaking down
- [x] Create a list of things we want to simulate e.g. battery life, windmill power out
- [x] Add images instead of circles and squares for the sprites
- [ ] Use a constraint solver/optimizer to find the best solution for swarm
- [x] Base the drone on an actual drone
- [x] Get the planned site for the wind farm
- [x] Simulate the ADV
- [ ] Simulate communications between drones and the master boat
- [x] Create Github Project
- [x] Add team members to the project
- [x] Finalise architecture
- [ ] Simulate inspection
- [x] Minimise time to inspect the complete wind farm
- [ ] Simulate the drone not responding
