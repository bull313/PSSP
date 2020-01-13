import sys
import math
import random
import threading
import time
from functools import reduce

print(r"I'll be ignored \n")
print("Hello " + "You")
str3 = "Hello You"

print("1st 3", str3[0:3])
print("Every other", str3[0:-1:2])

str3 = str3.replace("Hello", "Goodbye")
print(str3)

str3 = str3[:8] + "y" + str3[9:]
print(str3)

print("you" in str3)
print("you" not in str3)

print("You index", str3.find("you"))
print("        Helo      ".strip())
print("        Helo      ".rstrip())

print(" ".join(["Some", "Words"]))

print("A string".split(" "))