from datetime import timedelta


class HospitalConstant:
    EXAM_ROOMS = 5
    NUM_DOCTORS = 5

    # Constant to modify for different simulations
    PATIENTS_PER_HOUR = 10

    # Constants for linear inc/dec style patient entrance
    # Reference data: https://www.beckershospitalreview.com/quality/how-healthy-is-your-emergency-department.html
    DEFAULT_PEAK_PATIENTS = 13
    DEFAULT_MIN_PATIENTS = 1.8
