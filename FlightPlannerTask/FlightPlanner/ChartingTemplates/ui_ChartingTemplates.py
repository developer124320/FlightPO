# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
import  define



class Ui_ChartingTemplates(object):
    def setupUi(self, Form):
        Form.setObjectName(("Form"))
        Form.resize(300, 200)
        font = QtGui.QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)

        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))
        self.vlForm.setSpacing(0)
        self.vlForm.setMargin(0)

        self.gbTemplates = GroupBox(Form)
        self.gbTemplates.Caption = "Available Templates"
        self.vlForm.addWidget(self.gbTemplates)

        self.grid = QtGui.QTableView(self.gbTemplates)
        self.grid.setObjectName("grid")
        self.grid.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.gbTemplates.Add = self.grid

        self.pnlGridButtons = Frame(self.gbTemplates, "HL")
        self.gbTemplates.Add = self.pnlGridButtons

        self.btnAdd = QtGui.QPushButton(self.pnlGridButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setToolTip("Add")
        self.pnlGridButtons.Add = self.btnAdd

        self.btnModify = QtGui.QPushButton(self.pnlGridButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnModify.setIcon(icon)
        self.btnModify.setToolTip("Modify")
        self.pnlGridButtons.Add = self.btnModify

        self.btnRemove = QtGui.QPushButton(self.pnlGridButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemove.setIcon(icon)
        self.btnRemove.setToolTip("Remove")
        self.pnlGridButtons.Add = self.btnRemove

        self.gridModel = QtGui.QStandardItemModel()
        self.gridModel.setHorizontalHeaderLabels(["title", "space", "value"])
        self.grid.setModel(self.gridModel)















