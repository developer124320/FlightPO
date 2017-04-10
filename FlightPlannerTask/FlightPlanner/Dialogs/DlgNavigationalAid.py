# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlopeUnits
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.types import NavigationalAidType
from Type.switch import switch
from Type.NavigationalAid import OmnidirectionalNavigationalAid, DirectionalNavigationalAid, LineOfSight


class DlgNavigationalAid(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70)
        self.setWindowTitle("Navigational Aid")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.gbAll = GroupBox(self)
        self.gbAll.Caption = "Properties"
        verticalLayoutDlg.addWidget(self.gbAll)

        self.pnlType = ComboBoxPanel(self.gbAll)
        self.pnlType.Caption = "Type"
        self.pnlType.LabelWidth = 140
        self.gbAll.Add = self.pnlType

        self.pnlName = TextBoxPanel(self.gbAll)
        self.pnlName.Caption = "Name"
        self.pnlName.LabelWidth = 140
        self.pnlType.Items = NavigationalAidType.Items
        self.gbAll.Add = self.pnlName

        self.pnlSlope = AngleGradientBoxPanel(self.gbAll)
        self.pnlSlope.CaptionUnits = AngleGradientSlopeUnits.Degrees
        self.pnlSlope.Caption = "Slope"
        self.pnlSlope.LabelWidth = 140
        self.gbAll.Add = self.pnlSlope

        self.pnlStartingHeight = AltitudeBoxPanel(self.gbAll)
        self.pnlStartingHeight.Caption = "Starting Height"
        self.pnlStartingHeight.CaptionUnits = "m"
        self.pnlStartingHeight.LabelWidth = 140
        self.gbAll.Add = self.pnlStartingHeight

        self.pnlFinishingDistance = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlFinishingDistance.Caption = "Finishing Distance"
        self.pnlFinishingDistance.LabelWidth = 140
        self.gbAll.Add = self.pnlFinishingDistance

        self.pnlAlfa = AngleGradientBoxPanel(self.gbAll)
        self.pnlAlfa.CaptionUnits = AngleGradientSlopeUnits.Degrees
        self.pnlAlfa.Caption = "Alpha [" + unicode("α", "utf-8") + " - Cone]"
        self.pnlAlfa.LabelWidth = 140
        self.gbAll.Add = self.pnlAlfa

        self.pnlRadiusCone = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlRadiusCone.Caption = "Radius [R - Cone]"
        self.pnlRadiusCone.LabelWidth = 140
        self.gbAll.Add = self.pnlRadiusCone

        self.pnlRadiusCylinder = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlRadiusCylinder.Caption = "Radius [r - Cylinder]"
        self.pnlRadiusCylinder.LabelWidth = 140
        self.gbAll.Add = self.pnlRadiusCylinder

        self.pnla = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnla.Caption = "a"
        self.pnla.LabelWidth = 140
        self.gbAll.Add = self.pnla

        self.pnlb = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlb.Caption = "b"
        self.pnlb.LabelWidth = 140
        self.gbAll.Add = self.pnlb

        self.pnlh = AltitudeBoxPanel(self.gbAll)
        self.pnlh.Caption = "h"
        self.pnlh.CaptionUnits = "m"
        self.pnlh.LabelWidth = 140
        self.gbAll.Add = self.pnlh

        self.pnlr = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlr.Caption = "r"
        self.pnlr.LabelWidth = 140
        self.gbAll.Add = self.pnlr

        self.pnlD = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlD.Caption = "D"
        self.pnlD.LabelWidth = 140
        self.gbAll.Add = self.pnlD

        self.pnlHbig = AltitudeBoxPanel(self.gbAll)
        self.pnlHbig.Caption = "H"
        self.pnlHbig.CaptionUnits = "m"
        self.pnlHbig.LabelWidth = 140
        self.gbAll.Add = self.pnlHbig

        self.pnlL = DistanceBoxPanel(self.gbAll, DistanceUnits.M)
        self.pnlL.Caption = "L"
        self.pnlL.LabelWidth = 140
        self.gbAll.Add = self.pnlL

        self.pnlphi = AngleGradientBoxPanel(self.gbAll)
        self.pnlphi.CaptionUnits = AngleGradientSlopeUnits.Degrees
        self.pnlphi.Caption = unicode("ɸ", "utf-8")
        self.pnlphi.LabelWidth = 140
        self.gbAll.Add = self.pnlphi

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        self.connect(self.pnlType, SIGNAL("Event_0"), self.method_5)

        self.shownOnce = False
        self.method_5()


    def get_NavigationalAid(self):
        for case in switch(self.pnlType.SelectedItem):
            if case(NavigationalAidType.Omnidirectional):
                return OmnidirectionalNavigationalAid(self.pnlName.Value, self.pnlAlfa.Value, self.pnlRadiusCone.Value, self.pnlRadiusCylinder.Value, False)
            elif case(NavigationalAidType.Directional):
                return DirectionalNavigationalAid(self.pnlName.Value, self.pnla.Value, self.pnlb.Value, self.pnlh.Value, self.pnlr.Value, self.pnlD.Value, self.pnlHbig.Value, self.pnlL.Value, self.pnlphi.Value, False)
            elif case(NavigationalAidType.LineOfSight):
                return LineOfSight(self.pnlName.Value, self.pnlSlope.Value, self.pnlStartingHeight.Value, self.pnlFinishingDistance.Value, False)
            else:
                return None

    def set_NavigationalAid(self, value):
        try:
            if (value != None):
                self.pnlType.SelectedIndex = self.pnlType.FindString(value.Type)
                self.pnlName.Value = value.Name
                if isinstance(value, DirectionalNavigationalAid):
                    directionalNavigationalAid = value
                    self.pnla.Value = directionalNavigationalAid.a
                    self.pnlb.Value = directionalNavigationalAid.b
                    self.pnlh.Value = directionalNavigationalAid.h
                    self.pnlr.Value = directionalNavigationalAid.r
                    self.pnlD.Value = directionalNavigationalAid.D
                    self.pnlHbig.Value = directionalNavigationalAid.H
                    self.pnlL.Value = directionalNavigationalAid.L
                    self.pnlphi.Value = directionalNavigationalAid.phi
                elif isinstance(value, OmnidirectionalNavigationalAid):
                    omnidirectionalNavigationalAid = value
                    self.pnlAlfa.Value = omnidirectionalNavigationalAid.Alfa
                    self.pnlRadiusCone.Value = omnidirectionalNavigationalAid.R
                    self.pnlRadiusCylinder.Value = omnidirectionalNavigationalAid.r
                elif isinstance(value, LineOfSight):
                    lineOfSight = value
                    self.pnlSlope.Value = lineOfSight.Slope
                    self.pnlStartingHeight.Value = lineOfSight.StartingHeight
                    self.pnlFinishingDistance.Value = lineOfSight.FinishingDistance
            self.method_5()
        except:
            pass

    NavigationalAid = property(get_NavigationalAid, set_NavigationalAid, None, None)


    def method_5(self):
        if (self.pnlType.SelectedIndex > -1):
            navigationalAidType = self.pnlType.SelectedItem
            self.pnlName.Enabled = True
            self.pnla.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlb.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlh.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlr.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlD.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlHbig.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlL.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlphi.Enabled = navigationalAidType == NavigationalAidType.Directional
            self.pnlAlfa.Enabled = navigationalAidType == NavigationalAidType.Omnidirectional
            self.pnlRadiusCone.Enabled = navigationalAidType == NavigationalAidType.Omnidirectional
            self.pnlRadiusCylinder.Enabled = navigationalAidType == NavigationalAidType.Omnidirectional
            self.pnlSlope.Enabled = navigationalAidType == NavigationalAidType.LineOfSight
            self.pnlStartingHeight.Enabled = navigationalAidType == NavigationalAidType.LineOfSight
            self.pnlFinishingDistance.Enabled = navigationalAidType == NavigationalAidType.LineOfSight

    def acceptDlg(self):

        self.accept()
    
    @staticmethod
    def smethod_0(iwin32Window_0, navigationalAid_0):
        flag = False
        dlgNavigationalAid = DlgNavigationalAid(iwin32Window_0)
        dlgNavigationalAid.NavigationalAid = navigationalAid_0
        result = dlgNavigationalAid.exec_()
        if (not result):
            flag = False
        else:
            navigationalAid_0 = dlgNavigationalAid.NavigationalAid
            flag = True
        return flag, navigationalAid_0