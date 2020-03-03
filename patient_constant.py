#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 20:55:52 2020

@author: minhuyen, popuguy
"""
import numpy as np
from enum import Enum
import random as rand


class PatientStatus(Enum):
    UNQUEUED = 0
    WAITING = 1
    IN_ROOM = 2
    EXITING = 3


class PatientConstant:
    AGE = np.range(10, 50, 1)
    GENDER = ["Male", "Female", "Prefer not to answer"]
    RACE = ["American", "Asian", "African"]
