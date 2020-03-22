import sys
import math
import random
import threading
import time
from functools import reduce

s1 = set(["Ben", 1])
s2 = {"Paul", 1}

print("Length", len(s2))
s3 = s1 | s2
print(s3)
s3.add("Doug")
s3.discard("Ben")
print("Random", s3.pop())
s3 |= s2
print(s1.intersection(s2))
print(s1.symmetric_difference(s2))
print(s1.difference(s2))
s3.clear()
s4 = frozenset(["Paul", 7])