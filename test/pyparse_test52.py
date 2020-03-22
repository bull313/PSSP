import sys
import math
import random
import threading
import time
import re

if re.search("ape", "The ape at the apex"):
    print("There is an ape")

allApes = re.findall("ape", "The ape at the apex")
for i in allApes:
    print(i)

the_str = "The ape at the apex"
for i in re.finditer("ape.", the_str):
    loc_tuple = i.span()
    print(local_tuple)
    print(the_str[loc_typle[0]:loc_tuple[1]])






