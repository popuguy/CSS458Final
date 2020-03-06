from doctor_constant import *
from datetime import timedelta
import datetime


class Doctor:
    next_id = 0
    
    def __init__(self):
        self.state = DoctorState.READY
        self.time_entered_exam_room = None
        self.id = Doctor.next_id
        Doctor.next_id += 1

    def enter_exam_room(self, entry_time):
        self.state = DoctorState.IN_PATIENT_EXAM_ROOM
        self.time_entered_exam_room = entry_time

    def exit_exam_room(self):
        self.state = DoctorState.READY
        self.time_entered_exam_room = None

    def has_completed_patient_visit(self, cur_time):
        """Check if exam room visit complete.

        :param cur_time: Current simulation time
        :returns True if visit completed, else False
        """
        if self.time_entered_exam_room is None:
            # Edge case. Possibly never hit
            return True
        if cur_time >= self.time_entered_exam_room + \
                timedelta(minutes=DoctorConstant.AVG_TIME_SPENT_WITH_PATIENT):
            return True
        return False
