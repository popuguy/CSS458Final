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
        self.consutation_time = patient_constant.MEAN_ALL_VISITS
        
        if(self.gender == "Male"):      #- Gender attribute
            self.consutation_time *= patient_constant.RATE_GENDER_MALE
        elif(self.gender == "Female"):
            self.consutation_time *= patient_constant.RATE_GENDER_FEMALE
            
        if (self.race == "White"):      #- Race attribute
            self.consutation_time *= patient_constant.RATE_RACE_WHITE
        elif (self.race == "Black"):
            self.consutation_time *= patient_constant.RATE_RACE_BLACK
        elif (self.race == "Hispanic):
            self.consutation_time *= patient_constant.RATE_RACE_HISPANIC
        elif (self.race == "Asian"):
            self.consutation_time *= patient_constant.RATE_RACE_ASIAN
        elif (self.race == "Native"):
            self.consutation_time *= patient_constant.RATE_RACE_NATIVE
        else:
            self.consutation_time *= patient_constant.RATE_RACE_OTHER
        
        
        
        self.enter_room_time = environment.now # The time a patient enters the examination room
        self.waiting_time = 0 # The time a patient waits to see a doctor
        self.exit_ER = 0 # The time a patient exits the examination room
        
        
    
