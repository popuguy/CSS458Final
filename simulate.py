from datetime import timedelta
import datetime
from hospital_constant import HospitalConstant
from exam_room import ExamRoom
from priority_queue import PriorityQueue
# from Model import Model
# from patient_working import Patient
from patient import Patient


def simulate_waiting(time_span=timedelta(days=1),
                     time_delta=timedelta(minutes=3)):
    doctors = HospitalConstant.DOCTORS
    exam_rooms = [ExamRoom() for _ in range(HospitalConstant.EXAM_ROOMS)]
    waiting_queue = PriorityQueue()
    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)  # SIMULATION CURRENT TIME
    end_datetime = start_datetime + time_span

    # --- MAIN LOOP FOR SIMULATION ---
    while cur_datetime < end_datetime:
        cur_datetime += time_delta  # Add elapsed time in simulation
        exam_rooms_available = []  # Exam rooms to fill
        for exam_room in exam_rooms:
            if exam_room.patient is None:
                exam_rooms_available.append(exam_room)
                break
        # Given at least one room, patients waiting, and doctors available
        # fill all available rooms with a doctor and patient
        while waiting_queue.has_patients_waiting() and doctors > 0 \
                and len(exam_rooms_available) > 0:
            # TODO: make patient enter exam room
            # - set entry time
            # - change patient status
            # model.patient_in_ED(patient)

            # model.patient_out_ED(patient)

            # model.next_patient(waiting_queue.get())




            cur_patient = waiting_queue.get()
            doctors -= 1
            cur_exam_room = exam_rooms_available[-1]
            # Remove availability of selected exam room
            exam_rooms_available = exam_rooms_available[:-1]

            cur_datetime += HospitalConstant.TIME_TRANSITION_SEEING_PATIENT

            cur_patient.serve(cur_datetime)
            cur_exam_room.patient = cur_patient


if __name__ == '__main__':
    simulate_waiting()
