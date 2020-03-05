import numpy as np
from enum import Enum
import random as rand


class PatientStatus(Enum):
    UNQUEUED = 0
    WAITING = 1
    IN_ROOM = 2
    EXITING = 3


class PatientSex(Enum):
    MALE = 0
    FEMALE = 1


class PatientAge(Enum):
    AGE_UNDER_15 = 0
    AGE_15_24 = 1
    AGE_25_44 = 2
    AGE_45_64 = 3
    AGE_65_74 = 4
    AGE_OVER_74 = 5


class PatientRace(Enum):
    WHITE = 0
    BLACK = 1
    HISPANIC = 2
    ASIAN = 3
    NATIVE = 4
    OTHER = 5


class PatientInsurance(Enum):
    MEDICARE = 0
    MEDICAID = 1
    PRIVATE = 2
    OTHER = 3
    UNINSURED = 4


class PatientConstant:
    """
    Calculating the rate difference from the mean of all visits' time duration
    of difference attributes 
    
    """
    MEAN_ALL_VISITS = 195.7  # - mean duration of

    # - Calculating different rate of visit duration for each attribute
    # - Patient's gender attribute
    RATE_GENDER_MALE = 187.4 / MEAN_ALL_VISITS
    RATE_GENDER_FEMALE = 202.8 / MEAN_ALL_VISITS

    # - Patient's race attribute
    RATE_RACE_WHITE = 190.6 / MEAN_ALL_VISITS
    RATE_RACE_BLACK = 212.0 / MEAN_ALL_VISITS
    RATE_RACE_HISPANIC = 202.4 / MEAN_ALL_VISITS
    RATE_RACE_ASIAN = 203.8 / MEAN_ALL_VISITS
    RATE_RACE_NATIVE = 204.7 / MEAN_ALL_VISITS
    RATE_RACE_OTHER = 193.8 / MEAN_ALL_VISITS

    # - Patient's insurance coverage attribute
    RATE_INSURANCE_MEDICARE = 237.7 / MEAN_ALL_VISITS
    RATE_INSURANCE_MEDICAID = 182.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_PRIVATE = 192.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_OTHER = 169.4 / MEAN_ALL_VISITS
    RATE_INSURANCE_UNINSURED = 191.8 / MEAN_ALL_VISITS

    # ------------------ Portion of patients with attributes -----------------

    # Sex attributes
    SOURCE_DATA_NUM_PATIENTS = 4955590
    SOURCE_DATA_NUM_MALE = 2305226
    SOURCE_DATA_NUM_FEMALE = 2650203
    # Anomaly between num male, num female vs. total patients possibly due to
    # intersex patients
    SOURCE_DATA_PORTION_MALE = SOURCE_DATA_NUM_MALE / SOURCE_DATA_NUM_PATIENTS

    # Age attributes
    SOURCE_DATA_AGE_UNDER_15 = 946742
    SOURCE_DATA_AGE_15_24 = 875470
    SOURCE_DATA_AGE_25_44 = 1545098
    SOURCE_DATA_AGE_45_64 = 1007553
    SOURCE_DATA_AGE_65_74 = 253117
    SOURCE_DATA_AGE_OVER_74 = 327421

    # Race attributes
    SOURCE_DATA_RACE_WHITE = 3335431
    SOURCE_DATA_RACE_BLACK = 354549
    SOURCE_DATA_RACE_HISPANIC = 914958
    SOURCE_DATA_RACE_ASIAN = 73124
    SOURCE_DATA_RACE_NATIVE = 69377
    SOURCE_DATA_RACE_OTHER = 83967

    # Insurance coverage attributes
    SOURCE_DATA_INSURANCE_MEDICARE = 737230
    SOURCE_DATA_INSURANCE_MEDICAID = 1344182
    SOURCE_DATA_INSURANCE_PRIVATE = 1990780
    SOURCE_DATA_INSURANCE_OTHER = 239412
    SOURCE_DATA_INSURANCE_UNINSURED = 532653

    AGE = np.range(10, 50, 1)
    GENDER = ["Male", "Female"]
    RACE = ["White", "Asian", "Black", "Hispanic", "Native", "Other"]
    INSURANCE = ["Medicare", "Medicaid", "Private", "Other", "Uninsured"]
