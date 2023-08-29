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
EXPORT_DATES_CONFIG=3
IMPORT_DATES_CONFIG=4

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

#class LoadDate

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

class RemoveDate(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.allDates=args[0]
		self.dateToRemove=args[1]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.dateMan.removeDate(self.allDates,self.dateToRemove)

	#def run

#class RemoveDate

class GenerateBackup(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.exportPath=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.dateMan.exportDatesConfig(self.exportPath)

	#def run

#class GenerateBackup

class ImportBackup(QThread):

	def __init__(self,*args):

		QThread.__init__(self)
		self.importPath=args[0]
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.ret=Bridge.dateMan.importDatesConfig(self.importPath)

	#def run

#class ImportBackup


class Bridge(QObject):

	def __init__(self,appName=None,ticket=None,):

		QObject.__init__(self)
		Bridge.dateMan=HolidayManager.HolidayManager()
		self._holidayModel=HolidayModel.HolidayModel()
		self._showMainMessage=[False,"","Ok"]
		self._showDateForm=False
		self._closePopUp=[True,""]
		self._dateRangeOption=Bridge.dateMan.dateRangeOption
		self._daysInRange=Bridge.dateMan.daysInRange
		self._dateDescription=Bridge.dateMan.dateDescription
		self._enableGlobalOptions=False
		self._showRemoveDateDialog=[False,False]
		if appName!=None:
			self._appName=appName
		else:
			self._appName="Holiday-Manager"
						
		Bridge.dateMan.createN4dClient(sys.argv[1])

	#def _init__

	def initBridge(self):

		ret=Bridge.dateMan.readConf()
		if ret["status"]:
			self._systemLocale=Bridge.dateMan.systemLocale
			self.enableGlobalOptions=Bridge.dateMan.checkGlobalOptionsStatus()			
			self._updateHolidayModel()
			
		else:
			self.showMainMessage=[True,ret["code"],"Error"]

	#def initBridge

	def _getAppName(self):

		return self._appName

	#def _getAppName

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

	def _getEnableGlobalOptions(self):

		return self._enableGlobalOptions

	#def _getEnableGlobalOptions

	def _setEnableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.on_enableGlobalOptions.emit()

	#def _setEnableGlobalOptions

	def _getShowRemoveDateDialog(self):

		return self._showRemoveDateDialog

	#def _getShowRemoveDateDialog

	def _setShowRemoveDateDialog(self,showRemoveDateDialog):

		if self._showRemoveDateDialog!=showRemoveDateDialog:
			self._showRemoveDateDialog=showRemoveDateDialog
			self.on_showRemoveDateDialog.emit()

	#def _setShowRemoveDateDialog	

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
			self.showMainMessage=[True,self.saveDate.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.saveDate.ret[1],"Error"]

		self.closePopUp=[True,""]
		self.enableGlobalOptions=Bridge.dateMan.checkGlobalOptionsStatus()			

	#def _saveDataRet

	@Slot('QVariantList')
	def removeDate(self,data):

		self.showMainMessage=[False,"","Ok"]
		self.removeAllDates=data[0]
		if self.removeAllDates:
			self.dateToRemove=None
		else:
			self.dateToRemove=data[1]

		self.showRemoveDateDialog=[True,self.removeAllDates]

	#def removeDate

	@Slot(str)
	def manageRemoveDateDialog(self,response):

		self.showRemoveDateDialog=[False,False]
		if response=="Accept":
			self._launchRemoveDateProcess()

	#def manageRemoveDateDialog

	def _launchRemoveDateProcess(self):

		self.closePopUp=[False,APPLY_CHANGES_MSG]

		self.removeDateProcess=RemoveDate(self.removeAllDates,self.dateToRemove)
		self.removeDateProcess.start()
		self.removeDateProcess.finished.connect(self._removeDateProcessRet)

	#def _launchRemoveDateProcess

	def _removeDateProcessRet(self):

		if self.removeDateProcess.ret[0]:
			self._updateHolidayModel()
			self.showMainMessage=[True,self.removeDateProcess.ret[1],"Ok"]
		else:
			self.showMainMessage=[False,self.removeDateProcess.ret[1],"Error"]

		self.enableGlobalOptions=Bridge.dateMan.checkGlobalOptionsStatus()
		self.closePopUp=[True,""]

	#def _removeDateProcessRet	

	@Slot(str)
	def exportDatesConfig(self,exportPath):

		self.showMainMessage=[False,"","Ok"]
		self.closePopUp=[False,EXPORT_DATES_CONFIG]
		self.generateBackup=GenerateBackup(exportPath)
		self.generateBackup.start()
		self.generateBackup.finished.connect(self._exportDatesConfigRet)

	#def exportDatesConfig

	def _exportDatesConfigRet(self):

		if self.generateBackup.ret["status"]:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Ok"]
		else:
			self.showMainMessage=[True,self.generateBackup.ret["code"],"Error"]
		
		self.closePopUp=[True,""]			

	#def _exportDatesConfigRet

	@Slot(str)
	def importDatesConfig(self,importPath):

		self.showMainMessage=[False,"","Ok"]
		self.closePopUp=[False,IMPORT_DATES_CONFIG]
		self.importBackup=ImportBackup(importPath)
		self.importBackup.start()
		self.importBackup.finished.connect(self._importBackupRet)

	#def importDatesConfig

	def _importBackupRet(self):

		if self.importBackup.ret[0]:
			self._updateHolidayModel()
			self.showMainMessage=[True,self.importBackup.ret[1],"Ok"]
		else:
			self.showMainMessage=[True,self.importBackup.ret[1],"Error"]

		self.enableGlobalOptions=Bridge.dateMan.checkGlobalOptionsStatus()			
		self.closePopUp=[True,""]

	#def _importBackupRet

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

	on_enableGlobalOptions=Signal()
	enableGlobalOptions=Property(bool,_getEnableGlobalOptions,_setEnableGlobalOptions,notify=on_enableGlobalOptions)

	on_showRemoveDateDialog=Signal()
	showRemoveDateDialog=Property('QVariantList',_getShowRemoveDateDialog,_setShowRemoveDateDialog,notify=on_showRemoveDateDialog)

	appName=Property(str,_getAppName,constant=True)
	systemLocale=Property(str,_getSystemLocale,constant=True)
	holidayModel=Property(QObject,_getHolidayModel,constant=True)


#clas Bridge



