import sys
import math
import random
import threading
import time
from functools import reduce

age = 30
if age > 21:
    print("You can drive a tractor trailer")
elif age >= 16:
    print("You can drive a car")
else:
    print("You can't drive at all")