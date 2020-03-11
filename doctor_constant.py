from enum import Enum


class DoctorState(Enum):
    """Possibly invalid source for current data:
    https://www.ncbi.nlm.nih.gov/pubmed/23340186

    RESULTS:
    "Results showed that physicians spent 25% of their time in direct
    patient contact, 5.8% with indirect patient care, 24% communicating
    with other staff, 31% documenting their work and 6% on transport.
    Personal time ac-counted for 5% and other activities for 3%."
    """
    READY = 0
    IN_PATIENT_EXAM_ROOM = 1
    DOING_INDIRECT_PATIENT_CARE = 2
    COMMUNICATING_WITH_STAFF = 3
    DOCUMENTING_WORK = 4
    MOVING = 5
    PERSONAL_TIME = 6
    OTHER = 7


class DoctorConstant:
    # Source:
    # https://www.statista.com/statistics/250219/us-physicians-opinion-about-their-compensation/
    AVG_TIME_SPENT_WITH_PATIENT = 20  # Minutes
    PORTION_TIME_SPENT_WITH_PATIENT = 0.25
