# elevator-sim

## Overview
`elevator-sim` contains an Elevator class used to create an Elevator object with a `current_floor` and speed `sec_per_floor`. Using the method `got_to_floor`, and providing a list of desired floor destination, a simulation of the elevator moving between floors in created, resulting in a dataframe containing the entire simulation with an option to output "live" data to the console at a specified simulation speed. The "live" data shows the elevator moving between floors and prints at the current state of the elevator for each increment of the sim.


## Files
- `elevator.py`: Contains the Elevator class and is used for running the elevator simulation
- `test_elevator.py`: Contains the unit tests for the Elevator class
- `elevator_driver.py`: Driver file already set up as an example for using the elevator class.
- `elevator_demo.ipynb`: Demo file set up as an example for using the elevator class. This is the same as the `.py` driver, but is in a jupyter notebook and already shows example output.


## Example
```python
import elevator

elev = elevator.Elevator(current_floor = 2, sec_per_floor = 10)

out = elev.go_to_floor([3, 1, 2], live_sim=True, sim_speed = 1)

print(out)
```