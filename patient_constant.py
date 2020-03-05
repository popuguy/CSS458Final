import numpy as np
from enum import Enum
import random as rand


class PatientStatus(Enum):
    UNQUEUED = 0
    WAITING = 1
    IN_ROOM = 2
    EXITING = 3


class PatientConstant:
    """
    Calculating the rate difference from the mean of all visits' time duration
    of difference attributes 
    
    """
    MEAN_ALL_VISITS = 195.7     #- mean duration of 
    
    #- Calculating different rate of visit duration for each attribute
    #- Patient's gender attribute
    RATE_GENDER_MALE = 187.4 / MEAN_ALL_VISITS
    RATE_GENDER_FEMALE = 202.8 / MEAN_ALL_VISITS
    
    #- Patient's race attribute
    RATE_RACE_WHITE = 190.6 / MEAN_ALL_VISITS
    RATE_RACE_BLACK = 212.0 / MEAN_ALL_VISITS
    RATE_RACE_HISPANIC = 202.4 / MEAN_ALL_VISITS
    RATE_RACE_ASIAN = 203.8 / MEAN_ALL_VISITS
    RATE_RACE_NATIVE = 204.7 / MEAN_ALL_VISITS
    RATE_RACE_OTHER = 193.8 / MEAN_ALL_VISITS
    
    #- Patient's insurance coverage attribute
    RATE_INSURANCE_MEDICARE = 237.7 / MEAN_ALL_VISITS
    RATE_INSURANCE_MEDICAID = 182.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_PRIVATE = 192.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_OTHER = 169.4 / MEAN_ALL_VISITS
    RATE_INSURANCE_UNINSURED = 191.8 / MEAN_ALL_VISITS
    
    
    AGE = np.range(10, 50, 1)
    GENDER = ["Male", "Female"]
    RACE = ["White", "Asian", "Black", "Hispanic", "Native", "Other"]
    INSURANCE = ["Medicare", "Medicaid", "Private", "Other", "Uninsured"]
    
