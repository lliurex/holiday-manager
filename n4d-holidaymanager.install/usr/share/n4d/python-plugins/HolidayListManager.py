 
import os
import imp
holidayManager=imp.load_source("HolidayManager","/usr/lib/python3/dist-packages/holidaymanager/HolidayManager.py")



class HolidayListManager(object):

	def __init__(self):

		self.holidayListManager=holidayManager.HolidayManager()
		
	#def __init__	


	def read_conf(self):
		
		result=self.holidayListManager.read_conf()
		return result

	#def read_conf	

	def add_day(self,day,comment):
		
		result=self.holidayListManager.add_day(day,comment)
		return result

	#def add_day	

	
	def delete_day(self,day):
		
		result=self.holidayListManager.delete_day(day)
		return result		

	#def delete_day

	def reset_holiday_list(self):

		result=self.holidayListManager.reset_holiday_list()
		return result

	#def reset_holiday_list

	def import_holiday_list(self,orig_path):
	
		result=self.holidayListManager.import_holiday_list(orig_path)
		return result

	#def import_holiday_list	

	def export_holiday_list(self,user,dest_path):

		result=self.holidayListManager.export_holiday_list(dest_path)	
		if result['status']:
			cmd='chown -R '+user+":nogroup " + dest_path
			os.system(cmd)
			
		return result

	#def export_holiday_list 	

