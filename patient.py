import random
from patient_constant import *


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
        self._give_statistical_attributes()

    def _give_statistical_attributes(self):
        self.age = random.choice(10, 20, 30)

    def queue(self, queue_time):
        self.time_queued = queue_time
