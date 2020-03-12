# Import statements 
from datetime import timedelta
import datetime
from hospital_constant import HospitalConstant
from exam_room import ExamRoom
from priority_queue import PriorityQueue
from priority_queue import QueueingAlgorithm
from doctor import Doctor
from doctor_constant import *
from patient import Patient
from entrance_styles import PatientEntranceStyles


def time_delta_to_minutes(time_delta):
    """Accurate to one second time delta in minutes returned.
    :param time_delta A datetime.timedelta object
    :returns A float of minutes in the time delta
    """
    return (time_delta.days * 24 * 60) + (time_delta.seconds / 60)


def simulate_waiting(time_span=timedelta(days=1),
                     time_delta=timedelta(minutes=3),
                     verbose=False):
    """Main simulation function. Simulates the cycle of treat-and-release
    patients going from the waiting room, to the exam room, to leaving in an
    Emergency Department.

    :param verbose: If True, print info in simulation.
    :param time_span: Length of full simulation.
    :param time_delta: Time between movements in simulation.
    """
    doctors = [Doctor() for _ in range(HospitalConstant.NUM_DOCTORS)]
    exam_rooms = [ExamRoom() for _ in range(HospitalConstant.EXAM_ROOMS)]

    entrance_style = PatientEntranceStyles()

    # waiting_queue = PriorityQueue()
    waiting_queue = PriorityQueue(alg=QueueingAlgorithm.fast_first)
    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)  # SIMULATION CURRENT TIME
    end_datetime = start_datetime + time_span

    # patients_to_generate = 0.0
    # Place for all patients that came through the clinic. Used for
    # conclusions, not the actual simulation.
    patients_visiting = []

    num_loops = 0

    # --- MAIN LOOP FOR SIMULATION ---
    while cur_datetime < end_datetime:
        num_loops += 1
        cur_datetime += time_delta  # Add elapsed time in simulation

        exam_rooms_available = []  # Exam rooms to fill
        for exam_r in exam_rooms:
            if exam_r.patient is None:
                exam_rooms_available.append(exam_r)

        # --- FILLING ROOMS WITH PATIENTS ---
        while waiting_queue.has_patients_waiting() and \
                len(exam_rooms_available) > 0:
            cur_patient = waiting_queue.get()

            cur_exam_room = exam_rooms_available[-1]
            # Remove availability of selected exam room
            exam_rooms_available = exam_rooms_available[:-1]

            cur_patient.serve(cur_datetime)
            if verbose:
                print("Served patient", cur_patient.id)
            cur_exam_room.patient = cur_patient

        # --- UPDATE DOCTOR ACTIVITIES ---

        for doctor in doctors:
            doctor.update_activity(time_delta)

        # --- FILLING WITH DOCTORS ---
        doctors_available = []
        for doctor in doctors:
            if doctor.state is DoctorState.READY:
                doctors_available.append(doctor)

        for exam_r in exam_rooms:
            if len(doctors_available) < 1:
                break
            if exam_r.doctor is None and exam_r.patient is not None and \
                    exam_r.patient.seen_by_doctor is not True:
                doctors_available[-1].enter_exam_room(cur_datetime)
                exam_r.doctor = doctors_available[-1]
                if verbose:
                    print("Doctor", exam_r.doctor.id, "entered for patient",
                          exam_r.patient.id)
                doctors_available = doctors_available[:-1]

        # --- DOCTOR VISIT COMPLETIONS ---
        for exam_r in exam_rooms:
            if exam_r.doctor is not None and \
                    exam_r.doctor.has_completed_patient_visit(cur_datetime):
                exam_r.doctor.exit_exam_room()
                if verbose:
                    print("Doctor", exam_r.doctor.id, "left for patient",
                          exam_r.patient.id)
                exam_r.patient.seen_by_doctor = True

        # --- VACATE ROOMS APPROPRIATELY ---
        for exam_r in exam_rooms:
            if exam_r.patient is not None and \
                    exam_r.patient.has_completed_visit(cur_datetime):
                exam_r.patient.exit(cur_datetime)
                if verbose:
                    print("Patient", exam_r.patient.id, "left")
                exam_r.reset()

        # --- GIVE INFECTIONS ---
        patients_waiting = waiting_queue.get_queue_patients()
        num_infected_waiting = 0
        for patient in patients_waiting:
            if patient.infected:
                num_infected_waiting += 1
        for patient in patients_waiting:
            if not patient.infected and patient.try_contract_infection(time_delta, num_infected_waiting):
                print("Patient infected!!")

        # For different configurations of the simulation, patients will be
        # added at different intervals here
        patients_to_generate = entrance_style.rise_and_fall_linear(
            num_loops, time_delta)
        for i in range(patients_to_generate):
            patient = Patient()
            waiting_queue.add(patient, cur_datetime)
            patients_visiting.append(patient)

        # mins_elapsed = time_delta.total_seconds() / 60
        #
        # patients_per_minute = HospitalConstant.PATIENTS_PER_HOUR / 60.0
        #
        # patients_to_generate += mins_elapsed * patients_per_minute
        # unqueued_patients = [Patient() for _
        #                      in range(int(patients_to_generate))]
        #
        # patients_to_generate -= int(patients_to_generate)
        #
        # print("it would gen", entrance_style.rise_and_fall_linear(num_loops, time_delta), "patients here")
        #
        # # --- QUEUE PATIENTS ---
        # for patient in unqueued_patients:
        #     waiting_queue.add(patient, cur_datetime)
        #     patients_visiting.append(patient)

    # Conclusions
    total_wait_time = 0
    total_served_patients = 0
    for i in range(len(patients_visiting)):
        if patients_visiting[i].time_queued is None or \
                patients_visiting[i].time_served is None:
            continue

        total_served_patients += 1
        wait_time_patient_delta = patients_visiting[i].time_served - \
                                  patients_visiting[i].time_queued
        wait_time_patient_mins = time_delta_to_minutes(wait_time_patient_delta)
        total_wait_time += wait_time_patient_mins
    avg_wait_time = total_wait_time / total_served_patients
    print("Average wait time for simulation:", avg_wait_time, "minutes.")


if __name__ == '__main__':
    simulate_waiting()
