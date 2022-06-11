# elevator-sim

## Overview

`elevator-sim` contains an Elevator class (`elevator.py`) used to create an Elevator object with a `current_floor`, speed (`sec_per_floor`), and the lowest and highest floors of the building (`min_building_floor` and `max_building_floor`). Using the method `go_to_floor`, and providing a list of desired floor destinations, a simulation of the elevator moving between floors is created, resulting in a dataframe containing the entire simulation with an option to output "live" data to the console at a specified simulation speed. The "live" data shows the elevator moving between floors and prints at the current state of the elevator for each time increment of the sim.


## Simulation Assumptions

- the speed of the elevator (seconds per floor) may need to be varied, so this was made an input to the constructor, but has been defaulted to 10. Must be an integer greater than 0.
- At least one of the desired floors must differ from the current floor. Attempting to only request the same floor will raise an exception.
- Time for doors opening/closing at each destination floor is ignored.
- If consecutive duplicate floors are input, the duplications can be ignored. For example, if the desired floors `[3, 5, 5]` are entered, one of the `5`s can be ignored and the simulation will use `[3, 5]`.
- The current floor and desired floors must be inclusively within the min/max building floors that are set in the Elevator constructor


## Files

- `elevator.py`: Contains the Elevator class and is used for running the elevator simulation
- `test_elevator.py`: Contains the unit tests for the Elevator class
- `elevator_driver.py`: Driver file already set up as an example for using the elevator class.
- `elevator_demo.ipynb`: Demo file set up as an example for using the elevator class. This is the same as the `.py` driver, but is in a jupyter notebook and already shows example output.


## Example

```python
# import elevator module (elevator.py)
import elevator
# instantiate elevator object
elev = elevator.Elevator(current_floor = 1, sec_per_floor = 10, 
                         min_building_floor = 1, max_building_floor = 20)
# run simulation with list of desired floors, opt to print out "live" data
# to the console with live_sim, and setting the speed the data will be
# printed
out = elev.go_to_floor([3, 1, 2], live_sim=True, sim_speed = 1)
# print the resulting dataframe containing all the sim data
print(out)
```