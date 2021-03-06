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
import numpy as N
import matplotlib.pyplot as plt


def time_delta_to_minutes(time_delta):
    """Accurate to one second time delta in minutes returned.
    :param time_delta A datetime.timedelta object
    :returns A float of minutes in the time delta
    """
    return (time_delta.days * 24 * 60) + (time_delta.seconds / 60)


def simulate_waiting(time_span=timedelta(days=1),
                     time_delta=timedelta(minutes=3),
                     verbose=False,
                     queue_method="prioritize_treatment_time",
                     number_of_exam_rooms=HospitalConstant.EXAM_ROOMS,
                     number_of_doctors=HospitalConstant.NUM_DOCTORS,
                     setAttributes=True, use_linear_rise_fall=True,
                     basic_patients_per_hour=None,
                     portion_time_doc_spend=False,
                     portionChange=0.25, get_infected_percent=False):
    """Main simulation function. Simulates the cycle of treat-and-release
    patients going from the waiting room, to the exam room, to leaving in an
    Emergency Department.
    :param number_of_exam_rooms: Number exam rooms to use
    :param number_of_doctors: Number of doctors to use
    :param setAttributes: Parameter only used in making graphs
    :param use_linear_rise_fall: Parameter only used in making graphs
    :param basic_patients_per_hour: Parameter only used in making graphs
    :param portion_time_doc_spend: Parameter only used in making graphs
    :param portionChange: Parameter only used in making graphs
    :param get_infected_percent: Parameter only used in making graphs
    :return: Average waiting time, or if appropriate, portion of patients infected
    :param verbose: If True, print info in simulation.
    :param time_span: Length of full simulation.
    :param time_delta: Time between movements in simulation.
    :param queue_method: 2 alternative queuing method
    """

    doctors = [Doctor() for _ in range(number_of_doctors)]
    exam_rooms = [ExamRoom() for _ in range(number_of_exam_rooms)]

    entrance_style = PatientEntranceStyles()
    #    print("queue_method = ", queue_method)
    if (queue_method == "first_come_first_serve"):
        waiting_queue = PriorityQueue()
    elif (queue_method == "prioritize_treatment_time"):
        waiting_queue = PriorityQueue(alg=QueueingAlgorithm.fast_first)

    start_datetime = datetime.datetime(2020, 1, 1)
    cur_datetime = datetime.datetime(2020, 1, 1)  # SIMULATION CURRENT TIME
    end_datetime = start_datetime + time_span

    # patients_to_generate = 0.0
    # Place for all patients that came through the clinic. Used for
    # conclusions, not the actual simulation.
    patients_visiting = []

    num_loops = 0
    total_num_patients_infected = 0

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
        if portion_time_doc_spend == False:
            for doctor in doctors:
                doctor.update_activity(time_delta)

         # For different portion time
        if portion_time_doc_spend == True:
            for doctor in doctors:
                doctor.update_activity_change_portion_time(time_delta, portion=portionChange)

        # --- FILLING WITH DOCTORS ---
        doctors_available = []
        for doctor in doctors:
            if doctor.state is DoctorState.READY:
                doctors_available.append(doctor)

        for exam_r in exam_rooms:
            if len(doctors_available) < 1:
                break
            if exam_r.doctor is None and exam_r.patient is not None and \
                    not exam_r.patient.seen_by_doctor:
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

                if verbose:
                    print("Doctor", exam_r.doctor.id, "left for patient",
                          exam_r.patient.id)
                # exam_r.doctor.exit_exam_room()
                exam_r.make_doctor_exit()
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
            if not patient.infected and \
                    patient.try_contract_infection(
                        time_delta, num_infected_waiting):
                total_num_patients_infected += 1
                if verbose:
                    print("Patient infected!!")

        # For different configurations of the simulation, patients will be
        # added at different intervals here
        patients_to_generate = None
        if use_linear_rise_fall:
            patients_to_generate = entrance_style.rise_and_fall_linear(
                num_loops, time_delta)
        else:
            patients_to_generate = entrance_style.basic(time_delta, basic_patients_per_hour)

        for i in range(patients_to_generate):
            patient = Patient(setAttributes)
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
        # print("it would gen", entrance_style.rise_and_fall_linear(num_loops,
        # time_delta), "patients here")
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
    global avg_wait_time
    avg_wait_time = total_wait_time / total_served_patients
    #    print("total_served_patients = ", total_served_patients)
    #    print("Average wait time for simulation:", avg_wait_time, "minutes.")

    # Number of patients infected
    #    print(total_num_patients_infected, "total_num_patients_infected")
    portion_patients_infected = total_num_patients_infected / len(patients_visiting)
    if get_infected_percent:
        return portion_patients_infected
    return avg_wait_time  # , total_served_patients


