class PriorityQueue:
    # Here, I have just defaulted to a lambda first-come first-serve for the
    # queueing algorithm
    def __init__(self, alg=lambda a, b: a.append(b)):
        """Setup for initiating a PriorityQueue object.

        :param alg: algorithm to use for adding a new patient to the queue.
        Algorithm methods must have two parameters, #1: queue and #2 patient.
        """
        self.patients = []
        self.queue_algorithm = alg

    def add(self, patient, add_time):
        """Queues a new patient to a position in the waiting queue based on
        the queue algorithm from __init__.

        :param patient: patient to queue.
        """
        patient.queue(add_time)
        self.patients = self.queue_algorithm(self.patients, patient)

    def get(self):
        """Removes the top waiting patient from the queue and returns them.

        :return: top waiting member of the queue
        """
        if len(self.patients) < 1:
            return None

        ret_patient = self.patients[0]
        self.patients = self.patients[1:]
        return ret_patient

    def has_patients_waiting(self):
        return len(self.patients) > 0

    def get_length(self):
        return len(self.patients)

    def get_queue_patients(self):
        return self.patients

    # from priority_queue import PriorityQueue as q

    # This is what I did so far. Please check the code if it's correct and modified it to fit our model. Thank you.


class QueueingAlgorithm:
    """A priority queue based on the treatment time.
    """

    @staticmethod
    def fast_first(patient_list, patient):
        """A queueing algorithm that always prioritizes patients with faster
        predicted times in the exam room

        :param patient_list: The waiting queue to add to
        :param patient: The patient to add
        :return: Ordered patient list with newly added patient
        """
        # traverse the queue
        for x in range(0, len(patient_list)):
            # if the treatment time of the current patient is longer
            if patient.treatment_time >= patient_list[x].treatment_time:
                # if we have traversed the complete queue
                if x == (len(patient_list) - 1):
                    # add the patient at the end
                    patient_list.insert(x + 1, patient)
                    return patient_list
                else:
                    continue
            else:
                patient_list.insert(x, patient)
                return patient_list
        patient_list.append(patient)
        return patient_list

    @staticmethod
    def urgent_first(patient_list, patient):
        """Prioritize patients with higher levels of urgency.
        """
        # traverse the queue
        for x in range(0, len(patient_list)):
            # if the treatment time of the current patient is longer
            if patient.levelOfUrgency <= patient_list[x].levelOfUrgency:
                # if we have traversed the complete queue
                if x == (len(patient_list) - 1):
                    # add the patient at the end
                    patient_list.insert(x + 1, patient)
                else:
                    continue
            else:
                patient_list.add(x, patient)
                return patient_list
