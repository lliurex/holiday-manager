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

	dateLoaded=Signal()

	def __init__(self,manager,newDate,dateToLoad):

		super().__init__()
		self.manager=manager
		self.newDate=newDate
		self.dateToLoad=dateToLoad

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		self.manager.initValues()
		if not self.newDate:
			self.manager.loadDateConfig(self.dateToLoad)

		self.dateLoaded.emit()

	#def run

#class LoadDate

class SaveDate(QThread):

	dateSaved=Signal(dict)

	def __init__(self,manager,infoToSave):

		super().__init__()
		self.manager=manager
		self.infoToSave=infoToSave

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=self.manager.addDate(self.infoToSave)
		self.dateSaved.emit(ret)

	#def run

#class SaveDate

class RemoveDate(QThread):

	dateRemoved=Signal(dict)

	def __init__(self,manager,removeAll,dateToRemove):

		super().__init__()
		self.manager=manager
		self.allDates=removeAll
		self.dateToRemove=dateToRemove

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=self.manager.removeDate(self.allDates,self.dateToRemove)
		self.dateRemoved.emit(ret)
	
	#def run

#class RemoveDate

class GenerateBackup(QThread):

	backupGenerated=Signal(dict)

	def __init__(self,manager,exportPath):

		super().__init__()
		self.manager=manager
		self.exportPath=exportPath
		self.ret=[]

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=self.manager.exportDatesConfig(self.exportPath)
		self.backupGenerated.emit(ret)

	#def run

#class GenerateBackup

class ImportBackup(QThread):

	backupImported=Signal(dict)

	def __init__(self,manager,importPath):

		super().__init__()
		self.manager=manager
		self.importPath=importPath

	#def __init__

	def run(self,*args):

		time.sleep(0.5)
		ret=self.manager.importDatesConfig(self.importPath)
		self.backupImported.emit(ret)

	#def run

#class ImportBackup

