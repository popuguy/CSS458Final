from hospital_constant import HospitalConstant
from datetime import timedelta


class PatientEntranceStyles:
    def __init__(self):
        self.patients_to_generate = 0.0

    def basic(self, time_delta,
                       patients_per_hour=HospitalConstant.PATIENTS_PER_HOUR):
        """

        :param time_delta: The length of each loop as a datetime.timedelta
        :param patients_per_hour: Optionally user-defined patients to generate
        per unit hour
        :return: Number of new patients the simulation should generate at this
        instant
        """
        mins_elapsed = time_delta.total_seconds() / 60

        patients_per_minute = patients_per_hour / 60.0

        self.patients_to_generate += mins_elapsed * patients_per_minute
        num_new_generate = int(self.patients_to_generate)

        self.patients_to_generate -= int(self.patients_to_generate)

        return num_new_generate

    def peak_and_fall_linear(self, num_loops, time_delta,
                             time_from_start_peak=timedelta(hours=12),
                             peak_num_patients_per_hour=
                             HospitalConstant.DEFAULT_PEAK_PATIENTS,
                             min_num_patients_per_hour=
                             HospitalConstant.DEFAULT_MIN_PATIENTS):
        pass
