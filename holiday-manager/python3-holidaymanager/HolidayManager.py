#!/usr/bin/env python3

import os
import sys
import time
import shutil
from datetime import datetime, date,timedelta
import copy
import n4d.client


class HolidayManager(object):

	DATES_ALREADY_REMOVED=3
	DATE_EDITED_SUCCESSFULLY=7
	DATE_ADDED_SUCCESSFULLY=5
	DATE_REMOVED_SUCCESSFULLY=11
	DATES_REMOVED_SUCCESSFULLY=12


	def __init__(self):

		super(HolidayManager, self).__init__()

		self.dbg=0
		self.credentials=[]
		self.server='localhost'
		self.datesConfigData=[]
		self.configFile="/etc/manageHolidays/holiday_list"
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
		self._debug("readConf: ",result)
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
			tmp["description"]=self.datesConfig[item]["description"]
	
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
		self.dateRangeOption=self._checkRangeOption(self.dateToLoad)	
		self.daysInRange=self.getDaysInRange(self.dateToLoad)
		self.currentDateConfig=[self.dateToLoad,self.datesConfig[self.dateToLoad]["description"]]
		self.dateDescription=self.currentDateConfig[1]

	#def loadDateConfig

	def initValues(self):

		self.dateRangeOption=True
		self.daysInRange=[]
		self.currentDateConfig=[]
		self.dateDescription=""
		
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

	def checkGlobalOptionsStatus(self):

		if len(self.datesConfig)>0:
			return True
		else:
			return False

	#def checkGlobalOptionsStatus
	
	def addDate(self,newDate):

		ret=True
		action="add"
	
		if len(self.currentDateConfig)>0:
			action="edit"
			if newDate[0]!=self.currentDateConfig[0]:
				retDelete=self.client.HolidayListManager.delete_day(self.currentDateConfig[0])
				self._debug("addDate-delete: ",retDelete)
				if not retDelete['status']:
					ret=False
		if ret:
			retSave=self.client.HolidayListManager.add_day(newDate)
			self._debug("addDate-save: ",retSave)

			if retSave["status"]:
				retReadConfig=self.readConf()
				if retReadConfig['status']:
					if action=="edit":
						return [True,HolidayManager.DATE_EDITED_SUCCESSFULLY]
					else:
						return [True,HolidayManager.DATE_ADDED_SUCCESSFULLY]
				else:
					return [False,retReadConfig["code"]]
			else:
				return [False,retSave["code"]]
			
		else:
			return [False,retDelete["code"]]
	
	#def addDate

	def removeDate(self,allDates,dateToRemove=None):

		if allDates:
			if len(self.datesConfig)>0:
				retRemove=self.client.HolidayListManager.reset_holiday_list()
				self._debug("removeDate-all: ",retRemove)
				if retRemove['status']:
					retReadConfig=self.readConf()
					if retReadConfig["status"]:
						return [True,HolidayManager.DATES_REMOVED_SUCCESSFULLY]
					else:
						return [False,retReadConfig["code"]]
				else:
					return [False, retRemove["code"]]
			else:
				return [True,HolidayManager.DATES_ALREADY_REMOVED]
		else:
			ret=self.client.HolidayListManager.delete_day(dateToRemove)
			self._debug("removeDate: ",ret)

			if ret["status"]:
				retReadConfig=self.readConf()
				if retReadConfig['status']:
					return [True,HolidayManager.DATE_REMOVED_SUCCESSFULLY]
				else:
					return [False,retReadConfig["code"]]
			else:
				return [False,ret["code"]]

	#def removeBell

	def exportDatesConfig(self,destFile):

		user=os.environ["USER"]
		result=self.client.HolidayListManager.export_holiday_list(user,destFile)
		self._debug("exportDatesConfig: ",result)

		return result

	#def exportDatesConfig

	def importDatesConfig(self,origFile):

		resultImport=self.client.HolidayListManager.import_holiday_list(origFile)
		self._debug("importDatesConfig:",resultImport)
		if resultImport['status']:
			retReadConfig=self.readConf()
			if retReadConfig["status"]:
				return [True,resultImport["code"]]
			else:
				return [False,retReadConfig["code"]]
		else:
			return [False,resultImport["code"]]

	#def importDatesConfigs

	
#class HolidayManager	