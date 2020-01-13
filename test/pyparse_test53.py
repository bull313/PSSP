import sys
import math
import random
import threading
import time
import re
import sqlite3
import csv

def printDB():
    try:
        result = theCursor.execute("SELECT id, FName, LName, Age, Address FORM test_table")
        for row in result:
            print("ID: ", row[0])
            print("FName", row[1])
            print("LName", row[2])
            print("Age", row[3])
            print("Address", row[4])
        
    except sqlite3.OperationalError:
        print("The table doesn't exist")
    except:
        print("Couldn't get data")


db_conn = sqlite3.connect('test.db')
print("Database Created")
theCursor = db_conn.cursor()
try:
    db_conn.execute("IM NOT GONNA WRITE THIS WHOLE DB QUERY OUT RN")
    db_conn.commit()
    print("Table Created")
except sqlite3.OperationalError:
    print("Table Not Created")

conn.execute("INSERT INTO blah blah blah")
db_conn.commit()
print_DB()
db_conn.close()




