import sys
import math
import random
import threading
import time
from functools import reduce

with open("mydata.txt", mode="w", encoding="utf-8") as my_file:
    my_file.write("Some randomtext\nMore random text\nand more")

with open("mydata.txt", encoding="utf-8") as my_file:
    print(my_file.read())

print(my_file.closed)