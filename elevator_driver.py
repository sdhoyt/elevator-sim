#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script contains a driver for the elevator class

# import the elevator module
import elevator
# create an elevator object and specify the current floor, the elevator speed (sec_per_floor)
# and the lowest/highest floors of the building.
# The below inputs are all the default values for the constructor.
elev = elevator.Elevator(current_floor = 1, sec_per_floor = 10, 
                         min_building_floor = 1, max_building_floor = 20)
# run the go_to_floor method to run the simulation, specify whether a live_sim should be run and set
# the speed that the simulation will output the data to the console
sim_data = elev.go_to_floor([3, 1, 2], live_sim=True, sim_speed = 1)
# print out the dataframe containing the simulation data
print(sim_data)