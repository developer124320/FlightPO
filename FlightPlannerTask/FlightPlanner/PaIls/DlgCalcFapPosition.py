# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QFileDialog, QDialog, QMessageBox, QDialogButtonBox
from PyQt4.QtCore import QSizeF, SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, Distance, DistanceUnits
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.helpers import MathHelper, Unit
from FlightPlanner.BasicGNSS.rnavWaypoints import RnavWaypoints
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx
import math



class DlgFapCalcPosition(QDialog):
    def __init__(self, parent, thrPos, rwyPos = None, track = None):
        QDialog.__init__(self, parent)
        self.baseTrack = track
        self.resize(290, 136)
        self.setWindowTitle("Calculate FAP")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.groupBox = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox)

        self.pnlThrPosition = PositionPanel(self.groupBox)
        self.pnlThrPosition.Point3d = thrPos
        self.groupBox.Add = self.pnlThrPosition
        self.pnlThrPosition.Visible = False

        self.pnlRwyEndPosition = PositionPanel(self.groupBox)
        self.pnlRwyEndPosition.Point3d = rwyPos
        self.groupBox.Add = self.pnlRwyEndPosition
        self.pnlRwyEndPosition.Visible = False

        self.pnlTrack = TrackRadialBoxPanel(self.groupBox)
        self.pnlTrack.Caption = "Track"
        if rwyPos == None:
            self.pnlTrack.Value = track
        else:
            self.pnlTrack.Value = MathHelper.getBearing(thrPos, rwyPos)
        self.pnlTrack.LabelWidth = 100
        self.groupBox.Add = self.pnlTrack

        self.pnlDist = DistanceBoxPanel(self.groupBox, DistanceUnits.M, DistanceUnits.NM)
        self.pnlDist.Caption = "Distance"
        self.pnlDist.Value = Distance(5, DistanceUnits.NM)
        self.pnlDist.LabelWidth = 100
        self.groupBox.Add = self.pnlDist

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        
    def acceptDlg(self):
        nauticalMiles = self.pnlDist.Value.NauticalMiles
        value = Unit.ConvertDegToRad(self.pnlTrack.Value)
        num1 = math.fabs(self.baseTrack - value)
        if (num1 > 180):
            num1 = 360 - num1
        num2 = math.sin(Unit.smethod_0(num1)) * 0.7559395
        num3 = Unit.smethod_1(math.asin(num2 / nauticalMiles))
        num4 = math.cos(Unit.smethod_0(num1)) * 0.755939525
        num5 = math.cos(Unit.smethod_0(num3)) * nauticalMiles
        calcPt = RnavWaypoints.smethod_3(self.pos1400m, self.pnlTrack.Value, Distance(math.fabs(num5 - num4), DistanceUnits.NM))

        self.accept()

    # @staticmethod
    # def smethod_0(parent, thrPos, rwyPos = None, track = None):
    #     dlg = DlgFapCalcPosition(parent, thrPos, rwyPos, track)
    #     dlg.
    
    


