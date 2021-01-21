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
		
		result={}
		ret=self.holidayListManager.read_conf()
		result["code"]=ret["code"]
		result["info"]=ret["info"]
		
		if ret["status"]:
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)


	#def read_conf	

	def add_day(self,day,comment):
		
		result={}
		ret=self.holidayListManager.add_day(day,comment)
		result["code"]=ret["code"]
		result["info"]=ret["info"]
		
		if ret["status"]:
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)

	#def add_day	

	
	def delete_day(self,day):
		
		result={}
		ret=self.holidayListManager.delete_day(day)
		result["code"]=ret["code"]
		result["info"]=ret["info"]
		
		if ret["status"]:
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)
		

	#def delete_day

	def reset_holiday_list(self):
		
		result={}
		ret=self.holidayListManager.reset_holiday_list()
		result["code"]=ret["code"]
		result["info"]=ret["info"]
		
		if ret["status"]:
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)
	
	#def reset_holiday_list

	def import_holiday_list(self,orig_path):
		
		result={}
		ret=self.holidayListManager.import_holiday_list(orig_path)
		result["code"]=ret["code"]
		result["info"]=ret["info"]
		
		if ret["status"]:
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)
			


	#def import_holiday_list	

	def export_holiday_list(self,user,dest_path):

		result={}
		ret=self.holidayListManager.export_holiday_list(dest_path)	
		result["code"]=ret["code"]
		result["info"]=ret["info"]

		if ret['status']:
			cmd='chown -R '+user+":nogroup " + dest_path
			os.system(cmd)
			return n4d.responses.build_successful_call_response(result)
		else:
			return n4d.responses.build_failed_call_response(result)

		
	#def export_holiday_list 	

