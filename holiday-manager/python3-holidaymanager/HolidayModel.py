#!/usr/bin/python3
import os
import sys
from PySide2 import QtCore, QtGui, QtQml

class HolidayModel(QtCore.QAbstractListModel):

	IdRole= QtCore.Qt.UserRole + 1000
	TypeRole=QtCore.Qt.UserRole+1001
	DescriptionRole=QtCore.Qt.UserRole+1002
		
	def __init__(self,parent=None):
		
		super(HolidayModel, self).__init__(parent)
		self._entries =[]
	
	#def __init__

	def rowCount(self, parent=QtCore.QModelIndex()):
		
		if parent.isValid():
			return 0
		return len(self._entries)

	#def rowCount

	def data(self, index, role=QtCore.Qt.DisplayRole):
		
		if 0 <= index.row() < self.rowCount() and index.isValid():
			item = self._entries[index.row()]
			if role == HolidayModel.IdRole:
				return item["id"]
			elif role == HolidayModel.TypeRole:
				return item["type"]
			elif role == HolidayModel.DescriptionRole:
				return item["description"]
			
	#def data

	def roleNames(self):
		
		roles = dict()
		roles[HolidayModel.IdRole] = b"id"
		roles[HolidayModel.TypeRole] = b"type"
		roles[HolidayModel.DescriptionRole] = b"description"

		return roles

	#def roleNames

	def appendRow(self,i,t,d):
		
		tmpId=[]
		for item in self._entries:
			tmpId.append(item["id"])

		if i not in tmpId:
			self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(),self.rowCount())
			self._entries.append(dict(id=i,type=t,description=d))
			self.endInsertRows()

	#def appendRow

	def removeRow(self,index):

		self.beginRemoveRows(QtCore.QModelIndex(),index,index)
		self._entries.pop(index)
		self.endRemoveRows()
	
	#def removeRow

	def clear(self):
		
		count=self.rowCount()
		self.beginRemoveRows(QtCore.QModelIndex(), 0, count)
		self._entries.clear()
		self.endRemoveRows()
	
	#def clear
	
#class HolidayModel
