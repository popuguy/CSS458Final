from hospital_constant import HospitalConstant
from datetime import timedelta


class PatientEntranceStyles:
    def __init__(self):
        self.patients_to_generate = 0.0

    def _time_delta_to_minutes(self, time_delta):
        """Accurate to one second time delta in minutes returned.
        :param time_delta A datetime.timedelta object
        :returns A float of minutes in the time delta
        """
        return (time_delta.days * 24 * 60) + (time_delta.seconds / 60)

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

    def rise_and_fall_linear(self, num_loops, time_delta,
                             time_from_start_peak=timedelta(hours=12),
                             peak_num_patients_per_hour=
                             HospitalConstant.DEFAULT_PEAK_PATIENTS,
                             min_num_patients_per_hour=
                             HospitalConstant.DEFAULT_MIN_PATIENTS):
        """Linear rise and fall patient entrance style

        :param num_loops: Number of loops executed in simulation so far
        :param time_delta: Time delta for each loop as datetime.timedelta
        :param time_from_start_peak: datetime.timedelta of how long from start
        to have the peak patients per hour generating
        :param peak_num_patients_per_hour: Most patients per hour
        :param min_num_patients_per_hour: Fewest patients per hour
        """
        time_delta_mins = self._time_delta_to_minutes(time_delta)
        time_from_start_peak_mins = self._time_delta_to_minutes(time_from_start_peak)
        num_loops_at_peak = time_from_start_peak_mins / time_delta_mins
        general_pph_slope = (peak_num_patients_per_hour - min_num_patients_per_hour) / num_loops_at_peak
        if num_loops < num_loops_at_peak:
            cur_num_patients_per_hour = min_num_patients_per_hour + (general_pph_slope * num_loops)
            print (cur_num_patients_per_hour, "cur_num_patients_per_hour")
            cur_num_patients_per_min = cur_num_patients_per_hour / 60

            mins_elapsed = time_delta.total_seconds() / 60

            self.patients_to_generate += mins_elapsed * cur_num_patients_per_min
            num_new_generate = int(self.patients_to_generate)

            self.patients_to_generate -= int(self.patients_to_generate)

            return num_new_generate
        else:
            cur_num_patients_per_hour = peak_num_patients_per_hour - (general_pph_slope * (num_loops % num_loops_at_peak))
            print(cur_num_patients_per_hour, "cur_num_patients_per_hour")
            cur_num_patients_per_min = cur_num_patients_per_hour / 60

            mins_elapsed = time_delta.total_seconds() / 60

            self.patients_to_generate += mins_elapsed * cur_num_patients_per_min
            num_new_generate = int(self.patients_to_generate)

            self.patients_to_generate -= int(self.patients_to_generate)

            return num_new_generate
