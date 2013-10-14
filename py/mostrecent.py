#!/usr/bin/python3

import os
import sys
import datetime
import cgitb
cgitb.enable()

SORT_ORDER = {"January":1,
			"February":2,
			"March":3,
			"April":4,
			"May":5,
			"June":6,
			"July":7,
			"August":8,
			"September":9,
			"October":10,
			"November":11,
			"December":12}


d = datetime.date.today()
yr = d.year
cwd = os.getcwd()

bills = []

while not bills:
	try:
		os.chdir(str(yr))
		bills = os.listdir()
	except OSError:
		print("Status: 301")
		print("Location: ../../bad_date.html")
		print()
		sys.exit()
		
	yr -= 1
		

bills[:] = [item.split('.')[0] for item in bills]
bills.sort(key = lambda val: SORT_ORDER[val], reverse=True)

location = (os.sep).join([str(d.year), bills[0]])

print("Status: 200")
print("Content-Type: application/pdf")
print("Location: "+location+".pdf")
print()
