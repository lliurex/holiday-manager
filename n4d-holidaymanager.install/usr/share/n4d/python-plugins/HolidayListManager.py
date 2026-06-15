#!/usr/bin/python3

import os
import subprocess
import n4d.responses
import sys
import json
import shutil
import copy
from datetime import datetime, date,timedelta


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
			with open(self.config_file,'r',encoding="utf-8") as fd:
				self.holiday_list=json.load(fd)
			ret= {"status":True,"code":HolidayListManager.READ_LIST_SUCCESSFUL,"info":self.holiday_list}
		except Exception as e:	
			ret={"status":False,"code":HolidayListManager.READ_LIST_ERROR,"info":self.holiday_list}

		return n4d.responses.build_successful_call_response(ret)

	#def read_conf

	def _create_conf(self,config_folder,file):

		if not os.path.exists(config_folder):
			os.makedirs(config_folder)	

		var={}
		with open(file,'w',encoding="utf-8") as fd:
			json.dump(var,fd,ensure_ascii=False)
	
	#def _create_conf		

	def add_day(self,newDate):
		
		current_list=self.holiday_list.copy()

		tmpDate=newDate.get("value")
		tmpDescription=newDate.get("description")
		current_list[tmpDate]={"description":tmpDescription}

		ret=self._write_conf(current_list)
		
		if ret.get("status"):
			shutil.move(self.block_file,self.config_file)
			
		return n4d.responses.build_successful_call_response(ret)

	#def add_day

	def _write_conf(self,info):
		
		if os.path.exists(self.block_file):
			return {"status":False,"code":HolidayListManager.LIST_BLOCK_ERROR,"info":""}
		
		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)

		try:	
			with open(self.block_file,'w',encoding="utf-8") as fd:
				json.dump(info,fd,ensure_ascii=False)
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

		info.pop(day,None)
	
		ret=self._write_conf(info)

		if ret.get("status"):
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info
		
		return n4d.responses.build_successful_call_response(ret)

	#def delete_day

	def reset_holiday_list(self):
		
		info={}
		
		ret=self._write_conf(info)

		if ret.get("status"):
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info		
		
		return n4d.responses.build_successful_call_response(ret)
	
	#def reset_holiday_list

	def import_holiday_list(self,orig_path):
		
		if not os.path.exists(orig_path):
			ret={"status":False,"code":HolidayListManager.IMPORT_FILE_EXITS_ERROR,"info":""}
			return n4d.responses.build_successful_call_response(ret)

		if os.path.exists(self.block_file):
			ret={"status":False,"code":HolidayListManager.IMPORT_BLOCK_ERROR,"info":""}
			return n4d.responses.build_successful_call_response(ret)

		try:
			with open(orig_path,'r',encoding="utf-8") as fd:
				json.load(fd)

			shutil.copyfile(orig_path,self.config_file)
			ret={"status":True,"code":HolidayListManager.IMPORT_PROCESS_SUCESSFUL,"info":""}

		except Exception as e:
			ret={"status":False,"code":HolidayListManager.IMPORT_PROCESS_ERROR,"info":str(e)}
	
		return n4d.responses.build_successful_call_response(ret)

	#def import_holiday_list	

	def export_holiday_list(self,user,dest_path):

		if not os.path.exists(self.config_file):
			ret={"status":False,"code":HolidayListManager.EXPORT_PROCESS_ERROR,"info":str(e)}
			return n4d.responses.build_successful_call_response(ret)

		try:
			shutil.copy2(self.config_file,dest_path)
			ret={"status":True,"code":HolidayListManager.EXPORT_PROCESS_SUCCESSFUL,"info":""}
		
		except Exception as e:		
			ret={"status":False,"code":HolidayListManager.EXPORT_PROCESS_ERROR,"info":str(e)}
			return n4d.responses.build_successful_call_response(ret)

		if ret.get("status"):
			try:
				subprocess.run(["chown","-R",f"{user}:nogroup",dest_path])
			except subprocess.CalledProcessError as e:
				pass		
		
		return n4d.responses.build_successful_call_response(ret)

	#def export_holiday_list

	def is_holiday(self,day):

		if not getattr(self,'holiday_list',None):
			if os.path.exists(self.config_file):
				try:
					with open(self.config_file,'r',encoding="utf-8") as fd:
						self.holiday_list=json.load(fd)
				except Exception as e:
					self.holiday_list={}
			else:
				self.holiday_list={}

		holiday_days=set()

		for item in self.holiday_list:
			if "-" in item:
				days_inrange=self._get_days_inrange(item)
				holiday_days.update(days_inrange)
			else:
				holiday_days.add(item)

		is_present=day in holiday_days

		ret={
			"status":is_present,
			"code":"",
			"info":""
		}
		
		return n4d.responses.build_successful_call_response(ret)

	#def is_holiday	

	def _get_days_inrange(self,day):	

		if not day:
			return []

		tmpDay=day.split("-")
		date1=datetime.strptime(tmpDay[0],'%d/%m/%Y')
		date2=datetime.strptime(tmpDay[1],'%d/%m/%Y') if len(tmpDay)>1 else date1

		delta=date2-date1

		return [(date1 + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(delta.days + 1)]
	

	#def _get_days_inrange

	def are_days_configured(self):

		are_days=False
		
		if getattr(self,'holiday_list',None):
			are_days=True
		else:
			if os.path.exists(self.config_file):
				try:
					with open(self.config_file,'r') as fd:
						data=json.load(fd)
					
					are_days=bool(data)
				except Exception as e:
					pass

		ret={"status":are_days,"code":"","data":""}

		return n4d.responses.build_successful_call_response(ret)

	#def are_days_configured 	

