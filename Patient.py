#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:59:07 2020

@author: minhuyen
"""
import numpy as np
import random 

"""A class to create a patient object
"""
class Patient:
    
    def __init__(self, consultation_time, appointment_time_mean, \
                 appointment_time_std, environment):
        
        self.ID = 0 #This is a unique ID of a patient
        self.gender = "Male" #This is the gender of a patient
        self.race = "American" #This is the race of a patient
        self.arrival_time = 1 #The time a patient arrives at the ER
        
        # The level of urgency will be generated randomly
        self.levelOfUrgency = random.randint(0, 9) 
        
        # The time a patient spend with a doctor
        self.consutation_time = random.normalvarities(appointment_time_mean, appointment_time_std)
        self.enter_room_time = environment.now # The time a patient enters the examination room
        self.waiting_time = 0 # The time a patient waits to see a doctor
        self.exit_ER = 0 # The time a patient exits the examination room
        
        
    