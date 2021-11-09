#!/usr/bin/python3

import importlib.machinery
import os
holidayManager=importlib.machinery.SourceFileLoader("HolidayManager.py","/usr/lib/python3/dist-packages/holidaymanager/HolidayManager.py").load_module()

import n4d.responses


class HolidayListManager:

	def __init__(self):

		self.holidayListManager=holidayManager.HolidayManager()
		
	#def __init__	


	def read_conf(self):
		
		ret=self.holidayListManager.read_conf()
		
		return n4d.responses.build_successful_call_response(ret)


	#def read_conf	

	def add_day(self,day,comment):
		
		ret=self.holidayListManager.add_day(day,comment)
		
		return n4d.responses.build_successful_call_response(ret)

	#def add_day	

	
	def delete_day(self,day):
		
		ret=self.holidayListManager.delete_day(day)
		
		return n4d.responses.build_successful_call_response(ret)
		

	#def delete_day

	def reset_holiday_list(self):
		
		ret=self.holidayListManager.reset_holiday_list()
		
		return n4d.responses.build_successful_call_response(ret)
	
	#def reset_holiday_list

	def import_holiday_list(self,orig_path):
		
		ret=self.holidayListManager.import_holiday_list(orig_path)
		
		return n4d.responses.build_successful_call_response(ret)
			

	#def import_holiday_list	

	def export_holiday_list(self,user,dest_path):

		ret=self.holidayListManager.export_holiday_list(dest_path)
		if ret['status']:
			cmd='chown -R '+user+":nogroup " + dest_path
			os.system(cmd)
		
		return n4d.responses.build_successful_call_response(ret)

		
	#def export_holiday_list 	

