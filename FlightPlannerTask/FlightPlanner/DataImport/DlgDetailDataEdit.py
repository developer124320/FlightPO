# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import Point3D, PositionPanel
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import DataBaseCoordinateType
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
import define

class DlgDetailDataEdit(QDialog):
    def __init__(self, parent, title, valueList = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70);
        self.setWindowTitle(title)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.frameBasic = Frame(self)
        verticalLayoutDlg.addWidget(self.frameBasic)

        self.pnlDetail = PositionPanel(self.frameBasic, None, None, "Degree")
        self.pnlDetail.btnCalculater.setVisible(False)
        self.pnlDetail.Caption = "Position"
        self.frameBasic.Add = self.pnlDetail

        self.pnlType = ComboBoxPanel(self.frameBasic)
        self.pnlType.Caption = "Type"
        self.pnlType.LabelWidth = 120
        self.frameBasic.Add = self.pnlType

        self.pnlCenter = PositionPanel(self.frameBasic, None, None, "Degree")
        self.pnlCenter.btnCalculater.setVisible(False)
        self.pnlCenter.Caption = "Center Position"
        self.pnlCenter.hideframe_Altitude()
        self.frameBasic.Add = self.pnlCenter


        self.pnlMagVariation = TextBoxPanel(self.frameBasic)
        self.pnlMagVariation.Caption = "Mag. Variation"
        self.pnlMagVariation.LabelWidth = 120
        self.frameBasic.Add = self.pnlMagVariation

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)


        self.x = ""
        self.y = ""
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.cenLatitude = ""
        self.cenLongitude = ""
        self.type = ""
        self.magVariation = ""

        self.pnlMagVariation.Visible = False
        self.pnlCenter.Visible = False
        self.pnlType.Items = [DataBaseCoordinateType.ArcPoint,
                              DataBaseCoordinateType.CCA,
                              DataBaseCoordinateType.CenPoint,
                              DataBaseCoordinateType.CWA,
                              DataBaseCoordinateType.FNT,
                              DataBaseCoordinateType.GRC,
                              DataBaseCoordinateType.MidPoint,
                              DataBaseCoordinateType.Point]

        if valueList != None:
            self.pnlDetail.Point3d = Point3D(float(valueList[1]), float(valueList[0]), float(valueList[2]) if (valueList[2] != None and valueList[2] != "") else 0.0 )
            self.pnlType.Value = valueList[3]
            if title == "Modify Detail Airspace":
                if valueList[5] != None and valueList[5] != "":
                    self.pnlCenter.Point3d = Point3D(float(valueList[5]), float(valueList[4]))
            elif title == "Modify Detail Routes":
                self.pnlMagVariation.Value = valueList[4]
        if title == "Modify Detail Airspace" or title == "Add Detail Airspace":
            self.pnlCenter.Visible = True
        elif title == "Modify Detail Routes" or title == "Add Detail Routes":
            self.pnlMagVariation.Visible = True
    def acceptDlg(self):
        if self.pnlDetail.Point3d != None and isinstance(self.pnlDetail.Point3d, Point3D):
            xyPoint = QgisHelper.CrsTransformPoint(self.pnlDetail.Point3d.get_X(), self.pnlDetail.Point3d.get_Y(), define._latLonCrs, define._xyCrs, self.pnlDetail.Point3d.get_Z())
            self.x = QString(str(xyPoint.get_X()))
            self.y = QString(str(xyPoint.get_Y()))
            self.latitude = QString(str(self.pnlDetail.Point3d.get_Y()))
            self.longitude = QString(str(self.pnlDetail.Point3d.get_X()))
            self.altitude = QString(str(self.pnlDetail.Altitude().Metres))
        if self.pnlCenter.Point3d != None and isinstance(self.pnlCenter.Point3d, Point3D):
            self.cenLatitude = QString(str(self.pnlCenter.Point3d.get_Y()))
            self.cenLongitude = QString(str(self.pnlCenter.Point3d.get_X()))
        self.magVariation = self.pnlMagVariation.Value
        self.type = self.pnlType.SelectedItem
        self.accept()