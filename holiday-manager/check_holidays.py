#! /usr/bin/python3

import time
from datetime import date

import n4d.client

class CheckDay(object):

	def __init__(self):

		self.current_day=date.today().strftime('%d/%m/%Y')
		self.n4d=n4d.client.Client()
		self.check_day()

	#def __init__	

	def check_day(self):

		check=self.n4d.HolidayListManager.is_holiday(self.current_day)["status"]
		if check:
			exit(1) 
		else:
			exit(0)

	#def check_day
	
#class CheckDay			

	
testday=CheckDay()			