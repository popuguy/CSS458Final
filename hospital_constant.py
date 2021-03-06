# =======================================================================
#                        General Documentation

"""Single-class module.

   See function docstring for description.
"""

# =======================================================================


# ---------------- Module General Import and Declarations ---------------
from datetime import timedelta


# ---------------------- Class:  HospitalConstant -----------------------
class HospitalConstant:
    """Class for constants pertaining to representation of the entire hospital
    in the simulation.

    """
    EXAM_ROOMS = 8
    NUM_DOCTORS = 10

    # Constant to modify for different simulations
    PATIENTS_PER_HOUR = 10

    # Constants for linear inc/dec style patient entrance
    # Reference data: https://www.beckershospitalreview.com/quality/how-healthy-is-your-emergency-department.html
    DEFAULT_PEAK_PATIENTS = 10
    DEFAULT_MIN_PATIENTS = 1.8

# ===== end file =====
