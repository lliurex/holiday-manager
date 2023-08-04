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

LOAD_MSG=1
APPLY_CHANGES_MSG=2

class LoadDate(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.newDate=args[0]
		self.dateInfo=args[1]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		Bridge.dateMan.initValues()
		if not self.newDate:
			Bridge.dateMan.loadDateConfig(self.dateInfo)

	#def run

#class LoadBell

class AddDate(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.newDate=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.dateMan.addDate(self.newDate)

	#def run

#class AddDate


class Bridge(QObject):

	def __init__(self,ticket=None):

		QObject.__init__(self)
		Bridge.dateMan=HolidayManager.HolidayManager()
		self._holidayModel=HolidayModel.HolidayModel()
		self._showMainMessage=[False,"","Ok"]
		self._showDateForm=False
		self._closePopUp=[True,""]
		self._dateRangeOption=Bridge.dateMan.dateRangeOption
		self._daysInRange=Bridge.dateMan.daysInRange
		self._dateDescription=Bridge.dateMan.dateDescription
						
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
				self._holidayModel.appendRow(item["id"],item["type"],item["description"])
	
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

	def _getClosePopUp(self):

		return self._closePopUp

	#def _getClosePopUp

	def _setClosePopUp(self,closePopUp):

		if self._closePopUp!=closePopUp:
			self._closePopUp=closePopUp
			self.on_closePopUp.emit()

	#def _setClosePopUp

	def _getDateDescription(self):

		return self._dateDescription

	#def _getDateDescription

	def _setDateDescription(self,dateDescription):

		if self._dateDescription!=dateDescription:
			self._dateDescription=dateDescription
			self.on_dateDescription.emit()

	#def _setDateDescription

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

		self.closePopUp=[False,LOAD_MSG]
		self.newDate=LoadDate(True,"")
		self.newDate.start()
		self.newDate.finished.connect(self._newDateRet)

	#def addNewDate

	def _newDateRet(self):

		self._initializeVars()
		self.closePopUp=[True,""]

	#def _newDateRet

	def _initializeVars(self):

		self.dateRangeOption=Bridge.dateMan.dateRangeOption
		self.daysInRange=Bridge.dateMan.daysInRange
		self.dateDescription=Bridge.dateMan.dateDescription
		self.currentDateConfig=copy.deepcopy(Bridge.dateMan.currentDateConfig)
		self.showDateForm=True

	#def _initializeVars

	@Slot(str)
	def loadDate(self,dateToLoad):

		self.closePopUp=[False,LOAD_MSG]
		self.editDate=LoadDate(False,dateToLoad)
		self.editDate.start()
		self.editDate.finished.connect(self._editDateRet)

	#def loadDate

	def _editDateRet(self):

		self._initializeVars()
		self.closePopUp=[True,""]
		self.showDateForm=True

	#def _editDateRet

	@Slot('QVariantList')
	def applyDateChanges(self,data):

		self.showDateForm=False

		if data!=self.currentDateConfig:
			self.currentDateConfig=data
			self.closePopUp=[False,APPLY_CHANGES_MSG]
			self.saveDate=AddDate(self.currentDateConfig)
			self.saveDate.start()
			self.saveDate.finished.connect(self._saveDateRet)

	#def applyDateChanges

	def _saveDateRet(self):

		if self.saveDate.ret[0]:
			self._updateHolidayModel()
			self.closePopUp=[True,""]
			self.showMainMessage=[True,self.saveDate.ret[1],"Ok"]
		else:
			self.closePopUp=[True,""]
			self.showMainMessage=[True,self.saveDate.ret[1],"Error"]

	#def _saveDataRet

	@Slot()
	def closeDateForm(self):

		self.showDateForm=False

	#def closeDateForm

	on_showMainMessage=Signal()
	showMainMessage=Property('QVariantList',_getShowMainMessage,_setShowMainMessage,notify=on_showMainMessage)

	on_showDateForm=Signal()
	showDateForm=Property(bool,_getShowDateForm,_setShowDateForm,notify=on_showDateForm)

	on_closePopUp=Signal()
	closePopUp=Property('QVariantList',_getClosePopUp,_setClosePopUp,notify=on_closePopUp)

	on_dateDescription=Signal()
	dateDescription=Property(str,_getDateDescription,_setDateDescription,notify=on_dateDescription)

	on_dateRangeOption=Signal()
	dateRangeOption=Property(bool,_getDateRangeOption,_setDateRangeOption,notify=on_dateRangeOption)

	on_daysInRange=Signal()
	daysInRange=Property('QVariantList',_getDaysInRange,_setDaysInRange,notify=on_daysInRange)

	systemLocale=Property(str,_getSystemLocale,constant=True)
	holidayModel=Property(QObject,_getHolidayModel,constant=True)


#clas Bridge



