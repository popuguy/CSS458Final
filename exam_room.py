from patient import Patient


class ExamRoom:
    def __init__(self):
        self.patient = None  # None, if no patient occupying
        self.doctor = None #should we have doctor too?
