from patient import Patient


class ExamRoom:
    """Representation of an examination room only occupied by doctors and
    patients. This is where treatment and release takes place.

    """
    def __init__(self):
        self.patient = None  # None, if no patient occupying
        self.doctor = None

    def reset(self):
        self.patient = None
        self.doctor = None

    def make_doctor_exit(self):
        self.doctor.exit_exam_room()
        self.doctor = None
    # def can_vacate(self):