def compareQueuingMethod():
    """This function compare average waiting time of 2 queuing methods
    "first come, first served" and "process queueing by CPU burst time," 
    which prioritize patients with faster treatment time
    
    """
    print("Comparing patient's average waiting time" +
          " using 2 queuing methods...")
    print("(can take up to 10 seconds)")
    iteration = 50
    iteration_step = N.arange(iteration) + 1

    # Average waiting-time using different queuing methods
    waittime_first_come_first_serve = N.zeros(iteration, dtype='d')
    waittime_prioritize_treatment_time = N.zeros(iteration, dtype='d')

    for i in range(iteration):
        waittime_first_come_first_serve[i] = \
            simulate_waiting(queue_method="first_come_first_serve")
        waittime_prioritize_treatment_time[i] = \
            simulate_waiting(queue_method="prioritize_treatment_time")

    mean_waittime_first_come_first_serve = \
        N.mean(waittime_first_come_first_serve)
    mean_waittime_prioritize_treatment_time = \
        N.mean(waittime_prioritize_treatment_time)

    print("'First come, first served' queuing method: ",
          round(mean_waittime_first_come_first_serve, 1), " minutes")
    print("'Process queueing by CPU burst time' queuing method: ", \
          round(mean_waittime_prioritize_treatment_time, 1), " minutes")

    plt.figure(1)
    plt.plot(iteration_step, waittime_first_come_first_serve,
             color='skyblue', label="'First come, first served'")
    plt.plot(iteration_step, waittime_prioritize_treatment_time, color='olive',
             linestyle='dashed', label="'Process queueing by CPU burst time'")
    plt.xlabel("Iteration")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time using 2 different queuing methods")
    plt.legend()
    plt.show()
    print()


#    plt.figure(1)
#    plt.plot(waittime_first_come_first_serve, time)
#    plt.xlabel("waittime_first_come_first_serve")
#    plt.ylabel("Time")
#    plt.show()
#    
#    plt.figure(2)
#    plt.plot(waittime_prioritize_treatment_time, time)
#    plt.xlabel("waittime_prioritize_treatment_time")
#    plt.ylabel("Time")
#    plt.show()

def compareExamRoomsQuantity():
    """This function compare average waiting time with different number of
    examination rooms
    
    """
    print("Comparing patient's average waiting time using different \
          number of examination rooms...")
    print("(can take up to 10 seconds)")

    # Setting as 10 because iteration of 50 gives the same result
    iteration = 10
    exam_rooms = N.arange(1, 10) * 10  # Number of examination rooms
    # Mean of all average waiting time in 100 iterations
    mean_avg_wait_time = N.arange(len(exam_rooms))

    for i in range(len(exam_rooms)):
        avg_wait_time = N.arange(iteration)

        for j in range(iteration):
            avg_wait_time[j] = \
                simulate_waiting(number_of_exam_rooms=exam_rooms[i])

        mean_avg_wait_time[i] = N.mean(avg_wait_time)

    plt.figure(1)
    plt.plot(exam_rooms, mean_avg_wait_time)
    plt.xlabel("Number of examination rooms")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time vs. Number of examination rooms")
    plt.show()
    print()


def compareDoctorsQuantity():
    """This function compare average waiting time with 
    different number of doctors
    
    """
    print("Comparing patient's average waiting time using different" +
          " number of doctors...")
    print("(can take up to 30 seconds)")

    iteration = 30
    num_of_doctors = N.arange(1, 10) * 5  # Number of examination rooms
    # Mean of all average waiting
    mean_avg_wait_time = N.arange(len(num_of_doctors))
    # - time in 100 iterations

    for i in range(len(num_of_doctors)):
        avg_wait_time = N.arange(iteration)

        for j in range(iteration):
            avg_wait_time[j] = \
                simulate_waiting(number_of_doctors=num_of_doctors[i])

        mean_avg_wait_time[i] = N.mean(avg_wait_time)

    plt.figure(2)
    plt.plot(num_of_doctors, mean_avg_wait_time)
    plt.xlabel("Number of doctors")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time vs. Number of doctors")
    plt.show()
    print()


