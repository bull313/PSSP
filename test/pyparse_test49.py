import sys
import math
import random
import threading
import time
from functools import reduce

class Animal:
    def __init__(self, name="unknown", weight=0):
        self.__name = name
        self.__weight = weight
    
    @property
    def name(self, name):
        self.__name = name
    
    def make_noise(self):
        return "Grrrrr"
    
    def __str__(self):
        return "{} is a {} and says {}".format(self.__name, type(self).__name__, self.make_noise())
