# ======================================================================
#                        General Documentation
"""Multiple-classes module.

   See classes docstring for description.
"""

#=======================================================================


# ---------------- Module General Import and Declarations --------------
import numpy as np
from enum import Enum
import random as rand

#------------------------- Class:  PatientStatus -----------------------
"""This class represents the current status of a patient.
"""
class PatientStatus(Enum):
    UNQUEUED = 0
    WAITING = 1
    IN_ROOM = 2
    EXITING = 3

#------------------------- Class:  PatientSex --------------------------
"""This class represents a patient's gender.
"""
class PatientSex(Enum):
    MALE = 0
    FEMALE = 1

#------------------------- Class:  PatientAge --------------------------
"""This class represents the age of a patient. Each age range is specified with a number.
"""
class PatientAge(Enum):
    AGE_UNDER_15 = 0
    AGE_15_24 = 1
    AGE_25_44 = 2
    AGE_45_64 = 3
    AGE_65_74 = 4
    AGE_OVER_74 = 5

#------------------------- Class:  PatientRace --------------------------
"""This class represents a patient's race. Each race is specified with a number.
"""
class PatientRace(Enum):
    WHITE = 0
    BLACK = 1
    HISPANIC = 2
    ASIAN = 3
    NATIVE = 4
    OTHER = 5

#------------------------- Class:  PatientInsurance --------------------------
"""This class represents the insurance status/information of a patient. Each of them is specified with a number.
"""
class PatientInsurance(Enum):
    MEDICARE = 0
    MEDICAID = 1
    PRIVATE = 2
    OTHER = 3
    UNINSURED = 4

#------------------------- Class:  PatientConstant --------------------------
class PatientConstant:
    """
    Calculating the rate difference from the mean of all visits' time duration
    of difference attributes 
    """
    PLUS_OR_MINUS_PORTION = 0.01
    PORTION_INFECTED = 0.1
    # Slight source:
    # https://www.fredhutch.org/en/news/center-news/2015/12/separating-fact-from-fiction-about-colds-and-flu.html
    #
    # Mostly just guessed numbers about transmission probability
    # From a story, 10 hours in close proximity to a person sick with a cold was enough to infect
    # Assume that is a base and the disease in question has some multiplier of infectiousness related to that base
    #
    # Another source:
    # https://arstechnica.com/science/2020/03/dont-panic-the-comprehensive-ars-technica-guide-to-the-coronavirus/2/#h3
    # 2-2.5 R0 number for COVID-19 as opposed to 1.3 for seasonal flu
    INFECTIOUSNESS_MULTIPLIER = 2.25 / 1.3
    BASE_INFECTIOUSNESS = 300  # Minutes for 50% chance at 1.3 R0
    DISEASE_INFECTION_CHANCE_PER_MINUTE = 0.5 / (BASE_INFECTIOUSNESS *
                                                 (1 / INFECTIOUSNESS_MULTIPLIER))
    
    #Source:
    #https://bmcemergmed.biomedcentral.com/track/pdf/10.1186/1471-227X-12-15
    MEAN_ALL_VISITS = 195.7  # - mean duration of all visits' treatment time
    LOW_MEAN_ALL_VISITS = 194.2
    HIGH_MEAN_ALL_VISITS = 197.2

    # - Calculating different rate of visit duration for each attribute
    # - Patient's gender attribute
    RATE_GENDER_MALE = 187.4 / MEAN_ALL_VISITS
    RATE_GENDER_FEMALE = 202.8 / MEAN_ALL_VISITS
    # RATE_GENDER = [RATE_GENDER_MALE, RATE_GENDER_FEMALE]

    # - Patient's race attribute
    RATE_RACE_WHITE = 190.6 / MEAN_ALL_VISITS
    RATE_RACE_BLACK = 212.0 / MEAN_ALL_VISITS
    RATE_RACE_HISPANIC = 202.4 / MEAN_ALL_VISITS
    RATE_RACE_ASIAN = 203.8 / MEAN_ALL_VISITS
    RATE_RACE_NATIVE = 204.7 / MEAN_ALL_VISITS
    RATE_RACE_OTHER = 193.8 / MEAN_ALL_VISITS
    # RATE_RACE = [RATE_RACE_WHITE, RATE_RACE_BLACK, RATE_RACE_HISPANIC, \
    #              RATE_RACE_ASIAN, RATE_RACE_NATIVE, RATE_RACE_OTHER]
    RATE_RACE_DICT = {PatientRace.WHITE: RATE_RACE_WHITE, PatientRace.BLACK: RATE_RACE_BLACK,
                      PatientRace.HISPANIC: RATE_RACE_HISPANIC, PatientRace.ASIAN: RATE_RACE_ASIAN,
                      PatientRace.NATIVE: RATE_RACE_NATIVE, PatientRace.OTHER: RATE_RACE_OTHER}

    # - Patient's insurance coverage attribute
    RATE_INSURANCE_MEDICARE = 237.7 / MEAN_ALL_VISITS
    RATE_INSURANCE_MEDICAID = 182.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_PRIVATE = 192.8 / MEAN_ALL_VISITS
    RATE_INSURANCE_OTHER = 169.4 / MEAN_ALL_VISITS
    RATE_INSURANCE_UNINSURED = 191.8 / MEAN_ALL_VISITS
    # RATE_INSURANCE = [RATE_INSURANCE_MEDICARE, RATE_INSURANCE_MEDICAID,
    #                  RATE_INSURANCE_PRIVATE, RATE_INSURANCE_OTHER,
    #                  RATE_INSURANCE_UNINSURED]
    RATE_INSURANCE_DICT = {PatientInsurance.MEDICARE: RATE_INSURANCE_MEDICARE,
                           PatientInsurance.MEDICAID: RATE_INSURANCE_MEDICAID,
                           PatientInsurance.PRIVATE: RATE_INSURANCE_PRIVATE,
                           PatientInsurance.OTHER: RATE_INSURANCE_OTHER,
                           PatientInsurance.UNINSURED: RATE_INSURANCE_UNINSURED}

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

    SOURCE_DATA_TOTAL_AGE = SOURCE_DATA_AGE_UNDER_15 + SOURCE_DATA_AGE_15_24 + \
                            SOURCE_DATA_AGE_25_44 + SOURCE_DATA_AGE_45_64 + \
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
