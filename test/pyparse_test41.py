import sys
import math
import random
import threading
import time
from functools import reduce

def get_sum(num1: int = 1, num2: int = 1):
    return num1 + num2

print(get_sum(5, 4))

def get_sum2(*args):
    sum = 0
    for arg in args:
        sum += arg
    return sum
print(get_sum2(1, 2, 3, 4))