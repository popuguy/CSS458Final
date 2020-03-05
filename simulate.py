from datetime import timedelta
import datetime
from hospital_constant import HospitalConstant
from exam_room import ExamRoom
from priority_queue import PriorityQueue
from doctor import Doctor
from doctor_constant import *
# from Model import Model
# from patient_working import Patient
from patient import Patient


def simulate_waiting(time_span=timedelta(days=1),
                     time_delta=timedelta(minutes=3)):
    """Main simulation function. Simulates the cycle of treat-and-release
    patients going from the waiting room, to the exam room, to leaving in an
    Emergency Department.

    :param time_span: Length of full simulation.
    :param time_delta: Time between movements in simulation.
    """
    # doctors = HospitalConstant.DOCTORS
    doctors = [Doctor() for _ in range(HospitalConstant.NUM_DOCTORS)]
    exam_rooms = [ExamRoom() for _ in range(HospitalConstant.EXAM_ROOMS)]
    unqueued_patients = []
    waiting_queue = PriorityQueue()
    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)  # SIMULATION CURRENT TIME
    end_datetime = start_datetime + time_span

    patients_to_generate = 0.0

    # --- MAIN LOOP FOR SIMULATION ---
    while cur_datetime < end_datetime:
        cur_datetime += time_delta  # Add elapsed time in simulation

        exam_rooms_available = []  # Exam rooms to fill
        for exam_room in exam_rooms:
            if exam_room.patient is None:
                exam_rooms_available.append(exam_room)

        # --- FILLING ROOMS WITH PATIENTS ---
        while waiting_queue.has_patients_waiting() and \
                len(exam_rooms_available) > 0:
            cur_patient = waiting_queue.get()

            cur_exam_room = exam_rooms_available[-1]
            # Remove availability of selected exam room
            exam_rooms_available = exam_rooms_available[:-1]

            cur_patient.serve(cur_datetime)
            cur_exam_room.patient = cur_patient

        # --- FILLING WITH DOCTORS ---
        doctors_available = []
        for doctor in doctors:
            if doctor.state is DoctorState.READY:
                doctors_available.append(doctor)

        for exam_room in exam_rooms:
            if len(doctors_available) < 1:
                break
            if exam_room.doctor is not None and \
                    exam_room.patient.seen_by_doctor is not True:
                doctors_available[-1].enter_exam_room(cur_datetime)
                exam_room.doctor = doctors_available[-1]
                doctors_available = doctors_available[:-1]

        # --- DOCTOR VISIT COMPLETIONS ---
        for exam_room in exam_rooms:
            if exam_room.doctor is not None and \
                    exam_room.doctor.has_completed_patient_visit(cur_datetime):
                exam_room.doctor.exit_exam_room()
                exam_room.patient.seen_by_doctor = True

        # --- VACATE ROOMS APPROPRIATELY ---
        for exam_room in exam_rooms:
            if exam_room.patient.has_completed_visit(cur_datetime):
                exam_room.patient.exit(cur_datetime)
                exam_room.reset()

        # For different configurations of the simulation, patients will be
        # added at different intervals here
        mins_elapsed = time_delta.total_seconds() / 60

        patients_per_minute = HospitalConstant.PATIENTS_PER_HOUR / 60.0

        patients_to_generate += mins_elapsed * patients_per_minute
        unqueued_patients += [Patient() for _
                              in range(int(patients_to_generate))]

        patients_to_generate -= int(patients_to_generate)

        # --- QUEUE PATIENTS ---
        for patient in unqueued_patients:
            waiting_queue.add(patient)


if __name__ == '__main__':
    simulate_waiting()
