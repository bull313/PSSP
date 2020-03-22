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

def next_2(num):
    return num + 1, num + 2

i1, i2 = next_2(5)
print(i1, i2)

def mult_by(num):
    return lambda x: x * num
print("3 * 5 = ", (mult_by(3)(5)))

def mult_list(list, func):
    for x in list:
        print(func(x))
mult_by_4 = mult_by(4)
mult_list(list(range(0, 5)), mult_by_4)

power_list = [lambda x: x ** 2, 
                lambda x: x ** 3]