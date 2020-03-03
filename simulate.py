from datetime import timedelta
import datetime
from hospital_constant import HospitalConstant
from exam_room import ExamRoom
from priority_queue import PriorityQueue


def simulate_waiting(time_span=timedelta(days=1),
                     time_delta=timedelta(minutes=3)):
    doctors = HospitalConstant.DOCTORS
    exam_rooms = [ExamRoom() for _ in range(HospitalConstant.EXAM_ROOMS)]
    waiting_queue = PriorityQueue()
    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)
    end_datetime = start_datetime + time_span

    # --- MAIN LOOP FOR SIMULATION ---
    while cur_datetime < end_datetime:
        cur_datetime += time_delta
        exam_room_available = None
        for exam_room in exam_rooms:
            if exam_room.patient is None:
                exam_room_available = exam_room
                break
        if waiting_queue.has_patients_waiting() and doctors > 0 \
                and exam_room_available:
            # TODO: make patient enter exam room
            # - set entry time
            # - change patient status
            pass


if __name__ == '__main__':
    simulate_waiting()
