#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:59:07 2020

@author: minhuyen
"""
import numpy as np
import random 
from patientConstant import patient_constant

"""A class to create a patient object
"""
class Patient:
    
    def __init__(self, consultation_time, environment):
        
        self.ID = random.randint(0, 100) #This is a unique ID of a patient
        self.gender = random.choice(patient_constant.GENDER) #This is the gender of a patient
        self.race = random.choice(patient_constant.RACE) #This is the race of a patient
        self.age = random.choice(patient_constant.AGE)
        self.arrival_time = random.randint(0, 10, 5) #The time a patient arrives at the ER
        
        # The level of urgency will be generated randomly
        self.levelOfUrgency = random.randint(0, 9) 
        
        # The time a patient spend with a doctor
        if(self.gender == "Male"):
            self.consutation_time = random.normalvarities(patient_constant.MALE_MEAN, 0.0)
        elif(self.gender == "Female"):
            self.consutation_time = random.normalvarities(patient_constant.FEMALE_MEAN, 0.0)
        self.enter_room_time = environment.now # The time a patient enters the examination room
        self.waiting_time = 0 # The time a patient waits to see a doctor
        self.exit_ER = 0 # The time a patient exits the examination room
        
        
    
