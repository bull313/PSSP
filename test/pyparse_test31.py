import sys
import math
import random
import threading
import time
from functools import reduce

l1 = [1, 3.14, "Ben", True]
print("Length", len(l1))
print("1st", l1[0])
print("Last", l1[-1])

l1[0] = 2
l1[2:4] = ["Bob", False]
l1[2:2] = ["Paul", 9]
l1.insert(2, "Paul")
l2 = l1 + ["Egg", 4]
l2.remove("Paul")
l2.pop(0)
print("l2", l2)

l2 = ["Egg", 4] + l1
l3 = [[1, 2], [3, 4]]
print("[1, 1]", l3[1][1])

print("1 Exists", (1 in l1))
print("Min", min([1, 2, 3]))
print("Max", max([1, 2, 3]))
print("1dt 2", l1[0:2])
print("Every Other", l1[0:-1:2])
print("Reverse", l1[::-1])