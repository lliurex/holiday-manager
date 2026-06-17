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

	KIRIGAMI_MSG_OK=0
	KIRIGAMI_MSG_ERROR=1
	KIRIGAMI_MSG_WARNING=2
	KIRIGAMI_MSG_INFO=3


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
		self.client=n4d.client.Client(ticket=tk,timeout=120)

	#def create_n4dClient

	def _debug(self,function,msg):

		if self.dbg==1:
			print(f"[MANAGE HOLIDAYS]: {function} {msg}")

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
		self.datesConfig=result.get("info",{})
		self.datesConfigData=[]
		
		if result.get("status"):
			result["type"]=HolidayManager.KIRIGAMI_MSG_OK
			self._getDatesConfig()
		else:
			result["type"]=HolidayManager.KIRIGAMI_MSG_ERROR

		return result

	#def readConf

	def _getDatesConfig(self):

		orderDate=self._getOrderDate()

		for item in orderDate:
			tmp={
				"id":item,
				"type":"range" if "-" in item else "single",
				"description":self.datesConfig.get(item).get("description")
			}

			self.datesConfigData.append(tmp)

	#def _getDatesConfig		

	def _getOrderDate(self):

		return sorted(
			self.datesConfig.keys(),
			key=lambda item:datetime.strptime(item.split("-")[0],"%d/%m/%Y")
			)
		
	#def _getOrderDate

	def loadDateConfig(self,date):

		self.dateToLoad={
			"id":date,
			"rangeOption":self._checkRangeOption(date),
			"daysInRange":self.getDaysInRange(date),
			"description":self.datesConfig.get(date).get("description")
		}

		self.currentDateConfig={
			"value":date,
			"description":self.dateToLoad.get("description")
		}

	#def loadDateConfig

	def initValues(self):

		self.dateToLoad={
			"id":"",
			"rangeOption":True,
			"daysInRange":[],
			"description":""
		}

		self.currentDateConfig={
			"value":self.dateToLoad.get("id"),
			"description":self.dateToLoad.get("description")
		}
		
	#def initValues

	def getDaysInRange(self,day):	

		if not day:
			return []

		tmpDay=day.split("-")
		date1=datetime.strptime(tmpDay[0],'%d/%m/%Y')
		date2=datetime.strptime(tmpDay[1],'%d/%m/%Y') if len(tmpDay)>1 else date1

		delta=date2-date1

		return [(date1 + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(delta.days + 1)]
	
		#def getDaysInRange

	def _checkRangeOption(self,date):

		return not date or "-" in date
		
	#def _checkRangeOption

	def checkGlobalOptionsStatus(self):

		return bool(self.datesConfig)

	#def checkGlobalOptionsStatus
	
	def addDate(self,newDate):

		action="add"
	
		if len(self.currentDateConfig.get("value"))>0:
			action="edit"
			if newDate.get("value")!=self.currentDateConfig.get("value"):
				retDelete=self.client.HolidayListManager.delete_day(self.currentDateConfig.get("value"))
				self._debug("addDate-delete: ",retDelete)
				if not retDelete.get("status"):
					return {"status":False,"code":retDelete.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}
		
		retSave=self.client.HolidayListManager.add_day(newDate)
		self._debug("addDate-save: ",retSave)

		if not retSave.get("status"):
			return {"status":False,"code":retSave.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}
		
		retReadConfig=self.readConf()

		if not retReadConfig.get("status"):
			return {"status":False,"code":retReadConfig["code"],"type":HolidayManager.KIRIGAMI_MSG_ERROR}

		if action=="edit":
			return {"status":True,"code":HolidayManager.DATE_EDITED_SUCCESSFULLY,"type":HolidayManager.KIRIGAMI_MSG_OK}
		
		return {"status":True,"code":HolidayManager.DATE_ADDED_SUCCESSFULLY,"type":HolidayManager.KIRIGAMI_MSG_OK}
			
	#def addDate

	def removeDate(self,allDates,dateToRemove=None):

		if allDates:
			if not self.datesConfig:
				return {"status":True,"code":HolidayManager.DATES_ALREADY_REMOVED,"type":HolidayManager.KIRIGAMI_MSG_OK}

			retRemove=self.client.HolidayListManager.reset_holiday_list()
			self._debug("removeDate-all: ",retRemove)
			msgOK=HolidayManager.DATES_REMOVED_SUCCESSFULLY
		else:
			retRemove=self.client.HolidayListManager.delete_day(dateToRemove)
			self._debug("removeDate: ",retRemove)
			msgOK=HolidayManager.DATE_REMOVED_SUCCESSFULLY

		if not retRemove.get("status"):
			return {"status":False,"code":retRemove.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}

		retReadConfig=self.readConf()
		if not retReadConfig.get("status"):
			return {"status":False,"code":retReadConfig.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}

		return {"status":True,"code":msgOK,"type":HolidayManager.KIRIGAMI_MSG_OK}
	
	#def removeBell

	def exportDatesConfig(self,destFile):

		user=os.environ["USER"]
		result=self.client.HolidayListManager.export_holiday_list(user,destFile)
		self._debug("exportDatesConfig: ",result)

		result["type"]=HolidayManager.KIRIGAMI_MSG_OK if result.get("status") else HolidayManager.KIRIGAMI_MSG_ERROR
		
		return result

	#def exportDatesConfig

	def importDatesConfig(self,origFile):

		resultImport=self.client.HolidayListManager.import_holiday_list(origFile)
		self._debug("importDatesConfig:",resultImport)
		
		if not resultImport.get('status'):
			return {"status":False,"code":resultImport.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}
		
		retReadConfig=self.readConf()
		if not retReadConfig.get("status"):
			return {"status":False,"code":retReadConfig.get("code"),"type":HolidayManager.KIRIGAMI_MSG_ERROR}

		return {"status":True,"code":resultImport.get("code"),"type":HolidayManager.KIRIGAMI_MSG_OK}
	
	#def importDatesConfigs

	
#class HolidayManager	
