import random

from doctor_constant import *
from datetime import timedelta
import datetime


def time_delta_to_minutes(time_delta):
    """Accurate to one second time delta in minutes returned.
    :param time_delta A datetime.timedelta object
    :returns A float of minutes in the time delta
    """
    return (time_delta.days * 24 * 60) + (time_delta.seconds / 60)


class Doctor:
    """Doctor class defines a single doctor that changes states to
    'move' around the hospital/medical environment

    """
    next_id = 0

    # Constructor
    def __init__(self):
        self.state = DoctorState.READY
        self.time_entered_exam_room = None
        self.id = Doctor.next_id
        Doctor.next_id += 1

    def enter_exam_room(self, entry_time):
        """Appropriately modifies doctor for entry to exam room

        :param entry_time: When entry takes place
        """
        self.state = DoctorState.IN_PATIENT_EXAM_ROOM
        self.time_entered_exam_room = entry_time

    def exit_exam_room(self):
        """Appropriately modifies doctor for exit of exam room

        """
        self.state = DoctorState.OTHER
        self.time_entered_exam_room = None

    def update_activity(self, time_delta):
        """Will be called in simulation to transition between a state of
        readiness to see patients in exam rooms and working on other activities
        at a rate defined in DoctorConstant.
        :param time_delta: The amount of time since last update_activity was
        called.
        """
        if self.state == DoctorState.IN_PATIENT_EXAM_ROOM:
            return
        # We have the amount of time a doctor stays in patient room as
        # DoctorConstant.PORTION_TIME_SPENT_WITH_PATIENT
        # We have the length of time a doctor stays in patient room as
        # DoctorConstant.AVG_TIME_SPENT_WITH_PATIENT
        # Thus, for average time spent doing OTHER we use PORTION * all time
        # = TIME_SPENT_WITH_PATIENT
        total_time_unit = DoctorConstant.AVG_TIME_SPENT_WITH_PATIENT / \
                          DoctorConstant.PORTION_TIME_SPENT_WITH_PATIENT
        time_spent_doing_other = total_time_unit - \
                                 DoctorConstant.AVG_TIME_SPENT_WITH_PATIENT
        chance_change_task = time_delta_to_minutes(time_delta) / \
                             time_spent_doing_other
        if self.state == DoctorState.OTHER and random.random() < \
                chance_change_task:
            self.state = DoctorState.READY

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
