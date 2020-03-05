from doctor_constant import *
from datetime import timedelta
import datetime


class Doctor:
    def __init__(self):
        self.state = DoctorState.READY
        self.time_entered_exam_room = None

    def enter_exam_room(self, entry_time):
        self.state = DoctorState.IN_PATIENT_EXAM_ROOM
        self.time_entered_exam_room = entry_time
