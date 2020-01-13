import sys
import math
import random
import threading
import time
from functools import reduce

one_to_4 = range(1, 5)
times2 = lambda x: x * 2
print(list(map(times2, one_to_4)))

print(list(filter(lambda x: x % 2 == 0), range(1, 11)))

print(reduce(lambda x, y: x + y), range(1, 6))