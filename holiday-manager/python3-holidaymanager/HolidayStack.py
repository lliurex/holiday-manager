from PySide2.QtCore import QObject,Signal,Slot,QThread,Property,QTimer,Qt,QModelIndex
import os 
import sys
import threading
import time
import copy

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from . import HolidayModel
from . import HolidayManager

class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)
		Bridge.dateMan=HolidayManager.HolidayManager()
		self._holidayModel=HolidayModel.HolidayModel()
		self._showMainMessage=[False,"","Ok"]
		self._showDateForm=False
		self._dateInfo=["",""]
		self._dateRangeOption=True
		self._daysInRange=[]
	
		Bridge.dateMan.createN4dClient(sys.argv[1])

	#def _init__

	def initBridge(self):

		ret=Bridge.dateMan.readConf()
		if ret["status"]:
			self._systemLocale=Bridge.dateMan.systemLocale
			self._updateHolidayModel()
		else:
			self.showMainMessage=[True,ret["code"],"Error"]

	#def initBridge

	def _getHolidayModel(self):

		return self._holidayModel

	#def _getHolidayModel

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

	def _updateHolidayModel(self):

		ret=self._holidayModel.clear()
		datesEntries=Bridge.dateMan.datesConfigData
		for item in datesEntries:
			if item["id"]!="":
				self._holidayModel.appendRow(item["id"],item["type"],item["comment"])
	
	#def _updateHolidayModel

	def _getShowMainMessage(self):

		return self._showMainMessage

	#def _getShowMainMessage

	def _setShowMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.on_showMainMessage.emit()

	#def _setShowMainMessage

	def _getShowDateForm(self):

		return self._showDateForm

	#def _getShowDateForm

	def _setShowDateForm(self,showDateForm):

		if self._showDateForm!=showDateForm:
			self._showDateForm=showDateForm
			self.on_showDateForm.emit()

	#def _setShowDateForm

	def _getDateInfo(self):

		return self._dateInfo

	#def _getDateInfo

	def _setDateInfo(self,dateInfo):

		if self._dateInfo!=dateInfo:
			self._dateInfo=dateInfo
			self.on_dateInfo.emit()

	#def _setDateInfo

	def _getDateRangeOption(self):

		return self._dateRangeOption

	#def _getDateRangeOption

	def _setDateRangeOption(self,dateRangeOption):

		if self._dateRangeOption!=dateRangeOption:
			self._dateRangeOption=dateRangeOption
			self.on_dateRangeOption.emit()

	#def _setDateRangeOption

	def _getDaysInRange(self):

		return self._daysInRange

	#def _getDaysInRange

	def _setDaysInRange(self,daysInRange):

		if self._daysInRange!=daysInRange:
			self._daysInRange=daysInRange
			self.on_daysInRange.emit()

	#def _setDaysInRange 

	@Slot()
	def addNewDate(self):

		Bridge.dateMan.initValues()
		self.currentDateConfig=copy.deepcopy(Bridge.dateMan.currentDateConfig)
		self._initializeVars()
		print(self.daysInRange)
		print(self.dateRangeOption)
		self.showDateForm=True

	#def addNewDate

	def _initializeVars(self):

		self.dateInfo=Bridge.dateMan.dateInfo
		self.dateRangeOption=Bridge.dateMan.dateRangeOption
		self.daysInRange=Bridge.dateMan.daysInRange

	#def _initializeVars

	@Slot(str)
	def loadDate(self,date):

		Bridge.dateMan.initValues()
		Bridge.dateMan.loadDateConfig(date)
		self._initializeVars()
		self.showDateForm=True

	#def loadDate

	@Slot('QVariantList')
	def applyDateChanges(self,data):

		self.showDateForm=False

	#def applyDateChanges

	@Slot()
	def closeDateForm(self):

		self.showDateForm=False

	#def closeDateForm

	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage,notify=on_showMainMessage)

	on_showDateForm=Signal()
	showDateForm=Property(bool,_getShowDateForm,_setShowDateForm,notify=on_showDateForm)

	on_dateInfo=Signal()
	dateInfo=Property('QVariantList',_getDateInfo,_setDateInfo,notify=on_dateInfo)

	on_dateRangeOption=Signal()
	dateRangeOption=Property(bool,_getDateRangeOption,_setDateRangeOption,notify=on_dateRangeOption)

	on_daysInRange=Signal()
	daysInRange=Property('QVariantList',_getDaysInRange,_setDaysInRange,notify=on_daysInRange)

	systemLocale=Property(str,_getSystemLocale,constant=True)
	holidayModel=Property(QObject,_getHolidayModel,constant=True)


#clas Bridge



