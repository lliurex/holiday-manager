#!/usr/bin/env python3

import os
import sys
import json
import codecs
import time
import shutil
from datetime import datetime, date,timedelta
import copy


class HolidayManager(object):

	def __init__(self):

		super(HolidayManager, self).__init__()

		self.dbg=0
		self.config_dir=os.path.expanduser("/etc/manageHolidays/")
		self.config_file=os.path.join(self.config_dir,"holiday_list")
		self.block_file=os.path.join(self.config_dir,"holiday_tmp")
		#self.read_conf()

	#def __init__


	def _debug(self,function,msg):

		if self.dbg==1:
			print("[MANAGE HOLIDAYS]: "+ str(function) + str(msg))

	#def _debug		

	def _create_conf(self,config_folder,file):

		if not os.path.exists(config_folder):
			os.makedirs(config_folder)	

		var={}	
		with codecs.open(file,'w',encoding="utf-8") as f:
			json.dump(var,f,ensure_ascii=False)
			f.close()	
	
	#def _create_conf		

	def read_conf(self):
		
		'''
			code=4: Read file correctly
			code=5: Error in read file

		'''
		if not os.path.exists(self.config_file):
			self._create_conf(self.config_dir,self.config_file)

		try:
			f=open(self.config_file)
			self.holiday_list=json.load(f)
			return {"status":True,"code":4,"info":self.holiday_list}
		except Exception as e:	
			self._debug("Read configuration file: ",str(e))
			return {"status":False,"code":5,"info":self.holiday_list}

		f.close()	

	#def read_conf	


	def _write_conf(self,info):
		
		'''
			code=1: Block for another user
			code=2: Correcty write
			code=3: error when write a holiday_list

		'''
		if os.path.exists(self.block_file):
			return {"status":False,"code":1,"info":""}
		else:
			self._create_conf(self.config_dir,self.block_file)
			try:	
				with codecs.open(self.block_file,'w',encoding="utf-8") as f:
					json.dump(info,f,ensure_ascii=False)
					f.close()	
					return {"status":True,"code":2,"info":""}
			except Exception as e:
				self._debug("Write configuration file: ",str(e))
				return {"status":False,"code":3,"info":str(e)}


	#def _write_conf	


	def add_day(self,day,description):

		'''
			Format to day arg:
				-day="dd/mm/yyyy"
				-interval="dd/mm/yyyy-dd/mm/yyyy"
		'''		

		info=self.holiday_list.copy()
		info[day]={}
		info[day]["description"]=description
		
		result=self._write_conf(info)
		
		if result["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info
			
		return result	

	#def add_day

		
	def _get_interval_id(self):

		interval=[]
		for item in self.holiday_list:
			if self.holiday_list[item]["intervalId"]!="":
				interval.append(int(self.holiday_list[item]["intervalId"]))

		if len(interval)>0:
			next_intervalId=max(interval)+1
			
		else:
			next_intervalId=0

		return next_intervalId	

	#def _get_interval_id


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
			self._debug("Delete day: ",str(e))
		pass

		result=self._write_conf(info)

		if result["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info

		return result	
				
	#def delete_day			


	def get_days_inrange(self,day):

		list_days=[]
		tmp=day.split("-")
		date1=datetime.strptime(tmp[0],'%d/%m/%Y')
		date2=datetime.strptime(tmp[1],'%d/%m/%Y')
		delta=date2-date1
		for i in range(delta.days + 1):
			tmp_day=(date1 + timedelta(days=i)).strftime('%d/%m/%Y')
			list_days.append(tmp_day)

		return list_days	

	#def get_days_inrange	

	def is_holiday(self,day):

		holiday_days=[]
		if os.path.exists(self.config_file):
			self.read_conf()

		for item in self.holiday_list:
			tmp_list=[]
			if "-" in item:
				tmp_list=self.get_days_inrange(item)
				holiday_days=holiday_days+tmp_list
			else:
				holiday_days.append(item)


		if day in holiday_days:
			return True
		else:
			return False
				

	#def is_holiday	


	def reset_holiday_list(self):
		
		info={}
		
		result=self._write_conf(info)

		if result["status"]:
			shutil.move(self.block_file,self.config_file)
			self.holiday_list=info

		return result	

	#def reset_holiday_list	


	def import_holiday_list(self,orig_path):
		
		'''
			code=6: Import correctly
			code=7: Block for another user
			code=8: Error in import
			code=9: Orig file not exits
		'''
		if os.path.exists(orig_path):
			try:
				f=open(orig_path)
				read=json.load(f)
				if not os.path.exists(self.block_file):
					shutil.copyfile(orig_path,self.config_file)
					f.close()
					return {"status":True,"code":6,"info":""}
				else:
					return {"status":False,"code":7,"info":""}
	
			except Exception as e:
				self._debug("Import holiday list: ",str(e))
				return {"status":False,"code":8,"info":str(e)}


		return {"status":False,"code":9,"info":""}
		
	
	#def import_holiday_list
		
	
	def export_holiday_list(self,dest_path):

		'''
			code=10: Export correcty
			code=11: Error in export
		'''

		try:
			if os.path.exists(self.config_file):
				shutil.copy2(self.config_file,dest_path)
				
				return {"status":True,"code":10,"info":""}

		except Exception as e:		
			self._debug("Export holiday list: ",str(e))
			return {"status":False,"code":11,"info":str(e)}

			

	#def export_holiday_list	

#Class HolidayManager	