from datetime import timedelta


class HospitalConstant:
    EXAM_ROOMS = 5
    DOCTORS = 5

    # Amount of time between when a patient is about to be seen and is
    # actually seen
    TIME_TRANSITION_SEEING_PATIENT = timedelta(minutes=0)
