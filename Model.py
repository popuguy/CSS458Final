# ---------------- Module General Import and Declarations ---------------------------------
import simpy
from patient import Patient as patient
from priority_queue import PriorityQueue as pq

# ========================================================================================
#                        General Documentation

"""Multiple functions module.

   See function docstring for description.
"""
# ----------------------------------------------------------------------------------------
#                        Additional Documentation
#
#This class is used to model the simulation
#
#
#
# ----------------------------------------------------------------------------------------
class Model:
    
    def __init__(self, env):
        self.env = env
        self.arrival_times = []
        self.rooms_available = []
        self.doctors_available = []
        self.patients_in_ED = []
        self.waiting_queue = pq
        self.patients_out_ED = []
        self.consultation_time = []

        # Set up counter for number fo patients entering simulation
        self.patient_count = 0

        # Set up running counts of patients waiting (total and by priority)
        self.patients_waiting = 0
    
    
    def patient_in_ED(self):
        self.arrival_times.append(patient.arrival_time)
        self.waiting_queue.add(patient)
        
    def patient_in_room(self):
        self.rooms_available 
        self.waiting_queue
    
    def patient_out_ED(self,patient):
        # now_step is going to be defined in the simulation class
        if self.waiting_queue.empty() or self.waiting_queue[0] > self.env.now_step:
            return None
        else:
            self.waiting_queue.get()[1]
            self.consultation_time.append(patient.consultation_time)
            return patient
        
    def next_patient():
        if self.waiting_queue.empty():
            return 
        else: 
            return max(self.waiting_queue[0], self.env.now_step)
        
    def chart(self):
        
        pass
    
    def createPatient():
        pass
    
    def calculate_mean(self):
        
    
    
