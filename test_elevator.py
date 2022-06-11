#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import elevator
import pandas as pd
import numpy as np

class TestElevator(unittest.TestCase):
    
    
    def test_sec_to_floor_not_int(self):
        # elevator speed must be an integer
        self.assertRaises(Exception, elevator.Elevator(2, 10), 2, .5)
        
        
    def test_sec_to_floor_zero_or_less(self):
        # elevator speed must greater than zero
        self.assertRaises(Exception, elevator.Elevator(2, 10), 2, -1)
        
        
    def test_current_floor_is_not_int(self):
        # current floor must be an integer
        self.assertRaises(Exception, elevator.Elevator(2, 10), 2.5)
        
        
    def test_current_floor_is_higher_than_building_limit(self):
       # current floor must be on or higher than the lowest building floor
       self.assertRaises(Exception, elevator.Elevator(2, 10), current_floor = 50, 
                         sec_per_floor = 10, min_building_floor = 1, 
                         max_building_floor = 10) 
       
       
    def test_current_floor_is_higher_than_building_limit(self):
        # current floor be on or lower than the highest building floor
        self.assertRaises(Exception, elevator.Elevator(2, 10), current_floor = -1, 
                          sec_per_floor = 10, min_building_floor = 1, 
                          max_building_floor = 10) 


    def test_building_floor_limit_not_integer(self):
        # building floor limits (min/max) must be integers
        self.assertRaises(Exception, elevator.Elevator(2, 10), current_floor = -1, 
                          sec_per_floor = 10, min_building_floor = .5, 
                          max_building_floor = 10)


    def test_go_to_floor_integer_input(self):
        # desired floor input can be an integer
        elev = elevator.Elevator(2, 10)
        
        desire_floors_test = 3
        
        ### Expected output
        expected_output = pd.DataFrame({
            "time_elapsed":[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "current_floor":[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            "floors_to_next_dest":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, np.nan],
            "time_to_next_dest":[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, np.nan],
            "next_destination":[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, np.nan]
            })

        expected_output["floors_to_next_dest"] = expected_output["floors_to_next_dest"].convert_dtypes(int)
        expected_output["time_to_next_dest"] = expected_output["time_to_next_dest"].convert_dtypes(int)
        expected_output["next_destination"] = expected_output["next_destination"].convert_dtypes(int)
        
        t1_out = elev.go_to_floor(desire_floors_test, False)
        
        self.assertTrue(t1_out.equals(expected_output))
    
    
    def test_go_to_floor_input_list(self):
        # desired floor input can be a list of integers
        elev = elevator.Elevator(2, 10)
        
        desire_floors_test = [1, 3]
        
        ### Expected output
        expected_output = pd.DataFrame({
            "time_elapsed":[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                            29, 30],
            "current_floor":[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 
                             1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            "floors_to_next_dest":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 
                                   2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, np.nan],
            "time_to_next_dest":[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 20, 19, 18, 17, 
                                 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 
                                 3, 2, 1, np.nan],
            "next_destination":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3,
                                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, np.nan]
            })

        expected_output["floors_to_next_dest"] = expected_output["floors_to_next_dest"].convert_dtypes(int)
        expected_output["time_to_next_dest"] = expected_output["time_to_next_dest"].convert_dtypes(int)
        expected_output["next_destination"] = expected_output["next_destination"].convert_dtypes(int)
        
        t1_out = elev.go_to_floor(desire_floors_test, False)
        
        self.assertTrue(t1_out.equals(expected_output))
        
        
    def test_go_to_floor_inputs_with_consec_dups(self):
        # inputs with consecuative duplicates are cleaned so the next
        # floor is always different ie. [1, 1, 3, 3] -> [1, 3]
        elev = elevator.Elevator(2, 10)
        
        desire_floors_test = [1, 1, 3, 3]
        
        ### Expected output
        expected_output = pd.DataFrame({
            "time_elapsed":[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                            29, 30],
            "current_floor":[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 
                             1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            "floors_to_next_dest":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 
                                   2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, np.nan],
            "time_to_next_dest":[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 20, 19, 18, 17, 
                                 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 
                                 3, 2, 1, np.nan],
            "next_destination":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3,
                                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, np.nan]
            })

        expected_output["floors_to_next_dest"] = expected_output["floors_to_next_dest"].convert_dtypes(int)
        expected_output["time_to_next_dest"] = expected_output["time_to_next_dest"].convert_dtypes(int)
        expected_output["next_destination"] = expected_output["next_destination"].convert_dtypes(int)
        
        t1_out = elev.go_to_floor(desire_floors_test, False)
        
        self.assertTrue(t1_out.equals(expected_output))
        
    
    def test_go_to_floor_first_desired_is_same_as_current(self):
        # if the first desired floor is the same as the current, then it should
        # be ignored
        elev = elevator.Elevator(2, 10)
        
        desire_floors_test = [2, 1, 3]
        
        ### Expected output
        expected_output = pd.DataFrame({
            "time_elapsed":[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                            29, 30],
            "current_floor":[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 
                             1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3],
            "floors_to_next_dest":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 
                                   2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1 ,1, 1, 1, np.nan],
            "time_to_next_dest":[10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 20, 19, 18, 17, 
                                 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 
                                 3, 2, 1, np.nan],
            "next_destination":[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3,
                                3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, np.nan]
            })

        expected_output["floors_to_next_dest"] = expected_output["floors_to_next_dest"].convert_dtypes(int)
        expected_output["time_to_next_dest"] = expected_output["time_to_next_dest"].convert_dtypes(int)
        expected_output["next_destination"] = expected_output["next_destination"].convert_dtypes(int)
        
        t1_out = elev.go_to_floor(desire_floors_test, False)
        
        self.assertTrue(t1_out.equals(expected_output))
        
        
    def test_go_to_floor_input_not_list_or_int(self):
        # tests excpetion when inputting a non list / int
        elev = elevator.Elevator(2, 10)        
        self.assertRaises(Exception, elev.go_to_floor, "3", False)
      
        
    def test_go_to_floor_list_input_not_int(self):
        # tests exception when list contains a non-int
        elev = elevator.Elevator(2, 10)
        self.assertRaises(Exception, elev.go_to_floor, [1, 4, "5"], False)
    
    
    def test_go_to_floor_realtime_not_bool(self):
        # tests exception when list contains a non-int
        elev = elevator.Elevator(2, 10)
        self.assertRaises(Exception, elev.go_to_floor, [1, 2, 3], "not a bool")
        
        
    def test_go_to_floor_all_floors_are_current(self):
        # tests exception when list contains a non-int
        elev = elevator.Elevator(2, 10)
        self.assertRaises(Exception, elev.go_to_floor, [2, 2, 2], False)
            

    def test_go_to_floor_sim_speed_not_numeric(self):
        #sim_speed must be numeric
        elev = elevator.Elevator(2, 10)
        self.assertRaises(Exception, elev.go_to_floor, [2, 2, 2], True, "3")
        
        
    def test_go_to_floor_sim_speed_less_than_equal_zero(self):
        #sim_speed must greater than zero
        elev = elevator.Elevator(2, 10)
        self.assertRaises(Exception, elev.go_to_floor, [2, 2, 2], True, -1)
    
    
    def test_go_to_floor_desired_floor_greater_than_building_max(self):
        # all desired floors must be on or below the highest building floor
        elev = elevator.Elevator(2, 10, 1, 10)
        self.assertRaises(Exception, elev.go_to_floor, [2, -1, 20], True, -1)


    def test_go_to_floor_desired_floor_less_than_building_min(self):
        # all desired floors must be on or above the lowest building floor
        elev = elevator.Elevator(2, 10, 1, 10)
        self.assertRaises(Exception, elev.go_to_floor, [2, -1, 5], True, -1)
        
        
if __name__ == '__main__':
    unittest.main()