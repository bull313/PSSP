import sys
import math
import random
import threading
import time
from functools import reduce

heroes = {
    "Superman" : "Clark Kent",
    "Batman" : "Bruce Wayne"
}

print("Length", len(herores))
print(herores["Superman"])
heroes["Flash"] = "Barry Allan"
heroes["Flash"] = "Barry Allen"
print(list(heroes.items()))
print(list(heroes.keys()))
print(list(heroes.values()))

del heroes["Flash"]
print(heroes.pop("Batman"))
print("Superman" in heroes)
for k in heroes:
    print(k)

for v in heroes.values():
    print(v)

d1 = { "name" : "Bread", "price" : .88}
print("%(name)s costs $%(price).2f " % d1)