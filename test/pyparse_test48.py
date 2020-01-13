import sys
import math
import random
import threading
import time
from functools import reduce

class Square:
    def __init__(self, height="0", width="0"):
        self.height = height
        self.width = width
    @property
    def height(self):
        print("Retrieving the height")
        return self.__height
    
    @height.setter
    def height(self, value):
        if value.isdigit():
            self.__height = value
        else:
            print("Please only enter numbers for height")

    @property
    def width(self):
        print("Retrieving the width")
        return self.__width
    
    @width.setter
    def width(self, value):
        if value.isdigit():
            self.__width = value
        else:
            print("Please only enter numbers for width")
    
    def get_area(self):
        return int(self.__width * self.__height)

square = Square()
square.height = "10"
square.width = "10"
print("Area", square.get_area())