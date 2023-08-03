#!/usr/bin/env python3

import os
import sys
import time
import shutil
from datetime import datetime, date,timedelta
import copy
import n4d.client


class HolidayManager(object):

	def __init__(self):

		super(HolidayManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.datesConfigData=[]
		self._getSystemLocale()
		self.initValues()

	#def __init__

	def createN4dClient(self,ticket):

		ticket=ticket.replace('##U+0020##',' ')
		tk=n4d.client.Ticket(ticket)
		self.client=n4d.client.Client(ticket=tk)

	#def create_n4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print("[MANAGE HOLIDAYS]: "+ str(function) + str(msg))

	#def _debug

	def _getSystemLocale(self):

		language=os.environ["LANGUAGE"]

		if language!="":
			tmpLang=language.split(":")
			self.systemLocale=tmpLang[0]
		else:
			self.systemLocale=os.environ["LANG"]

	#def _getSystemLocale

	def readConf(self):
		
		self.loadError=False
		result=self.client.HolidayListManager.read_conf()
		self._debug("Read configuration file: ",result)
		self.datesConfig=result["info"]
		self.datesConfigData=[]
		if result["status"]:
			self._getDatesConfig()
		return result

	#def readConf

	def _getDatesConfig(self):

		orderDate=self._getOrderDate()

		for item in orderDate:
			tmp={}
			tmp["id"]=item
			if "-" in item:
				tmp["type"]="range"
			else:
				tmp["type"]="single"
			tmp["comment"]=self.datesConfig[item]["description"]
	
			self.datesConfigData.append(tmp)

	#def _getDatesConfig		

	def _getOrderDate(self):

		tmp=[]
		orderDate=[]

		if len(self.datesConfig)>0:
			for item in self.datesConfig:
				if "-" in item:
					date_toformat=item.split("-")[0]
				else:
					date_toformat=item

				datef=datetime.strptime(date_toformat,"%d/%m/%Y")
				x=()
				x=item,datef
				tmp.append(x)

		tmp.sort(key=lambda date:date[1])
		for item in tmp:
			orderDate.append(item[0])

		return orderDate

	#def _getOrderDate

	def loadDateConfig(self,date):

		self.dateToLoad=date
		self.currentDateConfig=self.datesConfig[self.dateToLoad]
		self.dateInfo=[self.dateToLoad,self.currentDateConfig["description"]]
		self.daysInRange=self.getDaysInRange(self.dateToLoad)
		self.dateRangeOption=self._checkRangeOption(self.dateToLoad)		

	#def loadDateConfig

	def initValues(self):

		self.currentDateConfig={}
		self.dateInfo=["",""]
		self.dateRangeOption=True
		self.daysInRange=[]

	#def initValues

	def getDaysInRange(self,day):	

		listDays=[]
		if day!="":
			if "-" in day:
				tmp=day.split("-")
				date1=datetime.strptime(tmp[0],'%d/%m/%Y')
				date2=datetime.strptime(tmp[1],'%d/%m/%Y')
			else:
				date1=datetime.strptime(day,'%d/%m/%Y')
				date2=date1
			delta=date2-date1
			for i in range(delta.days + 1):
				tmpDay=(date1 + timedelta(days=i)).strftime('%d/%m/%Y')
				listDays.append(tmpDay)

		return listDays	

	#def getDaysInRange

	def _checkRangeOption(self,date):

		if date!="":
			if "-" in date:
				return True
			else:
				return False
		return True

	#def _checkRangeOption
	
	'''
	def add_day(self,day,description):

		
			Format to day arg:
				-day="dd/mm/yyyy"
				-interval="dd/mm/yyyy-dd/mm/yyyy"

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

		
			Format to day arg:
				-day="dd/mm/yyyy"
				-interval="dd/mm/yyyy-dd/mm/yyyy"
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
		

		if os.path.exists(orig_path):
			try:
				f=open(orig_path)
				read=json.load(f)
				if not os.path.exists(self.block_file):
					shutil.copyfile(orig_path,self.config_file)
					f.close()
					return {"status":True,"code":HolidayManager.IMPORT_PROCESS_SUCESSFUL,"info":""}
				else:
					return {"status":False,"code":HolidayManager.IMPORT_BLOCK_ERROR,"info":""}
	
			except Exception as e:
				self._debug("Import holiday list: ",str(e))
				return {"status":False,"code":HolidayManager.IMPORT_PROCESS_ERROR,"info":str(e)}


		return {"status":False,"code":HolidayManager.IMPORT_FILE_EXITS_ERROR,"info":""}
		
	
	#def import_holiday_list
		
	
	def export_holiday_list(self,dest_path):

		try:
			if os.path.exists(self.config_file):
				shutil.copy2(self.config_file,dest_path)
				
				return {"status":True,"code":HolidayManager.EXPORT_PROCESS_SUCCESSFUL,"info":""}

		except Exception as e:		
			self._debug("Export holiday list: ",str(e))
			return {"status":False,"code":HolidayManager.EXPORT_PROCESS_ERROR,"info":str(e)}

			

	#def export_holiday_list
	'''	

#class HolidayManager	