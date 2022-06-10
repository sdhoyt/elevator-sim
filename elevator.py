#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:28:45 2022

@author: seanhoyt
"""
import numpy as np
import pandas as pd
import time

class Elevator():
    def __init__(self, current_floor = 1, sec_per_floor = 10):
        
        self.current_floor = current_floor
        self.sec_per_floor = sec_per_floor
        
    
    def __create_route(self, desired_floors):
        # initial the floor route with the current floor
        route = [self.current_floor]
        
        # for each desired floor
        for i, floor in enumerate(desired_floors):
            # the index is incremented below, so skip the last one to avoid 
            # out of bounds
            if (i < len(desired_floors) - 1):                
                # find the direction (up/down) to travel between desired floors
                direction = int((desired_floors[i + 1] - floor) / abs(desired_floors[i + 1] - floor))
                # get all the floors between the two desired floors    
                route += list(range(desired_floors[i] + direction, desired_floors[i + 1] + direction, direction))
        
        return route


    def __validate_inputs(self, desired_floors, real_time):
        # if the desired floor is an int, make it a list
        if (type(desired_floors) is int):
            desired_floors = [desired_floors]
        # if a single int is not passed in, the desired floors must be in a list
        elif type(desired_floors) is not list:
            raise Exception("desired_floors must be an single floor number (int) or list of floor numbers")
        # the floors in the list must be ints
        elif not all(isinstance(n, int) for n in desired_floors):
            raise Exception("all floors in list must be an integer")
        # real_time must be a boolean
        if type(real_time) is not bool:
            raise Exception("real_time, must be a True/False boolean")
        
        # add current floor to the desired floor list to see start -> finish
        desired_floors.insert(0, self.current_floor)    
        
        # at least one floor in the list must be different than the current floor
        if all(floor >= self.current_floor for floor in desired_floors):
            raise Exception("must enter at least one floor that is not the current floor: {}". \
                            format(self.current_floor))
        
        return desired_floors
   
    
    def __clean_inputs(self, desired_floors):  
        # remove any sequentially duplicated floors from the list             
        clean_path = [desired_floors[i] for i in range(len(desired_floors)) if (i==0) or desired_floors[i] != desired_floors[i-1]]
        return clean_path
    
    
    def __create_dataframe(self, time_elapsed, current_floor, floors_to_next_dest,
                           time_to_next_floor, next_destination):
        return pd.DataFrame({
            "time_elapsed":time_elapsed,
            "current_floor":current_floor,
            "floors_to_next_dest":floors_to_next_dest,
            "time_to_next_floor":time_to_next_floor,
            "next_destination":next_destination
            }, dtype=int)
        
    
    def go_to_floor(self, desired_floors, real_time = True, sim_speed = 1):
        
        
        # check that all inputs are valid
        desired_floors = self.__validate_inputs(desired_floors, real_time)
        # clean inputs to remove any sequentially duplicated floors
        desired_floors = self.__clean_inputs(desired_floors)
        
        # create the full elevator route to reach each desired floor
        route = self.__create_route(desired_floors)                
        
        # get the list of time for each floor given the speed of the elevator
        times = list(range(0, len(route) * self.sec_per_floor))
        # remove times that occur after the final floor is reached
        time_elapsed = times[:-self.sec_per_floor + 1]
        
        # expand the list of floors in route to line up with the times it takes
        # to transition to each floor. This should be equal length to the 
        # time_elapsed list
        current_floor = np.repeat(route, self.sec_per_floor)[:-self.sec_per_floor + 1]
        
        # get a floor transition countdown list in seconds 
        floor_transition_countdown = np.array(range(self.sec_per_floor, 0, -1), dtype=int)
        # duplicate the floor transition countdown list for each floor in route and remove
        # the excess times that occur after the reaching the final floor
        time_to_next_floor  = np.tile(floor_transition_countdown, len(route))[:-self.sec_per_floor + 1]
        # remove the time for the final floor and replace with Nan since there 
        # are no more floors in the route
        time_to_next_floor = np.append(time_to_next_floor[:-1], np.nan)
        
        
        #desired_floors.insert(0, 5)
        
        # get the distance (in # of floors) between each floor in the list of 
        # desired floors
        distances = abs(np.array(np.diff(desired_floors), dtype=int))
        # repeat each desired floor based on the distance between the destinations to 
        # align with the time elapsed
        destinations = np.repeat(np.repeat(desired_floors[1:], distances), self.sec_per_floor)
        # append a nan to end to indicate that there are not more destinations
        next_destination = np.append(destinations, np.nan)  
        # subtract the next destination floor from the current cloor to find
        # the number of floors until next destination
        floors_to_next_dest = abs(next_destination - current_floor)
        
        # create a dataframe with the lists calculated above
        sim_out = self.__create_dataframe(time_elapsed, current_floor, 
                                          floors_to_next_dest, time_to_next_floor,
                                          next_destination)
                
        
        # convert next destination and floors to next destination to ints which 
        # were converted to floats during np.append()
        sim_out["next_destination"] = sim_out["next_destination"].convert_dtypes(int)
        sim_out["floors_to_next_dest"] = sim_out["floors_to_next_dest"].convert_dtypes(int)               
        
        # if a real time simulation is requested
        if real_time:
            # for each row in the sim dataframe
            for index, row in sim_out.iterrows():
                # print the elevator sim data
                print("elapsed time: {}sec current floor: {} next destination: {}". \
                      format(row["time_elapsed"], row["current_floor"], row["next_destination"]))
                print("floors to next destination: {} time to next floor: {}sec". \
                      format(row["floors_to_next_dest"], row["time_to_next_floor"]))
                # pause the sim based on desired sim speed
                time.sleep(1/sim_speed)
        
        # update the current floor for next set of desired floors
        self.current_floor = sim_out.current_floor.values[-1]
        
        return sim_out
            
        
        
        
            