def comparePatientsWithoutAttributes():
    """This function compare average waiting time with of patients with and
    without taking into account of their attributes
    
    """
    print("Comparing patient's average waiting time with and without \
          taking into account of their attributes...")
    print("(can take up to 10 seconds)")
    iteration = 25
    iteration_step = N.arange(iteration) + 1

    wait_time_with_attributes = N.zeros(iteration, dtype='d')
    wait_time_without_attributes = N.zeros(iteration, dtype='d')

    for i in range(iteration):
        wait_time_with_attributes_i = N.zeros(iteration, dtype='d')
        wait_time_without_attributes_i = N.zeros(iteration, dtype='d')
        for j in range(iteration):
            wait_time_with_attributes_i[j] = simulate_waiting(setAttributes=True)
            wait_time_without_attributes_i[j] = simulate_waiting(setAttributes=False)
        wait_time_with_attributes[i] = N.mean(wait_time_with_attributes_i)
        wait_time_without_attributes[i] = N.mean(wait_time_without_attributes_i)

    mean_wait_time_with_attributes = N.mean(wait_time_with_attributes)
    mean_wait_time_without_attributes = N.mean(wait_time_without_attributes)

    print("Taking into account of attributes: ",
          round(mean_wait_time_with_attributes, 1), " minutes")
    print("Without taking into account of attributes: ",
          round(mean_wait_time_without_attributes, 1), " minutes")
    print()

    plt.figure(3)
    plt.plot(iteration_step, wait_time_with_attributes,
             color='skyblue', label="With attributes")
    plt.plot(iteration_step, wait_time_without_attributes, color='olive',
             linestyle='dashed', label="Without attributes")
    plt.xlabel("Iteration")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time with and without patient's attributes")
    plt.legend()
    plt.show()
    print()


def compareDoctorsPlusExamRoomsQuantity():
    """This function compares the average waiting time with
        different number of doctors and exam rooms

        """
    print("Comparing patient's average waiting time using different" +
          " number of  and exam rooms...")
    print("(can take up to 30 seconds)")

    iteration = 30
    num_of_doctors = N.arange(1, 10) * 5  # Number of doctors
    exam_rooms = N.arange(1, 10) * 10  # Number of examination rooms
    # Mean of all average waiting
    mean_avg_wait_time = N.arange(len(num_of_doctors))
    # - time in 100 iterations

    for i in range(len(num_of_doctors)):
        avg_wait_time = N.arange(iteration)

        for j in range(iteration):
            avg_wait_time[j] = \
                simulate_waiting(number_of_doctors=num_of_doctors[i],
                                 number_of_exam_rooms=exam_rooms[i])

        mean_avg_wait_time[i] = N.mean(avg_wait_time)

    plt.figure(2)
    plt.plot(num_of_doctors, mean_avg_wait_time)
    plt.xlabel("Number of doctors and exam rooms")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time vs. Number of doctors and exam rooms")
    plt.show()
    print()


def comparePerformanceBenefitExamRoomsDoctorsEqualPrioritizationChange():
    print("Comparing benefits of increased exam rooms and doctors to benefit + "
          " of prioritizing patients based on projected examination time")
    iteration = 30
    num_of_doctors = N.arange(1, 10) * 5  # Number of doctors
    exam_rooms = N.arange(1, 10) * 10  # Number of examination rooms
    # Mean of all average waiting
    mean_avg_wait_time = N.arange(len(num_of_doctors))
    # - time in 100 iterations

    for i in range(len(num_of_doctors)):
        avg_wait_time = N.arange(iteration)

        for j in range(iteration):
            avg_wait_time[j] = \
                simulate_waiting(number_of_doctors=num_of_doctors[i],
                                 number_of_exam_rooms=exam_rooms[i])

        mean_avg_wait_time[i] = N.mean(avg_wait_time)

    avg_wait_time = N.arange(iteration)
    for i in range(iteration):
        avg_wait_time[i] = simulate_waiting(number_of_doctors=5, number_of_exam_rooms=10)

    wait_time_with_prioritization = N.mean(avg_wait_time)
    for wait_time_avg in mean_avg_wait_time:
        if wait_time_avg > wait_time_with_prioritization:
            print("better than one increase of 5 doctors and 10 exam rooms")


