from patient import Patient


class ExamRoom:
    def __init__(self):
        self.patient = None  # None, if no patient occupying
        # No doctor object or status necessary for an exam room. Presumed that
        # a patient will not enter an exam room alone, so one occupied exam
        # room always contains a doctor
