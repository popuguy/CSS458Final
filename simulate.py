# Import statements 
from datetime import timedelta
import datetime
from hospital_constant import HospitalConstant
from exam_room import ExamRoom
from priority_queue import PriorityQueue
from doctor import Doctor
from doctor_constant import *
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
    # unqueued_patients = []
    waiting_queue = PriorityQueue()
    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)  # SIMULATION CURRENT TIME
    end_datetime = start_datetime + time_span

    patients_to_generate = 0.0

    # --- MAIN LOOP FOR SIMULATION ---
    while cur_datetime < end_datetime:
        cur_datetime += time_delta  # Add elapsed time in simulation

        exam_rooms_available = []  # Exam rooms to fill
        for exam_r in exam_rooms:
            if exam_r.patient is None:
                exam_rooms_available.append(exam_r)
#        print(exam_rooms_available)

        # --- FILLING ROOMS WITH PATIENTS ---
        while waiting_queue.has_patients_waiting() and \
                len(exam_rooms_available) > 0:
            cur_patient = waiting_queue.get()

            cur_exam_room = exam_rooms_available[-1]
            # Remove availability of selected exam room
            exam_rooms_available = exam_rooms_available[:-1]

            cur_patient.serve(cur_datetime)
            print("Served patient", cur_patient.id)
            cur_exam_room.patient = cur_patient

        # --- FILLING WITH DOCTORS ---
        doctors_available = []
        for doctor in doctors:
            if doctor.state is DoctorState.READY:
                doctors_available.append(doctor)
#        print(doctors_available)

        for exam_r in exam_rooms:
            if len(doctors_available) < 1:
                break
            if exam_r.doctor is None and exam_r.patient is not None and\
                    exam_r.patient.seen_by_doctor is not True:
                doctors_available[-1].enter_exam_room(cur_datetime)
                exam_r.doctor = doctors_available[-1]
                print("Doctor", exam_r.doctor.id, "entered for patient",
                      exam_r.patient.id)
                doctors_available = doctors_available[:-1]
#            print(doctors_available)

        # --- DOCTOR VISIT COMPLETIONS ---
        for exam_r in exam_rooms:
            if exam_r.doctor is not None and \
                    exam_r.doctor.has_completed_patient_visit(cur_datetime):
                exam_r.doctor.exit_exam_room()
                print("Doctor", exam_r.doctor.id, "left for patient", 
                      exam_r.patient.id)
                exam_r.patient.seen_by_doctor = True

        # --- VACATE ROOMS APPROPRIATELY ---
        for exam_r in exam_rooms:
            if exam_r.patient is not None and \
                    exam_r.patient.has_completed_visit(cur_datetime):
                exam_r.patient.exit(cur_datetime)
                print("Patient", exam_r.patient.id, "left")
                exam_r.reset()

        # For different configurations of the simulation, patients will be
        # added at different intervals here
        mins_elapsed = time_delta.total_seconds() / 60

        patients_per_minute = HospitalConstant.PATIENTS_PER_HOUR / 60.0

        patients_to_generate += mins_elapsed * patients_per_minute
        unqueued_patients = [Patient() for _
                              in range(int(patients_to_generate))]
        
        #print("Patients to generate", patients_to_generate)

        patients_to_generate -= int(patients_to_generate)

        # --- QUEUE PATIENTS ---
        for patient in unqueued_patients:
            waiting_queue.add(patient)
#            print("Added patient. Queue length now",
#                  waiting_queue.get_length())


if __name__ == '__main__':
    simulate_waiting()
