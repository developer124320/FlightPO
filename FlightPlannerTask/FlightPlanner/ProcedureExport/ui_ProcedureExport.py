# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRnav.ui'
#
# Created: Wed Nov 25 16:19:08 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.StandardItemModel import StandardItemModel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame



class Ui_ProcedureExport(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(473, 580)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.vlForm = QtGui.QVBoxLayout(Form)
        self.vlForm.setObjectName(("vlForm"))

        self.gbFile = GroupBox(Form)
        self.gbFile.Title = "Database File"
        self.vlForm.addWidget(self.gbFile)

        self.pnlFile = TextBoxPanel(self.gbFile)
        self.pnlFile.Caption = ""
        self.pnlFile.LabelWidth = 0
        self.pnlFile.textBox.setMaximumWidth(100000)
        self.pnlFile.hLayoutBoxPanel.removeItem(self.pnlFile.spacerItem)
        self.pnlFile.Button = "openData.png"
        self.gbFile.Add = self.pnlFile

        self.lblEffectiveDate = QtGui.QLabel(self.gbFile)
        self.lblEffectiveDate.setText("Effective Date")
        self.lblEffectiveDate.setObjectName("lblEffectiveDate")
        self.gbFile.Add = self.lblEffectiveDate

        self.gbContent = GroupBox(Form)
        self.gbContent.Title = "Procedures"
        self.vlForm.addWidget(self.gbContent)

        self.tabControl = QtGui.QTabWidget(Form)
        self.tabControl.setObjectName(("tabControl"))

        self.tabSIDs = QtGui.QWidget(Form)
        self.tabSIDs.setObjectName(("tabSIDs"))
        self.vl_tabSIDs = QtGui.QVBoxLayout(self.tabSIDs)
        self.vl_tabSIDs.setObjectName("vl_tabSIDs")
        self.tabControl.addTab(self.tabSIDs, ("SIDs"))

        self.tabSTARs = QtGui.QWidget(Form)
        self.tabSTARs.setObjectName(("tabSTARs"))
        self.vl_tabSTARs = QtGui.QVBoxLayout(self.tabSTARs)
        self.vl_tabSTARs.setObjectName("vl_tabSTARs")
        self.tabControl.addTab(self.tabSTARs, ("STARs"))

        self.tabIAPs = QtGui.QWidget(Form)
        self.tabIAPs.setObjectName(("tabIAPs"))
        self.vl_tabIAPs = QtGui.QVBoxLayout(self.tabIAPs)
        self.vl_tabIAPs.setObjectName("vl_tabIAPs")
        self.tabControl.addTab(self.tabIAPs, ("IAPs"))

        self.tabHoldings = QtGui.QWidget(Form)
        self.tabHoldings.setObjectName(("tabHoldings"))
        self.vl_tabHoldings = QtGui.QVBoxLayout(self.tabHoldings)
        self.vl_tabHoldings.setObjectName("vl_tabHoldings")
        self.tabControl.addTab(self.tabHoldings, ("Holdings"))
        self.gbContent.Add = self.tabControl

        self.splitContainer = Frame(self.tabSIDs)
        self.vl_tabSIDs.addWidget(self.splitContainer)
        p1 = Frame(self.splitContainer, "HL")
        self.splitContainer.Add = p1
        p2 = Frame(self.splitContainer, "HL")
        self.splitContainer.Add = p2

        self.pnlProcButtons = Frame(p1)
        

        self.btnProcAdd = QtGui.QPushButton(self.pnlProcButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnProcAdd.setIcon(icon)
        self.btnProcAdd.setToolTip("Add")
        self.pnlProcButtons.Add = self.btnProcAdd

        self.btnProcEdit = QtGui.QPushButton(self.pnlProcButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnProcEdit.setIcon(icon)
        self.btnProcEdit.setToolTip("Modify")
        self.pnlProcButtons.Add = self.btnProcEdit

        self.btnProcRemove = QtGui.QPushButton(self.pnlProcButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnProcRemove.setIcon(icon)
        self.btnProcRemove.setToolTip("Remove")
        self.pnlProcButtons.Add = self.btnProcRemove

        self.gridProcedures = QtGui.QTableView(self.splitContainer)
        self.gridProcedures.setSelectionBehavior(1)
        self.gridProceduresSortModel = QtGui.QSortFilterProxyModel()
        self.gridProceduresStdModel = StandardItemModel()
        self.gridProceduresSortModel.setSourceModel(self.gridProceduresStdModel)
        self.gridProcedures.setModel(self.gridProceduresSortModel)
        p1.Add = self.gridProcedures
        p1.Add = self.pnlProcButtons

        self.gbProcLegs = GroupBox(p2)
        self.gbProcLegs.Title = "Procedure Legs"
        p2.Add = self.gbProcLegs

        self.tabControlProcLegs = QtGui.QTabWidget(self.gbProcLegs)
        self.tabControlProcLegs.setObjectName(("tabControlProcLegs"))
        self.tabProcLegs = QtGui.QWidget(Form)
        self.tabProcLegs.setObjectName(("tabProcLegs"))
        self.hlTabProcLegs = QtGui.QHBoxLayout(self.tabProcLegs)
        self.hlTabProcLegs.setObjectName("hlTabProcLegs")
        
        self.gridLegs = QtGui.QTableView(self.tabProcLegs)
        self.gridLegs.setSelectionBehavior(1)
        self.gridLegsStdModel = StandardItemModel()
        self.gridLegs.setModel(self.gridLegsStdModel)
        self.hlTabProcLegs.addWidget(self.gridLegs)
        
        self.pnlProcLegsButtons = Frame(self.tabProcLegs)

        self.btnLegsEdit = QtGui.QPushButton(self.pnlProcLegsButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLegsEdit.setIcon(icon)
        self.btnLegsEdit.setToolTip("Modify")
        self.pnlProcLegsButtons.Add = self.btnLegsEdit

        self.btnLegsPreview = QtGui.QPushButton(self.pnlProcLegsButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/pre.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLegsPreview.setIcon(icon)
        self.btnLegsPreview.setToolTip("Preview")
        self.pnlProcLegsButtons.Add = self.btnLegsPreview
        self.hlTabProcLegs.addWidget(self.pnlProcLegsButtons)

        

        self.tabControlProcLegs.addTab(self.tabProcLegs, ("AIXM 4.5"))


        self.tabProcLegsEx = QtGui.QWidget(Form)
        self.tabProcLegsEx.setObjectName(("tabProcLegsEx"))
        self.hlTabProcLegsEx = QtGui.QHBoxLayout(self.tabProcLegsEx)
        self.hlTabProcLegsEx.setObjectName("hlTabProcLegsEx")

        self.gridLegsEx = QtGui.QTableView(self.tabProcLegsEx)
        self.gridLegsEx.setSelectionBehavior(1)
        self.gridLegsExStdModel = StandardItemModel()
        self.gridLegsEx.setModel(self.gridLegsExStdModel)
        self.hlTabProcLegsEx.addWidget(self.gridLegsEx)


        self.pnlProcLegsExButtons = Frame(self.tabProcLegsEx)

        self.btnLegsExEdit = QtGui.QPushButton(self.pnlProcLegsExButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/mIconEditableEdits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLegsExEdit.setIcon(icon)
        self.btnLegsExEdit.setToolTip("Modify")
        self.pnlProcLegsExButtons.Add = self.btnLegsExEdit

        self.btnLegsExPreview = QtGui.QPushButton(self.pnlProcLegsExButtons)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resource/pre.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLegsExPreview.setIcon(icon)
        self.btnLegsExPreview.setToolTip("Preview")
        self.pnlProcLegsExButtons.Add = self.btnLegsExPreview
        self.hlTabProcLegsEx.addWidget(self.pnlProcLegsExButtons)


        self.tabControlProcLegs.addTab(self.tabProcLegsEx, ("AIXM 4.5+"))
        self.gbProcLegs.Add = self.tabControlProcLegs







