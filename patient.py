import random


class Patient:
    def __init__(self):
        self._give_statistical_attributes()

    def _give_statistical_attributes(self):
        self.age = random.choice(10, 20, 30)
