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
