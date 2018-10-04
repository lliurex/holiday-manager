#!/usr/bin/env python3

import time
from datetime import date

import holidaymanager.HolidayManager as HolidayManager



class CheckDay(object):

	def __init__(self):
		self.holidayManager=HolidayManager.HolidayManager()
		self.current_day=date.today().strftime('%d/%m/%Y')
		self.check_day()
	#def __init__	

	def check_day(self):

		check=self.holidayManager.is_holiday(self.current_day)
		if check:
			exit(1) 
		else:
			exit(0)

	#def check_day
	
#class CheckDay			

	
testday=CheckDay()			