import sys
import math
import random
import threading
import time
from functools import reduce

print(list(range(0, 5)))
print(list(range(0, 10, 2)))

num_list = [[1, 2, 3], [10, 20, 30], [100, 200, 300]]

for x in range(0, 3):
    for y in range(0, 3):
        print(num_list[x][y])