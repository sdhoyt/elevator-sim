#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 17:28:45 2022

@author: seanhoyt
"""
import numpy as np
import pandas as pd
import warnings
import time

class Elevator():
    def __init__(self, current_floor = 1, sec_per_floor = 10):
        
        self.current_floor = current_floor
        self.sec_per_floor = sec_per_floor # seconds / floor
        
    
    def __create_route(self, floor_path):
        print(floor_path)
        route = [self.current_floor]
        
        for i, floor in enumerate(floor_path):
            if (i < len(floor_path) - 1):
                
                direction = int((floor_path[i + 1] - floor) / abs(floor_path[i + 1] - floor))
                    
                route += list(range(floor_path[i] + direction, floor_path[i + 1] + direction, direction))
        
        return route


    def __validate_inputs(self, desired_floors, real_time):
        if (type(desired_floors) is int):
            desired_floors = [desired_floors]
        elif type(desired_floors) is not list:
            raise Exception("desired_floors must be an single floor number (int) or list of floor numbers")
        elif not all(isinstance(n, int) for n in desired_floors):
            raise Exception("all floors in list must be an integer")
        
        if type(real_time) is not bool:
            raise Exception("real_time, must be a True/False boolean")
        
        desired_floors.insert(0, self.current_floor)    
        
        if all(floor >= self.current_floor for floor in desired_floors):
            raise Exception("must enter at least one floor that is not the current floor: {}". \
                            format(self.current_floor))
        
        return desired_floors
   
    
    def __clean_inputs(self, desired_floors):               
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
        
        
        
        desired_floors = self.__validate_inputs(desired_floors, real_time)
        desired_floors = self.__clean_inputs(desired_floors)
        
        print(desired_floors)
        
        
        route = self.__create_route(desired_floors)                
        
        time_elapsed = list(range(0, len(route) * self.sec_per_floor))[:-self.sec_per_floor + 1]
        current_floor = np.repeat(route, self.sec_per_floor)[:-self.sec_per_floor + 1]
        time_to_next_floor  = np.tile(np.array(range(self.sec_per_floor, 0, -1), dtype=int), len(route))[:-self.sec_per_floor + 1]
        time_to_next_floor = np.append(time_to_next_floor[:-1], np.nan)
        desired_floors.insert(0, 5)
        distances = abs(np.array(np.diff(desired_floors), dtype=int))
        destinations = np.repeat(np.repeat(desired_floors[1:], distances), self.sec_per_floor)
        all_dest = np.append(destinations, np.nan)
        next_destination = all_dest        
        floors_to_next_dest = abs(next_destination - current_floor)
        
        sim_out = self.__create_dataframe(time_elapsed, current_floor, 
                                          floors_to_next_dest, time_to_next_floor,
                                          next_destination)
                
        
        sim_out["next_destination"] = sim_out["next_destination"].convert_dtypes(int)
        sim_out["floors_to_next_dest"] = sim_out["floors_to_next_dest"].convert_dtypes(int)               
        
        if real_time:
            for index, row in sim_out.iterrows():
                print("elapsed time: {}sec current floor: {} next destination: {}". \
                      format(row["time_elapsed"], row["current_floor"], row["next_destination"]))
                print("floors to next destination: {} time to next floor: {}sec". \
                      format(row["floors_to_next_dest"], row["time_to_next_floor"]))
                time.sleep(1/sim_speed)
        
        self.current_floor = sim_out.current_floor.values[-1]
        
        return sim_out
            
        
        
        
            

