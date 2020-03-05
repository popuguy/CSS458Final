import random
from patient_constant import *
import numpy as np


class Patient:
    def __init__(self):
        """For now, Patient initialization should always be randomized
        according to data-based attributes of hospital patients from
        Karaca et al.

        Source:
        https://bmcemergmed.biomedcentral.com/track/pdf/10.1186/1471-227X-12-15
        """
        self.status = PatientStatus.UNQUEUED
        self.time_queued = None
        self.time_served = None
        self._give_statistical_attributes()

    def _give_statistical_attributes(self):
        # self.age = random.choice(10, 20, 30)
        # Possible information on a statistical way to use the multiple means
        # for different attributes:
        # https://www.researchgate.net/post/Is_there_a_statistical_procedure_for_comparing_multiple_means_to_a_specific_value

        # Weighted attribute selection
        self.sex = np.random.choice(PatientSex.MALE, PatientSex.FEMALE,
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

        self.calculated_mean_hospital_time = self._calc_mean_wait_time()

    def _calc_mean_wait_time(self):
        # TODO: Fix to give a realistic wait time
        return PatientConstant.MEAN_ALL_VISITS

    def queue(self, queue_time):
        self.status = PatientStatus.WAITING
        self.time_queued = queue_time

    def serve(self, service_time):
        self.status = PatientStatus.IN_ROOM
        self.time_served = service_time
