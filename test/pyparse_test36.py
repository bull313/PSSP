import sys
import math
import random
import threading
import time
from functools import reduce

t1 = (1, 3.14, "Ben")
print("Length", len(t1))
print("1st", t1[0])
print("Last", t1[-1])
print("1st 2", t1[0:2])
print("Every other", t1[0:-1:2])
print("Reverse", t1[::-1])