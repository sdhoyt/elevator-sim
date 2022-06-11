#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time

class Elevator():
    '''
    Description
    -----------
    Class to represent an Elevator with the ability to simulate moving
    throughout a list of destination floors.

    ...

    Attributes
    ----------
    current_floor : int
        The current floor of the elevator object.
    sec_per_floor : int
        The speed of the elevator in number of seconds to move one floor.        
    min_building_floor: int
        The lowest floor of the building.
    max_building_floor: int
        The highest floor of the building.
    ...
    
    Assumptions
    -----------
    - the speed of the elevator (seconds per floor). Must be an integer.
    
    ...
        
    Example
    -------
    import elevator
    elev = elevator.Elevator(current_floor = 1, sec_per_floor = 10, 
                             min_building_floor = 1, max_building_floor = 20)
    elev.go_to_floor([3, 5], live_sim = True, sim_speed = 2)
    
    
    '''
    def __init__(self, current_floor = 1, sec_per_floor = 10, min_building_floor = 1,
                 max_building_floor = 20):
        
        self.current_floor = self.__validate_current_floor(current_floor, min_building_floor,
                                                           max_building_floor)
        self.sec_per_floor = self.__validate_elevator_speed(sec_per_floor)
        self.min_building_floor = self.__validate_building_floors(min_building_floor)
        self.max_building_floor = self.__validate_building_floors(max_building_floor)
    

    def __validate_current_floor(self, current_floor, min_building_floor, max_building_floor):
        # The purpose of this funtion is to verify that the current floor is 
        # an integer and within the building floor limits
        if (type(current_floor) is not int):
            raise Exception("current floor must be an integer")
        if (current_floor < min_building_floor or current_floor > max_building_floor):
            raise Exception("current floor must be on or within the min/max floors of .\
                            the building")
                            
        return current_floor
    
    
    def __validate_elevator_speed(self, sec_per_floor):
        # the purpose of this function is to verify that the elevator speed 
        # is an integer greater than 0.
        if (sec_per_floor <= 0 or type(sec_per_floor) is not int):
            raise Exception("sec_per_floor must be an integer greater than 0")
            
        return sec_per_floor
   
    
    def __validate_building_floors(self, floor_limit):
        # the purpose of this method is to verify that the building floor limits
        # are integers
        if (type(floor_limit) is not int):
            raise Exception("building floors must be an integer")
        
        return floor_limit
            
    
    def __create_route(self, floor_checkpoints):
        # The purpose of this method is to create a list of every floor along 
        # the route from current floor to the last desired floor
        
        # initial the floor route with the current floor
        route = [self.current_floor]
        
        # for each desired floor
        for i, floor in enumerate(floor_checkpoints):
            # the index is incremented below, so skip the last one to avoid 
            # out of bounds
            if (i < len(floor_checkpoints) - 1):                
                # find the direction (up/down) to travel between desired floors
                direction = int((floor_checkpoints[i + 1] - floor) / abs(floor_checkpoints[i + 1] - floor))
                # get all the floors between the two desired floors    
                route += list(range(floor_checkpoints[i] + direction, floor_checkpoints[i + 1] + direction, direction))
        
        return route


    def __validate_sim_inputs(self, desired_floors, live_sim, sim_speed):
        # The purpose of this method is to check that all inputs are valid
        
        # if the desired floor is an int, make it a list
        if (type(desired_floors) is int):
            desired_floors = [desired_floors]
        # if a single int is not passed in, the desired floors must be in a list
        elif type(desired_floors) is not list:
            raise Exception("desired_floors must be a single floor number (int) or list of floor numbers")
        # the floors in the list must be ints
        elif not all(isinstance(n, int) for n in desired_floors):
            raise Exception("all floors in list must be an integer")
            
        # live_sim must be a boolean
        if type(live_sim) is not bool:
            raise Exception("live_sim, must be a True/False boolean")
        
        # sim_speed must be an integer greater than 0
        if ((type(sim_speed) is not  int and type(sim_speed) is not float) or sim_speed <= 0):
            raise Exception("sim_speed must be an int greater than 0")
        
        # add current floor to the desired floor list to see start -> finish
        desired_floors.insert(0, self.current_floor)    
        # at least one floor in the list must be different than the current floor
        if (len(set(desired_floors)) == 1):
            raise Exception("must enter at least one floor that is not the current floor: {}". \
                            format(self.current_floor))
        

        # desired floors must be at or below the highest building floor
        if (any(x > self.max_building_floor for x in desired_floors)):
            raise Exception("at least one desired floor is higher than the highest building floor.")
        

        # desired floors at or above the lowest building floor
        if (any(x < self.min_building_floor for x in desired_floors)):
            raise Exception("at least one desired floor is lower than the lowest building floor.")
        
        return desired_floors
   
    
    def __clean_sim_inputs(self, floor_checkpoints):  
        # The purpose of this method is to remove any consecutive duplicate
        # floors from the desired floors list. This includes the current floor
        
        # remove any consecutively duplicated floors from the list             
        clean_path = [floor_checkpoints[i] for i in range(len(floor_checkpoints)) if (i==0) or floor_checkpoints[i] != floor_checkpoints[i-1]]
        return clean_path
    
    
    def __get_sim_elapsed_time(self, route):
        # The purpose of this method is to get the elapsed time for each time
        # increment of the simulation
        
        # expand the list of floors in route to line up with the times it takes
        # to transition to each floor. This should be equal length to the 
        # time_elapsed list
        # get the list of time for each floor given the speed of the elevator
        times = list(range(0, len(route) * self.sec_per_floor))
        # remove times that occur after the final floor is reached
        time_elapsed = times[:-self.sec_per_floor + 1]
        
        return time_elapsed
    
    
    def __get_sim_current_floor(self, route):
        # The purpose of this method is to get the current floor for each time
        # increment of the simulation
        
        return np.repeat(route, self.sec_per_floor)[:-self.sec_per_floor + 1]
    
    
    def __get_sim_next_dest(self, floor_checkpoints):
        # The purpose of this method is to get the next destination for each
        # time increment of the simulation
        
        # get the distance (in # of floors) between each floor in the list of 
        # desired floors
        distances = abs(np.array(np.diff(floor_checkpoints), dtype=int))
        # repeat each desired floor based on the distance between the destinations to 
        # align with the time elapsed
        destinations = np.repeat(np.repeat(floor_checkpoints[1:], distances), self.sec_per_floor)
        # append a nan to end to indicate that there are not more destinations
        next_destination = np.append(destinations, np.nan)  
        
        return next_destination
    
    
    def __get_sim_floors_to_next_dest(self, next_destination, current_floor):
        # The purpose of this method is to get the number of floors to the next
        # destination for each time increment of the simulation
        
        # subtract the next destination floor from the current cloor to find
        # the number of floors until next destination
        return abs(next_destination - current_floor)
    
    def __get_sim_time_to_next_dest(self, route, floors_to_next_dest):
        # The purpose of this method is to get the time to the next destination
        # for each time increment of the simulation
        
        # get a floor transition countdown list in seconds 
        floor_transition_countdown = np.array(range(self.sec_per_floor, 0, -1), dtype=int)
        # duplicate the floor transition countdown list for each floor in route and remove
        # the excess times that occur after the reaching the final floor
        time_to_next_floor  = np.tile(floor_transition_countdown, len(route))[:-self.sec_per_floor + 1]
        # remove the time for the final floor and replace with Nan since there 
        # are no more floors in the route
        time_to_next_floor = np.append(time_to_next_floor[:-1], np.nan)
        # get the time to the next destination
        time_to_next_dest = ((floors_to_next_dest - 1) * self.sec_per_floor) + time_to_next_floor
        
        return time_to_next_dest
    
    
    def __create_dataframe(self, time_elapsed, current_floor, floors_to_next_dest,
                           time_to_next_dest, next_destination):
        # The purpose of this method is to create the dataframe containing 
        # the simulation data
    
        sim_data = pd.DataFrame({
            "time_elapsed":time_elapsed,
            "current_floor":current_floor,
            "floors_to_next_dest":floors_to_next_dest,
            "time_to_next_dest":time_to_next_dest,
            "next_destination":next_destination
            }, dtype=int)
        
        # convert next destination and floors to next destination to ints which 
        # were converted to floats during np.append()
        sim_data["next_destination"] = sim_data["next_destination"].convert_dtypes(int)
        sim_data["floors_to_next_dest"] = sim_data["floors_to_next_dest"].convert_dtypes(int)  
        sim_data["time_to_next_dest"] = sim_data["time_to_next_dest"].convert_dtypes(int)  
        
        return sim_data
    
    
    def __run_live_sim(self, sim_data, sim_speed):
        # The purpose of this method to to run a live simulation by
        # printing the data to the console as the elevator moves between floors
        
        # for each row in the sim dataframe
        for index, row in sim_data.iterrows():
            
            # if the final floor has not yet been reached
            if (index != sim_data.shape[0] - 1):
                # print the elevator sim data
                print("elapsed time: {}sec | current floor: {} | next destination: {}". \
                      format(row["time_elapsed"], row["current_floor"], row["next_destination"]))
                print("floors to next destination: {} | time to next destination: {}sec\n". \
                      format(row["floors_to_next_dest"], row["time_to_next_dest"]))   
                    
                # pause the sim based on desired sim speed
                time.sleep(1/sim_speed)
                
            # when the final floor is reached    
            else:
                print("elapsed time: {}sec | current floor: {}". \
                      format(row["time_elapsed"], row["current_floor"]))
                print("Final destination reached.")
        
        
    def go_to_floor(self, desired_floors, live_sim = True, sim_speed = 1):
        '''
        Description
        -----------
        go_to_floor runs a simulation of an elevator moving between its current
        and one or more desired floor destinations. This method outputs a pandas
        DataFrame containing the simulation data. Additionaly, there are two 
        optional arguements to run a "live" simulation that prints the data to 
        the console at a speed dictated by the sim_speed argument.
        
        Assumptions
        -----------
        - At least one of the desired floors must differ from the current floor.
            Attempting to only request the same floor will raise an exception.
        - Time for doors opening/closing at each destination floor is ignored.
        - If consecutive duplicate floors are input, the duplications can be ignored.
            For example, if the desired floors [3, 5, 5] are entered, one of the 5s can
            be ignored and the simulation will use [3, 5].
        - The desired floors must be inclusively within the min/max building floors
            that are set in the Elevator constructor
        
        Parameters
        ----------
        desired_floors : int or list containing ints
            The floor(s) for the elevator to travel to.
        live_sim : boolean, optional
            Determines whether a "live" simulation is run where the 
            elevator data is output to the console as it moves between floors. 
            The default is True.
        sim_speed : int or float > 0, optional
            Determines the speed of the simulation relative to a 1 second time
            increment. For example, if sim_speed is 0.5, the simulation runs at 
            half the speed as the time increment being used in the simulation. If 
            sim_speed is 2, then the simulation is running at twice the speed as
            the time increment being use. 
            If live_sim is false, sim_speed is ignored.
            The default is 1.

        Returns
        -------
        sim_data : DataFrame
            DataFrame containing all the elevator simulation data. 
            The columns of the DataFrame are as follows:  
                - time_elapsed: total time elapsed for each time increment of simulation.
                - current_floor: current floor for each time increment of simulation.
                - floors_to_next_dest: number of floors to next destination for each 
                    time increment of simulation.
                - time_to_next_dest: number of seconds to the next destination for
                    each time incremement of simulation.
                - next_destination: next floor destination for each time increment
                    of the simulation.
        '''
        
        ###############################
        ## Validate and clean inputs ##
        ###############################
        # confirm that all inputs are valid
        floor_checkpoints = self.__validate_sim_inputs(desired_floors, live_sim, sim_speed)
        # clean inputs to remove any sequentially duplicated floors
        floor_checkpoints = self.__clean_sim_inputs(floor_checkpoints)      

        ###############################
        ## Calculate simulation data ##
        ###############################
        # create the full elevator route to reach each desired floor
        route = self.__create_route(floor_checkpoints)                
        # get the total elapsed time for each time increment of the simulation
        time_elapsed = self.__get_sim_elapsed_time(route)
        # get the current floor for each time increment of the simulation
        current_floor = self.__get_sim_current_floor(route)
        # get the next destination for each time increment of the simulation
        next_destination = self.__get_sim_next_dest(floor_checkpoints) 
        # get the floors to the next destination for each time increment 
        # of the simulation
        floors_to_next_dest = self.__get_sim_floors_to_next_dest(next_destination, current_floor)
        # get the time to the next destination for each time increment of
        # the simulation
        time_to_next_dest = self.__get_sim_time_to_next_dest(route, floors_to_next_dest)
        
        ###########################
        ## Construct a DataFrame ##
        ###########################
        # Construct a dataframe for the entire simulation
        sim_data = self.__create_dataframe(time_elapsed, current_floor, 
                                          floors_to_next_dest, time_to_next_dest,
                                          next_destination)           
        #########################
        ## Run live simulation ##
        #########################
        # if a live simulation is requested
        if live_sim:
            self.__run_live_sim(sim_data, sim_speed)

        ################################
        ## Save state and output data ##
        ################################
        # Retain the final elevator position and output the sim data
        self.current_floor = sim_data.current_floor.values[-1]
        
        return sim_data
