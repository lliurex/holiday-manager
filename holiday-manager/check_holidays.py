#! /usr/bin/python3

import time
from datetime import date

import xmlrpc.client as n4dclient
import ssl


class CheckDay(object):

	def __init__(self):

		self.current_day=date.today().strftime('%d/%m/%Y')
		context=ssl._create_unverified_context()
		self.n4d=n4dclient.ServerProxy("https://localhost:9779",context=context,allow_none=True)
		self.check_day()

	#def __init__	

	def check_day(self):

		#check=self.holidayManager.is_holiday(self.current_day)
		check=self.n4d.is_holiday('','HolidayListManager',self.current_day)["return"]["status"]
		if check:
			exit(1) 
		else:
			exit(0)

	#def check_day
	
#class CheckDay			

	
testday=CheckDay()			