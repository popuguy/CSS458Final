# Import statements
import numpy as np
from enum import Enum
import random as rand

"""This class represents the current status of a patient.
"""
class PatientStatus(Enum):
    UNQUEUED = 0
    WAITING = 1
    IN_ROOM = 2
    EXITING = 3

"""This class represents a patient's gender.
"""
class PatientSex(Enum):
    MALE = 0
    FEMALE = 1

"""This class represents the age of a patient. Each age range is specified with a number.
"""
class PatientAge(Enum):
    AGE_UNDER_15 = 0
    AGE_15_24 = 1
    AGE_25_44 = 2
    AGE_45_64 = 3
    AGE_65_74 = 4
    AGE_OVER_74 = 5

"""This class represents a patient's race. Each race is specified with a number.
"""
class PatientRace(Enum):
    WHITE = 0
    BLACK = 1
    HISPANIC = 2
    ASIAN = 3
    NATIVE = 4
    OTHER = 5

"""This class represents the insurance status/information of a patient. Each of them is specified with a number.
"""
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
    RATE_GENDER = [RATE_GENDER_MALE, RATE_GENDER_FEMALE]

    # - Patient's race attribute
    RATE_RACE_WHITE = 190.6 / MEAN_ALL_VISITS
    RATE_RACE_BLACK = 212.0 / MEAN_ALL_VISITS
    RATE_RACE_HISPANIC = 202.4 / MEAN_ALL_VISITS
    RATE_RACE_ASIAN = 203.8 / MEAN_ALL_VISITS
    RATE_RACE_NATIVE = 204.7 / MEAN_ALL_VISITS
    RATE_RACE_OTHER = 193.8 / MEAN_ALL_VISITS
    RATE_RACE = [RATE_RACE_WHITE, RATE_RACE_BLACK, RATE_RACE_HISPANIC, \
                 RATE_RACE_ASIAN, RATE_RACE_NATIVE, RATE_RACE_OTHER]

    # - Patient's insurance coverage attribute
    RATE_INSURANCE_MEDICARE = 237.7 / MEAN_ALL_VISITS
    RATE_INSURANCE_MEDICAID = 182.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_PRIVATE = 192.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_OTHER = 169.4 / MEAN_ALL_VISITS
    RATE_INSURANCE_UNINSURED = 191.8 / MEAN_ALL_VISITS
    RATE_INSURACE = [RATE_INSURACE_MEDICARE, RATE_INSURANCE_MEDICAID, \
                     RATE_INSURANCE_PRIVATE, RATE_INSURANCE_OTHER, \
                     RATE_INSURANCE_UNINSURED]
    
    # - Patient's age attribute
    RATE_AGE_UNDER_15 = 142.2 / MEAN_ALL_VISITS
    RATE_AGE_15_24 = 183.9 / MEAN_ALL_VISITS
    RATE_AGE_25_44 = 203.1 / MEAN_ALL_VISITS
    RATE_AGE_45_64 = 223.7 / MEAN_ALL_VISITS
    RATE_AGE_65_74 = 227.3 / MEAN_ALL_VISITS
    RATE_AGE_OVER_74 = 237.5 / MEAN_ALL_VISITS
    RATE_AGE = [RATE_AGE_UNDER_15, RATE_AGE_15_24, RATE_AGE_25_44, \
                RATE_AGE_45_64, RATE_AGE_65_74, RATE_AGE_OVER_74]

    # ------------------ Portion of patients with attributes -----------------

    SOURCE_DATA_NUM_PATIENTS = 4955590  # People in study

    # Sex attributes (# of people out of total)
    SOURCE_DATA_NUM_MALE = 2305226
    SOURCE_DATA_NUM_FEMALE = 2650203
    # Anomaly between num male, num female vs. total patients possibly due to
    # intersex patients
    SOURCE_DATA_PORTION_MALE = SOURCE_DATA_NUM_MALE / SOURCE_DATA_NUM_PATIENTS

    # Age attributes (# of people out of total)
    SOURCE_DATA_AGE_UNDER_15 = 946742
    SOURCE_DATA_AGE_15_24 = 875470
    SOURCE_DATA_AGE_25_44 = 1545098
    SOURCE_DATA_AGE_45_64 = 1007553
    SOURCE_DATA_AGE_65_74 = 253117
    SOURCE_DATA_AGE_OVER_74 = 327421

    SOURCE_DATA_TOTAL_AGE = SOURCE_DATA_AGE_UNDER_15 + SOURCE_DATA_AGE_15_24 +\
                            SOURCE_DATA_AGE_25_44 + SOURCE_DATA_AGE_45_64 +\
                            SOURCE_DATA_AGE_65_74 + SOURCE_DATA_AGE_OVER_74

    SOURCE_DATA_PORTION_AGE_UNDER_15 = SOURCE_DATA_AGE_UNDER_15 / \
                                       SOURCE_DATA_TOTAL_AGE
    SOURCE_DATA_PORTION_AGE_15_24 = SOURCE_DATA_AGE_15_24 / \
                                    SOURCE_DATA_TOTAL_AGE
    SOURCE_DATA_PORTION_AGE_25_44 = SOURCE_DATA_AGE_25_44 / \
                                    SOURCE_DATA_TOTAL_AGE
    SOURCE_DATA_PORTION_AGE_45_64 = SOURCE_DATA_AGE_45_64 / \
                                    SOURCE_DATA_TOTAL_AGE
    SOURCE_DATA_PORTION_AGE_65_74 = SOURCE_DATA_AGE_65_74 / \
                                    SOURCE_DATA_TOTAL_AGE
    SOURCE_DATA_PORTION_AGE_OVER_74 = SOURCE_DATA_AGE_OVER_74 / \
                                      SOURCE_DATA_TOTAL_AGE

    # Race attributes (# of people out of total)

    SOURCE_DATA_RACE_WHITE = 3335431
    SOURCE_DATA_RACE_BLACK = 354549
    SOURCE_DATA_RACE_HISPANIC = 914958
    SOURCE_DATA_RACE_ASIAN = 73124
    SOURCE_DATA_RACE_NATIVE = 69377
    SOURCE_DATA_RACE_OTHER = 83967

    SOURCE_DATA_TOTAL_RACE = SOURCE_DATA_RACE_WHITE + \
                             SOURCE_DATA_RACE_BLACK + \
                             SOURCE_DATA_RACE_HISPANIC + \
                             SOURCE_DATA_RACE_ASIAN + \
                             SOURCE_DATA_RACE_NATIVE + \
                             SOURCE_DATA_RACE_OTHER

    SOURCE_DATA_PORTION_RACE_WHITE = SOURCE_DATA_RACE_WHITE / \
                                     SOURCE_DATA_TOTAL_RACE
    SOURCE_DATA_PORTION_RACE_BLACK = SOURCE_DATA_RACE_BLACK / \
                                     SOURCE_DATA_TOTAL_RACE
    SOURCE_DATA_PORTION_RACE_HISPANIC = SOURCE_DATA_RACE_HISPANIC / \
                                        SOURCE_DATA_TOTAL_RACE
    SOURCE_DATA_PORTION_RACE_ASIAN = SOURCE_DATA_RACE_ASIAN / \
                                     SOURCE_DATA_TOTAL_RACE
    SOURCE_DATA_PORTION_RACE_NATIVE = SOURCE_DATA_RACE_NATIVE / \
                                      SOURCE_DATA_TOTAL_RACE
    SOURCE_DATA_PORTION_RACE_OTHER = SOURCE_DATA_RACE_OTHER / \
                                     SOURCE_DATA_TOTAL_RACE

    # Insurance coverage attributes (# of people out of total)
    SOURCE_DATA_INSURANCE_MEDICARE = 737230
    SOURCE_DATA_INSURANCE_MEDICAID = 1344182
    SOURCE_DATA_INSURANCE_PRIVATE = 1990780
    SOURCE_DATA_INSURANCE_OTHER = 239412
    SOURCE_DATA_INSURANCE_UNINSURED = 532653

    SOURCE_DATA_TOTAL_INSURANCE = SOURCE_DATA_INSURANCE_MEDICARE + \
                                 SOURCE_DATA_INSURANCE_MEDICAID + \
                                 SOURCE_DATA_INSURANCE_PRIVATE + \
                                 SOURCE_DATA_INSURANCE_OTHER + \
                                 SOURCE_DATA_INSURANCE_UNINSURED

    SOURCE_DATA_PORTION_INSURANCE_MEDICARE = \
        SOURCE_DATA_INSURANCE_MEDICARE / SOURCE_DATA_TOTAL_INSURANCE
    SOURCE_DATA_PORTION_INSURANCE_MEDICAID = \
        SOURCE_DATA_INSURANCE_MEDICAID / SOURCE_DATA_TOTAL_INSURANCE
    SOURCE_DATA_PORTION_INSURANCE_PRIVATE = \
        SOURCE_DATA_INSURANCE_PRIVATE / SOURCE_DATA_TOTAL_INSURANCE
    SOURCE_DATA_PORTION_INSURANCE_OTHER = \
        SOURCE_DATA_INSURANCE_OTHER / SOURCE_DATA_TOTAL_INSURANCE
    SOURCE_DATA_PORTION_INSURANCE_UNINSURED = \
        SOURCE_DATA_INSURANCE_UNINSURED / SOURCE_DATA_TOTAL_INSURANCE
