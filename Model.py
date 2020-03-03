#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 15:11:19 2020

@author: minhuyen
"""
import simpy
from patient import Patient
from priority_queue import PriorityQueue as pq
""" This class is used to model the simulation
"""

class Model:
    
    rooms_available = []
    doctors_available = []
    # Lists used to store update results
    update_time = []
    update_patients_in_ED = []
    update_patients_waiting = []
    update_patients_out_ED = []


    # Set up counter for number fo patients entering simulation
    patient_count = 0

    # Set up running counts of patients waiting (total and by priority)
    patients_waiting = 0
    patients_waiting_by_priority = [0, 0, 0]
    
    
    def patient_in_ED(Patient):
        pq.add(Patient)
        
    def patient_in_room(Patient):
        update_patients_waiting
    
    def patien_out_ED(Patient):
        update_patients_out_ED
        update_patients_waiting
        update_patients_in_ED
        
    def room_available:
        rooms_available
    
    