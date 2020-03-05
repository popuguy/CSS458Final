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
        # for different attributes: https://www.researchgate.net/post/Is_there_a_statistical_procedure_for_comparing_multiple_means_to_a_specific_value
        # Weighted sex selection
        self.sex = np.random.choice(PatientSex.MALE, PatientSex.FEMALE,
                                    p=[PatientConstant.SOURCE_DATA_PORTION_MALE,
                                       1 - PatientConstant.SOURCE_DATA_PORTION_MALE])
        self.age = np.random.choice(PatientAge.)
        self.race
        self.insurance

    def queue(self, queue_time):
        self.status = PatientStatus.WAITING
        self.time_queued = queue_time

    def serve(self, service_time):
        self.status = PatientStatus.IN_ROOM
        self.time_served = service_time
