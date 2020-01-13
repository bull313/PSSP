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
    
    def __gt__(self, animal2):
        if self.__weight > animal2.__weight:
            return True
        else:
            return False

class Dog(Animal):
    def __init__(self, name="unknown", owner="unknown", weight=0):
        Animal.__init__(self, name, weight)
        self.__owner = owner
    
    def __str__(self):
        return super().__str__() + " and is owned by " + self.__owner

animal = Animal("spot", 100)
print(animal)
dog = Dog("Bowser", "Bob", 150)
print(dog)
print(animal > dog)