class Bridge(QObject):

	showMainMessageChanged=Signal()
	showDateFormChanged=Signal()
	showPopUpChanged=Signal()
	dateToLoadChanged=Signal()
	enableGlobalOptionsChanged=Signal()
	showRemoveDateDialogChanged=Signal()

	def __init__(self,appName=None,ticket=None,):

		QObject.__init__(self)
		self.holidayManager=HolidayManager.HolidayManager()
		self._holidayModel=HolidayModel.HolidayModel()
		self._showMainMessage={"show":False,"msgCode":"","type":""}
		self._showDateForm=False
		self._showPopUp={"show":False,"msgCode":""}
		self._dateToLoad=self.holidayManager.dateToLoad
		self._enableGlobalOptions=False
		self._showRemoveDateDialog={"show":False,"removeAll":False}
		
		if appName!=None:
			self._appName=appName
		else:
			self._appName="Holiday-Manager"
						
		self.holidayManager.createN4dClient(sys.argv[1])

	#def _init__

	@Property('QVariant',notify=showMainMessageChanged)
	def showMainMessage(self):

		return self._showMainMessage

	#def showMainMessage

	@showMainMessage.setter
	def showMainMessage(self,showMainMessage):

		if self._showMainMessage!=showMainMessage:
			self._showMainMessage=showMainMessage
			self.showMainMessageChanged.emit()

	#def showMainMessage

	@Property(bool,notify=showDateFormChanged)
	def showDateForm(self):

		return self._showDateForm

	#def showDateForm

	@showDateForm.setter
	def showDateForm(self,showDateForm):

		if self._showDateForm!=showDateForm:
			self._showDateForm=showDateForm
			self.showDateFormChanged.emit()

	#def showDateForm

	@Property('QVariant',notify=showPopUpChanged)
	def showPopUp(self):

		return self._showPopUp

	#def _showPopUp

	@showPopUp.setter
	def showPopUp(self,showPopUp):

		if self._showPopUp!=showPopUp:
			self._showPopUp=showPopUp
			self.showPopUpChanged.emit()

	#def _showPopUp

	@Property('QVariant',notify=dateToLoadChanged)
	def dateToLoad(self):

		return self._dateToLoad

	#def dateToLoad

	@dateToLoad.setter
	def dateToLoad(self,dateToLoad):

		if self._dateToLoad!=dateToLoad:
			self._dateToLoad=dateToLoad
			self.dateToLoadChanged.emit()

	#def dateToLoad
	
	@Property(bool,notify=enableGlobalOptionsChanged)
	def enableGlobalOptions(self):

		return self._enableGlobalOptions

	#def enableGlobalOptions

	@enableGlobalOptions.setter
	def enableGlobalOptions(self,enableGlobalOptions):

		if self._enableGlobalOptions!=enableGlobalOptions:
			self._enableGlobalOptions=enableGlobalOptions
			self.enableGlobalOptionsChanged.emit()

	#def enableGlobalOptions

	@Property('QVariant',notify=showRemoveDateDialogChanged)
	def showRemoveDateDialog(self):

		return self._showRemoveDateDialog

	#def showRemoveDateDialog

	@showRemoveDateDialog.setter
	def showRemoveDateDialog(self,showRemoveDateDialog):

		if self._showRemoveDateDialog!=showRemoveDateDialog:
			self._showRemoveDateDialog=showRemoveDateDialog
			self.showRemoveDateDialogChanged.emit()

	#def showRemoveDateDialog

	def _getAppName(self):

		return self._appName

	#def _getAppName

	def _getSystemLocale(self):

		return self._systemLocale

	#def _getSystemLocale

	def _getHolidayModel(self):

		return self._holidayModel

	#def _getHolidayModel	

	def initBridge(self):

		ret=self.holidayManager.readConf()
		if not ret.get("status"):
			self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		else:
			self._systemLocale=self.holidayManager.systemLocale
			self.enableGlobalOptions=self.holidayManager.checkGlobalOptionsStatus()			
			self._updateHolidayModel()
			
	#def initBridge
	
	def _updateHolidayModel(self):

		ret=self._holidayModel.clear()
		datesEntries=self.holidayManager.datesConfigData

		for item in datesEntries:
			if item["id"]!="":
				self._holidayModel.appendRow(item["id"],item["type"],item["description"])
	
	#def _updateHolidayModel

	@Slot()
	def addNewDate(self):

		self.showPopUp={"show":True,"msgCode":LOAD_MSG}
		self.newDateT=LoadDate(self.holidayManager,True,"")
		self.newDateT.start()
		self.newDateT.dateLoaded.connect(self._loadDateRet)
		self.newDateT.finished.connect(self.newDateT.deleteLater)

	#def addNewDate

	@Slot(str)
	def loadDate(self,dateToLoad):

		self.showPopUp={"show":True,"msgCode":LOAD_MSG}
		self.editDateT=LoadDate(self.holidayManager,False,dateToLoad)
		self.editDateT.start()
		self.editDateT.dateLoaded.connect(self._loadDateRet)
		self.editDateT.finished.connect(self.editDateT.deleteLater)

	#def loadDate

	def _loadDateRet(self):

		self._initializeVars()
		self.showPopUp={"show":False,"msgCode":""}

	#def _loadDateRet

	def _initializeVars(self):

		self.dateToLoad=self.holidayManager.dateToLoad
		self.currentDateConfig=copy.deepcopy(self.holidayManager.currentDateConfig)
		self.showDateForm=True

	#def _initializeVars

	@Slot('QJSValue')
	def applyDateChanges(self,data):

		if hasattr(data,'toVariant'):
			data=data.toVariant()
				
		self.showDateForm=False

		if data!=self.currentDateConfig:
			self.currentDateConfig=data
			self.showPopUp={"show":True,"msgCode":APPLY_CHANGES_MSG}
			self.saveDateT=SaveDate(self.holidayManager,self.currentDateConfig)
			self.saveDateT.start()
			self.saveDateT.dateSaved.connect(self._saveDateRet)
			self.saveDateT.finished.connect(self.saveDateT.deleteLater)

	#def applyDateChanges

	@Slot(dict)
	def _saveDateRet(self,ret):

		if ret.get("status"):
			self._updateHolidayModel()
		
		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.showPopUp={"show":False,"msgCode":""}
		self.enableGlobalOptions=self.holidayManager.checkGlobalOptionsStatus()			

	#def _saveDataRet

	@Slot('QJSValue')
	def removeDate(self,data):

		if hasattr(data,'toVariant'):
			data=data.toVariant()

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		self.removeAllDates=data.get("removeAll")

		if self.removeAllDates:
			self.dateToRemove=None
		else:
			self.dateToRemove=data.get("dateToRemove")

		self.showRemoveDateDialog={"show":True,"removeAll":self.removeAllDates}

	#def removeDate

	@Slot(str)
	def manageRemoveDateDialog(self,response):

		self.showRemoveDateDialog={"show":False,"removeAll":False}
		if response=="Accept":
			self._launchRemoveDateProcess()

	#def manageRemoveDateDialog

	def _launchRemoveDateProcess(self):

		self.showPopUp={"show":True,"msgCode":APPLY_CHANGES_MSG}

		self.removeDateProcessT=RemoveDate(self.holidayManager, self.removeAllDates,self.dateToRemove)
		self.removeDateProcessT.start()
		self.removeDateProcessT.dateRemoved.connect(self._removeDateProcessRet)
		self.removeDateProcessT.finished.connect(self.removeDateProcessT.deleteLater)

	#def _launchRemoveDateProcess

	@Slot(dict)
	def _removeDateProcessRet(self,ret):

		if ret.get("status"):
			self._updateHolidayModel()
		
		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.enableGlobalOptions=self.holidayManager.checkGlobalOptionsStatus()
		self.showPopUp={"show":False,"msgCode":""}

	#def _removeDateProcessRet	

	@Slot(str)
	def exportDatesConfig(self,exportPath):

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		self.showPopUp={"show":True,"msgCode":EXPORT_DATES_CONFIG}
		self.generateBackupT=GenerateBackup(self.holidayManager,exportPath)
		self.generateBackupT.start()
		self.generateBackupT.backupGenerated.connect(self._generateBackupRet)
		self.generateBackupT.finished.connect(self.generateBackupT.deleteLater)

	#def exportDatesConfig

	@Slot(dict)
	def _generateBackupRet(self,ret):

		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.showPopUp={"show":False,"msgCode":""}			

	#def _exportDatesConfigRet

	@Slot(str)
	def importDatesConfig(self,importPath):

		self.showMainMessage={"show":False,"msgCode":"","type":""}
		self.showPopUp={"show":True,"msgCode":IMPORT_DATES_CONFIG}
		self.importBackupT=ImportBackup(self.holidayManager,importPath)
		self.importBackupT.start()
		self.importBackupT.backupImported.connect(self._importBackupRet)
		self.importBackupT.finished.connect(self.importBackupT.deleteLater)

	#def importDatesConfig

	@Slot(dict)
	def _importBackupRet(self,ret):

		if ret.get("status"):
			self._updateHolidayModel()
		
		self.showMainMessage={"show":True,"msgCode":ret.get("code"),"type":ret.get("type")}
		self.enableGlobalOptions=self.holidayManager.checkGlobalOptionsStatus()			
		self.showPopUp={"show":False,"msgCode":""}

	#def _importBackupRet

	@Slot()
	def closeDateForm(self):

		self.showDateForm=False

	#def closeDateForm

	appName=Property(str,_getAppName,constant=True)
	systemLocale=Property(str,_getSystemLocale,constant=True)
	holidayModel=Property(QObject,_getHolidayModel,constant=True)

#clas Bridge



