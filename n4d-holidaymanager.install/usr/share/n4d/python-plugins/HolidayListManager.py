#!/usr/bin/python3

import os
import n4d.responses
import sys
import json
import codecs
import shutil
import copy

class HolidayListManager:

	LIST_BLOCK_ERROR=-1
	WRITE_LIST_ERROR=-3
	READ_LIST_ERROR=-5
	IMPORT_BLOCK_ERROR=-7
	IMPORT_PROCESS_ERROR=-8
	IMPORT_FILE_EXITS_ERROR=-9
	EXPORT_PROCESS_ERROR=-11

	WRITE_LIST_SUCCESSFUL=2
	READ_LIST_SUCCESSFUL=4
	IMPORT_PROCESS_SUCESSFUL=6
	EXPORT_PROCESS_SUCCESSFUL=10
	
	def __init__(self):

		self.config_dir=os.path.expanduser("/etc/manageHolidays/")
		self.config_file=os.path.join(self.config_dir,"holiday_list")
		self.block_file=os.path.join(self.config_dir,"holiday_tmp")
		self.holiday_list={}

	#def __init__	

	def read_conf(self):
		
		if not os.path.exists(self.config_file):
			self._create_conf(self.config_dir,self.config_file)

		try:
			f=open(self.config_file)
			self.holiday_list=json.load(f)
			ret= {"status":True,"code":HolidayListManager.READ_LIST_SUCCESSFUL,"info":self.holiday_list}
		except Exception as e:	
			ret={"status":False,"code":HolidayListManager.READ_LIST_ERROR,"info":self.holiday_list}

		f.close()			
		
		return n4d.responses.build_successful_call_response(ret)

	#def read_conf

	def _create_conf(self,config_folder,file):

		if not os.path.exists(config_folder):
			os.makedirs(config_folder)	

		var={}	
		with codecs.open(file,'w',encoding="utf-8") as f:
			json.dump(var,f,ensure_ascii=False)
			f.close()	
	
	#def _create_conf		

	def add_day(self,day,comment):
		
		'''
			Format to day arg:
				-day="dd/mm/yyyy"
				-interval="dd/mm/yyyy-dd/mm/yyyy"
		'''		

		info=self.holiday_list.copy()
		info[day]={}
		info[day]["description"]=comment
		
		ret=self._write_conf(info)
		
		if ret["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info
			
		return n4d.responses.build_successful_call_response(ret)

	#def add_day

	def _write_conf(self,info):
		
		if os.path.exists(self.block_file):
			return {"status":False,"code":HolidayListManager.LIST_BLOCK_ERROR,"info":""}
		else:
			self._create_conf(self.config_dir,self.block_file)
			try:	
				with codecs.open(self.block_file,'w',encoding="utf-8") as f:
					json.dump(info,f,ensure_ascii=False)
					f.close()	
					return {"status":True,"code":HolidayListManager.WRITE_LIST_SUCCESSFUL,"info":""}
			except Exception as e:
				return {"status":False,"code":HolidayListManager.WRITE_LIST_ERROR,"info":str(e)}

	#def _write_conf		

	
	def delete_day(self,day):
		
		'''
			Format to day arg:
				-day="dd/mm/yyyy"
				-interval="dd/mm/yyyy-dd/mm/yyyy"
		'''	
		info=self.holiday_list.copy()

		try:
			info.pop(day)
		except Exception as e:
			pass

		ret=self._write_conf(info)

		if ret["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info
		
		return n4d.responses.build_successful_call_response(ret)

	#def delete_day

	def reset_holiday_list(self):
		
		info={}
		
		ret=self._write_conf(info)

		if ret["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info		
		
		return n4d.responses.build_successful_call_response(ret)
	
	#def reset_holiday_list

	def import_holiday_list(self,orig_path):
		
		if os.path.exists(orig_path):
			try:
				f=open(orig_path)
				read=json.load(f)
				if not os.path.exists(self.block_file):
					shutil.copyfile(orig_path,self.config_file)
					f.close()
					ret={"status":True,"code":HolidayListManager.IMPORT_PROCESS_SUCESSFUL,"info":""}
				else:
					ret={"status":False,"code":HolidayListManager.IMPORT_BLOCK_ERROR,"info":""}
	
			except Exception as e:
				ret={"status":False,"code":HolidayListManager.IMPORT_PROCESS_ERROR,"info":str(e)}

		ret={"status":False,"code":HolidayListManager.IMPORT_FILE_EXITS_ERROR,"info":""}
		
		return n4d.responses.build_successful_call_response(ret)
			

	#def import_holiday_list	

	def export_holiday_list(self,user,dest_path):

		try:
			if os.path.exists(self.config_file):
				shutil.copy2(self.config_file,dest_path)
				
				ret={"status":True,"code":HolidayListManager.EXPORT_PROCESS_SUCCESSFUL,"info":""}

		except Exception as e:		
			ret={"status":False,"code":HolidayListManager.EXPORT_PROCESS_ERROR,"info":str(e)}

		if ret['status']:
			cmd='chown -R '+user+":nogroup " + dest_path
			os.system(cmd)
		
		return n4d.responses.build_successful_call_response(ret)

	#def export_holiday_list 	

