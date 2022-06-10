#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:57:05 2022

@author: seanhoyt
"""

import elevator

elev = elevator.Elevator(5, 10)

out = elev.go_to_floor([5, 3, 3], real_time=True, sim_speed = 5)

print(out)