def compareAvgWaitingTimeAsPatientPerHourIncreases():
    patients_per_hour = (N.arange(0, 22) * 0.5) + 1.5
    iterations = 50
    average_wait_time_averages = N.zeros(len(patients_per_hour))
    for i in range(len(patients_per_hour)):
        average_wait_times = N.zeros(iterations)
        for j in range(iterations):
            average_wait_times[j] = \
                simulate_waiting(use_linear_rise_fall=False,
                                 basic_patients_per_hour=patients_per_hour[i])
        average_wait_time_averages[i] = N.mean(average_wait_times)

    plt.figure(2)
    plt.plot(patients_per_hour, average_wait_time_averages)
    plt.xlabel("N patients per hour")
    plt.ylabel("Waiting time average")
    plt.title("Full simulation run with N patients per hour vs Resultant average wait time")
    plt.show()


def comparePercentPatientsInfectedFCFSVsFastFirst():
    # ------------------------------------------------------------------------------------------------------------------------------------paul working
    patients_per_hour = (N.arange(0, 22) * 0.5) + 1.5
    iterations = 10
    infected_percent_averages_fcfs = N.zeros(len(patients_per_hour))
    print(len(infected_percent_averages_fcfs))
    infected_percent_averages_ff = N.zeros(len(patients_per_hour))
    for i in range(len(patients_per_hour)):
        print("Progress:", int(i / len(patients_per_hour) * 100), "%")
        infected_percent_fcfs = N.zeros(iterations)
        infected_percent_ff = N.zeros(iterations)
        for j in range(iterations):
            infected_percent_fcfs[j] = \
                simulate_waiting(use_linear_rise_fall=False,
                                 basic_patients_per_hour=patients_per_hour[i],
                                 get_infected_percent=True,
                                 queue_method="first_come_first_serve")
            infected_percent_ff[j] = \
                simulate_waiting(use_linear_rise_fall=False,
                                 basic_patients_per_hour=patients_per_hour[i],
                                 get_infected_percent=True,
                                 queue_method="prioritize_treatment_time")
        infected_percent_averages_fcfs[i] = N.mean(infected_percent_fcfs)
        infected_percent_averages_ff[i] = N.mean(infected_percent_ff)

    plt.figure(2)
    plt.plot(patients_per_hour, infected_percent_averages_fcfs,
             color='skyblue', label="FCFS")
    plt.plot(patients_per_hour, infected_percent_averages_ff, color='olive',
             linestyle='dashed', label="Fast-first")

    plt.xlabel("N patients per hour")
    plt.ylabel("Portion patients infected")
    plt.legend(loc="upper left")
    plt.title("Comparison of FCFS queuing with fast-first queuing over N patients per hour")
    plt.show()


def compareWaitingTimeAndDeviationByTimeDelta():
    iterations = 100  # Iterations per run
    delta_increment = 5  # Minutes
    num_deltas_to_try = 10  # Total number of sets of averages
    delta_minutes = (N.arange(0, num_deltas_to_try) * delta_increment) + 1
    average_wait_time_averages = N.zeros(num_deltas_to_try)
    average_wait_times = []

    i = 0
    for mins in delta_minutes:
        wait_time_set = []
        for iter in range(iterations):
            iteration_wait_time = simulate_waiting(time_delta=timedelta(minutes=float(mins)))
            wait_time_set.append(iteration_wait_time)
        average_wait_times.append(wait_time_set)
        average_wait_time_averages[i] = N.mean(wait_time_set)

        iter += 1

    std_devs = [N.std(times) for times in average_wait_times]

    plt.figure(2)
    plt.plot(delta_minutes, std_devs)
    plt.xlabel("Minutes in time delta for loop iterations")
    plt.ylabel("Waiting time standard deviation")
    plt.title("Standard deviation of wait time as a function of minutes in loop iteration time delta")
    plt.show()

def compareDoctorTimeSpent():
    """This function compares the average waiting time as portion of doctor
    time spent with patients increases
    """

    print("Comparing the average waiting time as portion of doctor time " +
          "spent with patients increases...")
    print("(can take up to 40 seconds)")

    iteration = 100

    portion_time = N.arange(1,8) * 0.125
    mean_avg_wait_time = N.arange(len(portion_time)) #- Mean of all average waiting
#    portionChange = 0.25
#    portion_time = []
#    portion_time.append(portionChange)

    for i in range(len(portion_time)):
        avg_wait_time = N.arange(iteration)

        for j in range(iteration):
            avg_wait_time[j] = \
                simulate_waiting(portion_time_doc_spend=True, portionChange=portion_time[i])

