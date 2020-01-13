import sys
import math
import random
import threading
import time
from functools import reduce

age = 15
if age < 5:
    print("Stay Home")
elif (age >= 5) and (age <= 6):
    print("Go to Kindergarten")
elif (age > 6) and (age <= 17):
    print("Grade", (age - 5))
else:
    print("College")

# condition_true true if condition else condition_false
canVote = True if age >= 18 else False
print(canVote)
    



