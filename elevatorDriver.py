#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:57:05 2022

@author: seanhoyt
"""

import elevator

elev = elevator.Elevator(2, 10)

out = elev.go_to_floor([3, 1, 2], live_sim=True, sim_speed = 5)

#print(out)