#            portionChange += 0.20
#            portion_time.append(portionChange)
        mean_avg_wait_time[i] = N.mean(avg_wait_time)

    plt.figure(2)
#    plt.xticks(portion_time)
    plt.plot(portion_time, mean_avg_wait_time)
    plt.xlabel("Portion of time doctor spends with patient")
    plt.ylabel("Average waiting time")
    plt.title("Average waiting time vs. Portion of time doctor spends with patient")
    plt.show()
    print()

def comparePercentPatientsInfectedAndWaitingTime():
    patients_per_hour = (N.arange(0, 22) * 0.5) + 1.5
    iterations = 10
    infected_percent_averages = N.zeros(len(patients_per_hour))
    averages_wait_time = N.zeros(len(patients_per_hour))
    for i in range(len(patients_per_hour)):
        print("Progress:", int(i / len(patients_per_hour) * 100), "%")
        infected_percent = N.zeros(iterations)
        waiting_time = N.zeros(iterations)
        for j in range(iterations):
            infected_percent[j] = \
                simulate_waiting(use_linear_rise_fall=False,
                                 basic_patients_per_hour=patients_per_hour[i],
                                 get_infected_percent=True)
            waiting_time[j] = avg_wait_time
        infected_percent_averages[i] = N.mean(infected_percent)
        averages_wait_time[i] = N.mean(waiting_time)
        #print(infected_percent_averages[i])
def comparePatientRiskContagiousnessLevel():
    r0s = N.arange(1,10) * 0.3
    # PatientConstant.get_adjusted_infection_chance(r0)

    # iterations = 10
    # infected_percent_averages = N.zeros(len(r0s))
    # averages_wait_time = N.zeros(len(r0s))
    # for i in range(len(r0s)):
    #     print("Progress:", int(i / len(patients_per_hour) * 100), "%")
    #     infected_percent = N.zeros(iterations)
    #     waiting_time = N.zeros(iterations)
    #     for j in range(iterations):
    #         infected_percent[j] = \
    #             simulate_waiting(use_linear_rise_fall=False,
    #                              basic_patients_per_hour=4,
    #                              get_infected_percent=True)
    #         waiting_time[j] = avg_wait_time
    #     infected_percent_averages[i] = N.mean(infected_percent)
    #     averages_wait_time[i] = N.mean(waiting_time)
    #     # print(infected_percent_averages[i])




def comparePortionPatientsInfectiousInitially():
    pass

def compareThreeDemographics():
    """Use Italian and American demographic data for runs

    :return:
    """
    pass

    # plt.figure(2)
    # #plt.plot(infected_percent_averages, averages_wait_time)
    # plt.scatter(infected_percent_averages, averages_wait_time)
    # plt.xlabel("Percentage of infected patients")
    # plt.ylabel("Waiting time")
    # plt.title("Comparing percentage of infected patients and waiting time")
    # plt.show()
# Finished metrics:
# 1 patients with and without attribute thinking
# 2 patient average waiting time with just doctor increase
# 3 patient average waiting time with just exam room increase
# 4 compare FCFS vs. prioritization fast first

# 5 Check number of increased exam rooms and doctors equal to prioritization change
# 6 Performance increase per adding doctors AND exam rooms
#
#
# Next metrics:
# 7 Average waiting time as number of patients per hour increases
# 8 Average waiting time as portion of doctor time spent with patients increases
# 9 Waiting time for more doctors vs additional portion of time with patient
# 10 Percent of patients infected vs waiting time
# 11 Percent of patients infected with prioritization vs fcfs
# 12 Risk to patients with different contagiousness level
# 13 Amount of waiting time by demographic

# 14 Average waiting time with time delta change
# 15 Average waiting time with simulation length increase
# 16 Average percent of people infected vs percent of people coming in infectious


if __name__ == '__main__':
    # compareQueuingMethod()
    # compareExamRoomsQuantity()
    # compareDoctorsQuantity()
    # comparePatientsWithoutAttributes()

    # comparePerformanceBenefitExamRoomsDoctorsEqualPrioritizationChange()

    # compareWaitingTimeAndDeviationByTimeDelta()
    # compareAvgWaitingTimeAsPatientPerHourIncreases()
    compareDoctorTimeSpent()

    comparePercentPatientsInfectedAndWaitingTime()
   # simulate_waiting(verbose=True)  #default calling function

#    comparePercentPatientsInfectedFCFSVsFastFirst()
