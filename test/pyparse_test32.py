import sys
import math
import random
import threading
import time
from functools import reduce

w1 = 1
while w1 < 5:
    print(w1)
    w1 += 1

w2 = 0
while w2 < 20:
    if w2 % 2 == 0:
        print(w2)
    elif w2 == 0:
        break
    else:
        w2 += 1
        continue
    w2 += 1

l4 = [1, 3.14, "Ben"]
while len(14):
    print(l4.pop(0))

