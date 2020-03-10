# Import statements
import random
from patient_constant import *
import numpy as np
from datetime import timedelta


class Patient:
    """This class represents a patient with these attributes: sex, age, race,
    and insurance status. A patient will also have a variable called status to
    keep track of where they are in the queue.
    """
    last_id = 0

    def __init__(self):
        """For now, Patient initialization should always be randomized
        according to data-based attributes of hospital patients from
        Karaca et al.

        Source:
        https://bmcemergmed.biomedcentral.com/track/pdf/10.1186/1471-227X-12-15
        """
        self.status = PatientStatus.UNQUEUED  # keep track of where a patient is in a queue
        self.time_queued = None  # the time when a patient is in the queue
        self.time_served = None  # the time when a patient is served, or enter the exam room
        self.time_exited = None  # the time when a patient is done with the examination, and leave the ER
        # Once a patient has actually been seen by a doctor this changes to
        # True. It is a condition for exiting
        self.seen_by_doctor = False
        self._give_statistical_attributes()  # generate random attributes to a patient

        Patient.last_id += 1
        self.id = Patient.last_id

    def _give_statistical_attributes(self):
        """Assign random value to a patient's attributes
        """
        # Possible information on a statistical way to use the multiple means
        # for different attributes:
        # https://www.researchgate.net/post/Is_there_a_statistical_procedure_for_comparing_multiple_means_to_a_specific_value

        # Weighted attribute selection
        self.sex = np.random.choice([PatientSex.MALE, PatientSex.FEMALE],
                                    p=[PatientConstant.SOURCE_DATA_PORTION_MALE,
                                       1 - PatientConstant.SOURCE_DATA_PORTION_MALE])

        self.age = np.random.choice([PatientAge.AGE_UNDER_15,
                                     PatientAge.AGE_15_24,
                                     PatientAge.AGE_25_44,
                                     PatientAge.AGE_45_64,
                                     PatientAge.AGE_65_74,
                                     PatientAge.AGE_OVER_74],
                                    p=[PatientConstant.SOURCE_DATA_PORTION_AGE_UNDER_15,
                                       PatientConstant.SOURCE_DATA_PORTION_AGE_15_24,
                                       PatientConstant.SOURCE_DATA_PORTION_AGE_25_44,
                                       PatientConstant.SOURCE_DATA_PORTION_AGE_45_64,
                                       PatientConstant.SOURCE_DATA_PORTION_AGE_65_74,
                                       PatientConstant.SOURCE_DATA_PORTION_AGE_OVER_74])

        self.race = np.random.choice([PatientRace.WHITE,
                                      PatientRace.BLACK,
                                      PatientRace.HISPANIC,
                                      PatientRace.ASIAN,
                                      PatientRace.NATIVE,
                                      PatientRace.OTHER],
                                     p=[PatientConstant.SOURCE_DATA_PORTION_RACE_WHITE,
                                        PatientConstant.SOURCE_DATA_PORTION_RACE_BLACK,
                                        PatientConstant.SOURCE_DATA_PORTION_RACE_HISPANIC,
                                        PatientConstant.SOURCE_DATA_PORTION_RACE_ASIAN,
                                        PatientConstant.SOURCE_DATA_PORTION_RACE_NATIVE,
                                        PatientConstant.SOURCE_DATA_PORTION_RACE_OTHER])

        self.insurance = np.random.choice([PatientInsurance.MEDICARE,
                                           PatientInsurance.MEDICAID,
                                           PatientInsurance.PRIVATE,
                                           PatientInsurance.OTHER,
                                           PatientInsurance.UNINSURED],
                                          p=[PatientConstant.SOURCE_DATA_PORTION_INSURANCE_MEDICARE,
                                             PatientConstant.SOURCE_DATA_PORTION_INSURANCE_MEDICAID,
                                             PatientConstant.SOURCE_DATA_PORTION_INSURANCE_PRIVATE,
                                             PatientConstant.SOURCE_DATA_PORTION_INSURANCE_OTHER,
                                             PatientConstant.SOURCE_DATA_PORTION_INSURANCE_UNINSURED])
        
        
        # find the mean of the waiting time
        # self.calculated_mean_hospital_time = self._calc_mean_wait_time()
        # self.actual_hospital_time_min = something...
        
        # This is the level of urgency which will affect the treatment and wait time.
        # Source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm
        self.levelOfUrgency = np.random.choice(np.range(1, 6))
        
    """This is a method to calculate the treament time of a patient. Treatment time is defined as the difference 
    between the time the patient had initial contact with a physician, physician assistant, or nurse practitioner 
    and the time the patient was discharged from the ED to another hospital unit or to the patient's residence.
    Please refer to the source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm"""
    def _calc_treatment_time(self):
        # I make an assumption here that when the patient is served or enter the exam room, this means they have
        # contact with doctor.
        self.treatment_time = self.time_exited - self.time_served 
        return self.treatment_time

    """This is a method to calculate the wait time of a patient. Wait time is defined as the difference 
        between the time of arrival in the ED and the time the patient had initial contact with a physician, physician 
        assistant, or nurse practitioner.
        Please refer to the source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm
    """
    def _calc_wait_time(self):
        # TODO: Fix to give a realistic wait time
        # I make an assumption here that the time when a patient is in the queue is the time when they arrive at ER.
        self.wait_time = self.time_served - self.time_queued
        return self.wait_time
        #return PatientConstant.MEAN_ALL_VISITS

    def queue(self, queue_time):
        """Enqueue a patient
        """
        self.status = PatientStatus.WAITING
        self.time_queued = queue_time

    def serve(self, service_time):
        """Serve a patient by moving them into the exam room
        """
        self.status = PatientStatus.IN_ROOM
        self.time_served = service_time

    def exit(self, cur_time):
        """Remove a patient from the exam room and get their departure time
        """
        self.time_exited = cur_time
        self.status = PatientStatus.EXITING

    def has_completed_visit(self, cur_time):
        """Get the total time during a patient's visit by adding waiting time and consultation time
        """
        return (cur_time <= self.time_served +
                timedelta(
                    minutes=self.calculated_mean_hospital_time)) and \
               self.seen_by_doctor
    

