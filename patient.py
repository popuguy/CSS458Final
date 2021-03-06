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

    def __init__(self, setAttributes=True):
        """For now, Patient initialization should always be randomized
        according to data-based attributes of hospital patients from
        Karaca et al.

        Source:
        https://bmcemergmed.biomedcentral.com/track/pdf/10.1186/1471-227X-12-15
        :param setAttributes: If True, attributes will be used for calculating
        projected time in exam room
        """
        self.calcAttributes = setAttributes  # True if patient is set to have attributes

        # Coronavirus or some other infectious disease
        self.infected = False
        self.infectious = False

        # self.calculated_mean_hospital_time = PatientConstant.MEAN_ALL_VISITS
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
        """Assigns patient attributes based on demographic selected in
        configuration.
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

        # Calculated mean hospital time is an estimate of treatment time for algorithms
        self.calculated_mean_hospital_time = self._calc_treatment_time()
        # print(self.calculated_mean_hospital_time, "calcd mean hosp time for patient")

        # Generated hospital time is the simulation-generated actual time the
        # patient will take to finish treatment in an exam room as long as a
        # doctor has visited during the time period.
        self.generated_hospital_time = self._generate_actual_treatment_time()

        # This is the level of urgency which will affect the treatment and wait time.
        # Source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm
        self.levelOfUrgency = np.random.choice(np.arange(1, 6))

        if random.random() < PatientConstant.PORTION_INFECTED:
            # print("Infected patient generated!")
            self.infected = True
            self.infectious = True

    def _generate_actual_treatment_time(self):
        """With a small degree of randomness, this method generates a real
        min amount of time they will need to spend in an exam room. Actual time
        spent in the exam room is based on whether the patient is seen by a
        doctor in a timely fashion.

        :return: Generated actual treatment time
        """
        # From the source, this is close-ish to +-1% for each attribute

        plus_or_minus_mean = random.uniform(
            1 - PatientConstant.PLUS_OR_MINUS_PORTION,
            1 + PatientConstant.PLUS_OR_MINUS_PORTION)

        self.generated_hospital_time = PatientConstant.MEAN_ALL_VISITS * \
                                       plus_or_minus_mean

        plus_or_minus_sex = random.uniform(
            1 - PatientConstant.PLUS_OR_MINUS_PORTION,
            1 + PatientConstant.PLUS_OR_MINUS_PORTION)
        # Calculate the treatment according to patient's attribute
        if self.sex is PatientSex.MALE:
            self.generated_hospital_time *= \
                PatientConstant.RATE_GENDER_MALE * plus_or_minus_sex
        else:
            self.generated_hospital_time *= \
                PatientConstant.RATE_GENDER_FEMALE * plus_or_minus_sex
        plus_or_minus_race = random.uniform(
            1 - PatientConstant.PLUS_OR_MINUS_PORTION,
            1 + PatientConstant.PLUS_OR_MINUS_PORTION)
        self.generated_hospital_time *= \
            PatientConstant.RATE_RACE_DICT[self.race] * plus_or_minus_race
        plus_or_minus_insurance = random.uniform(
            1 - PatientConstant.PLUS_OR_MINUS_PORTION,
            1 + PatientConstant.PLUS_OR_MINUS_PORTION)
        self.generated_hospital_time *= \
            PatientConstant.RATE_INSURANCE_DICT[self.insurance] * \
            plus_or_minus_insurance

        return self.generated_hospital_time

    def _calc_treatment_time(self):
        """This is a method to calculate the treatment time of a patient.
        Treatment time is defined as the difference between the time 
        the patient had initial contact with a doctor and the time the patient 
        was discharged from the emergency room
        Please refer to source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm
        
        Patient's treatment time is generated using the source at the top and
        differs according to their age, gender,race, and type of insurance
        attributes.

        """
        # I make an assumption here that when the patient is served or enter
        # the exam room, this means they have contact with doctor.
        # self.treatment_time = self.time_exited - self.time_served
        self.treatment_time = random.uniform(PatientConstant.LOW_MEAN_ALL_VISITS, \
                                             PatientConstant.HIGH_MEAN_ALL_VISITS)

#        print("before: ", self.treatment_time)
        if self.calcAttributes == True:

            # Calculate the treatment according to patient's attribute
            if self.sex is PatientSex.MALE:
                self.treatment_time *= PatientConstant.RATE_GENDER_MALE
            else:
                self.treatment_time *= PatientConstant.RATE_GENDER_FEMALE
            self.treatment_time *= PatientConstant.RATE_RACE_DICT[self.race]
            self.treatment_time *= \
                PatientConstant.RATE_INSURANCE_DICT[self.insurance]


#        print("after: ", self.treatment_time)
#        print()

        return self.treatment_time

    def _calc_wait_time(self):
        """This is a method to calculate the wait time of a patient. Wait time
        is defined as the difference between the time of arrival in the ED and
        the time the patient had initial contact with a physician, physician
        assistant, or nurse practitioner.

        Please refer to the source: https://www.cdc.gov/mmwr/preview/mmwrhtml/mm6319a8.htm
        """
        # TODO: Fix to give a realistic wait time
        # I make an assumption here that the time when a patient is in the
        # queue is the time when they arrive at ER.
        self.wait_time = self.time_served - self.time_queued
        return self.wait_time
        # return PatientConstant.MEAN_ALL_VISITS

    def try_contract_infection(self, time_delta, num_infected_near):
        """To be called only once per time_delta, method uses probability of
        infection to determine if patient has become infected by nearby
        infected patients during the last time_delta

        :param time_delta: Amount of time passed near num_infected_near
        :param num_infected_near: Number of infectious patients nearby
        :return: True if patient contracts the infection
        """
        chance_to_contract = \
            PatientConstant.DISEASE_INFECTION_CHANCE_PER_MINUTE * \
            self._time_delta_to_minutes(time_delta) * num_infected_near
        if random.random() < chance_to_contract:
            self.infected = True
            return True
        return False

    def _time_delta_to_minutes(self, time_delta):
        """Accurate to one second, time delta in minutes returned.
        :param time_delta A datetime.timedelta object
        :returns A float of minutes in the time delta
        """
        return (time_delta.days * 24 * 60) + (time_delta.seconds / 60)

    def queue(self, queue_time):
        """Enqueue a patient
        :param queue_time: When the queueing occurs
        """
        self.status = PatientStatus.WAITING
        self.time_queued = queue_time

    def serve(self, service_time):
        """Serve a patient by moving them into the exam room
        :param service_time: When the patient is moved to exam room
        """
        self.status = PatientStatus.IN_ROOM
        self.time_served = service_time

    def exit(self, cur_time):
        """Remove a patient from the exam room and get their departure time
        :param cur_time: Time at which patient departs
        """
        self.time_exited = cur_time
        self.status = PatientStatus.EXITING

        # print("Patient exiting. Examination took", self.time_exited -
        # self.time_served)
#        print("Patient exiting. Examination took", self.time_exited -
    #        self.time_served)

    def has_completed_visit(self, cur_time):
        """Get the total time during a patient's visit by adding waiting time
        and consultation time
        :param cur_time: Time to check for completion.
        :return: True if patient has been seen and has been in the exam room
        for the generated period of time.
        """
        return (cur_time >= self.time_served +
                timedelta(minutes=self.generated_hospital_time)) and \
               self.seen_by_doctor
