# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.helpers import MathHelper, Unit, Point3D

from qgis.core import QGis


import define

class TrackRadialBoxPanel(QWidget):
    def __init__(self, parent, alwwaysShowString = None):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("TrackRadialBoxPanel" + str(len(parent.findChildren(TrackRadialBoxPanel))))
        self.parentP = parent

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)


        self.hLayoutBoxPanel = QHBoxLayout(self)
        self.hLayoutBoxPanel.setSpacing(0)
        self.hLayoutBoxPanel.setContentsMargins(0,0,0,0)
        self.hLayoutBoxPanel.setObjectName(("hLayoutBoxPanel"))
        self.frameBoxPanel = QFrame(self)

        self.frameBoxPanel.setFrameShape(QFrame.NoFrame)
        self.frameBoxPanel.setFrameShadow(QFrame.Raised)
        self.frameBoxPanel.setObjectName(("frameBoxPanel"))
        self.hLayoutframeBoxPanel = QHBoxLayout(self.frameBoxPanel)
        self.hLayoutframeBoxPanel.setSpacing(0)
        self.hLayoutframeBoxPanel.setMargin(0)
        self.hLayoutframeBoxPanel.setObjectName(("hLayoutframeBoxPanel"))
        self.captionLabel = QLabel(self.frameBoxPanel)
        # sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.captionLabel.sizePolicy().hasHeightForWidth())
        # self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setMinimumSize(QSize(200, 0))
        self.captionLabel.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.captionLabel.setFont(font)
        self.captionLabel.setObjectName(("captionLabel"))
        self.hLayoutframeBoxPanel.addWidget(self.captionLabel)

        self.frameBoxPanelIn = Frame(self.frameBoxPanel, "HL")
        self.frameBoxPanelIn.layoutBoxPanel.setSpacing(5)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameBoxPanelIn.sizePolicy().hasHeightForWidth())
        self.frameBoxPanelIn.setSizePolicy(sizePolicy)

        self.txtRadialPlan = NumberBoxPanel(self.frameBoxPanelIn)
        self.txtRadialPlan.Caption = "Plan"
        self.txtRadialPlan.LabelWidth = 50
        self.frameBoxPanelIn.Add = self.txtRadialPlan

        self.txtRadialGeodetic = NumberBoxPanel(self.frameBoxPanelIn)
        self.txtRadialGeodetic.Caption = "Geodetic"
        self.txtRadialGeodetic.LabelWidth = 70
        self.frameBoxPanelIn.Add = self.txtRadialGeodetic

        self.btnCaptureRadial = QToolButton(self.frameBoxPanelIn)
        self.btnCaptureRadial.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)
        self.btnCaptureRadial.setIcon(icon)
        self.btnCaptureRadial.setObjectName(("btnCaptureRadial"))
        self.frameBoxPanelIn.Add = self.btnCaptureRadial

        self.hLayoutframeBoxPanel.addWidget(self.frameBoxPanelIn)
        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(0,10,QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)

        self.connect(self.txtRadialPlan, SIGNAL("Event_0"), self.txtRadialPlanChanged)
        self.connect(self.txtRadialGeodetic, SIGNAL("Event_0"), self.txtRadialGeodeticChanged)
        self.btnCaptureRadial.clicked.connect(self.btnCaptureRadialClicked)


        self.captionUnits = unicode("°", "utf-8")

        self.flag = 0
        self.startPoint = None
        self.endPoint = None
        self.alwwaysShowString = alwwaysShowString
        # self.txtRadialGeodetic.setText("0.0")
    def method_6(self, string_0):
        return "%s%s\t%f %s"%(string_0, self.Caption, self.Value, self.captionUnits);
    def txtRadialPlanChanged(self):
        try:
            if self.flag==0:
                self.flag=1;
            if self.flag==2:
                self.flag=0;
            if self.flag==1:
                try:
                    self.txtRadialGeodetic.Value = round(self.otherBearingCalc(self.txtRadialPlan.Value, QGis.Meters), 4)
                except:
                    self.txtRadialGeodetic.Value = 0.0
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtRadialGeodetic.Value = 0.0


    def txtRadialGeodeticChanged(self):
        try:
            if self.flag==0:
                self.flag=2;
            if self.flag==1:
                self.flag=0;
            if self.flag==2:
                try:
                    self.txtRadialPlan.Value = round(self.otherBearingCalc(self.txtRadialGeodetic.Value, QGis.DecimalDegrees), 4)
                except:
                    self.txtRadialPlan.Value = 0.0
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtRadialPlan.Value = 0.0

    def otherBearingCalc(self, basicAngle, basicUnit):
        positionPanelOfParent = None
        existPositionPanelValid = False
        if len(self.parentP.findChildren(PositionPanel)) > 0:
            for pnl in self.parentP.findChildren(PositionPanel):
                if pnl.IsValid():
                    positionPanelOfParent = pnl
                    existPositionPanelValid = True
                    break
        basicBearing = Unit.ConvertDegToRad(basicAngle)
        unit = positionPanelOfParent.getUnit()
        basicPoint3d = None
        if existPositionPanelValid:
            basicPoint3d = positionPanelOfParent.Point3d
        else:
            if basicUnit == QGis.Meters:
                basicPoint3d = Point3D(656565, 6565656)
            else:
                basicPoint3d = Point3D(17, 59)

        resultBearing = None
        if unit == None:
            return
        elif unit == QGis.Meters:
            if basicUnit == QGis.Meters:
                point3dStart = basicPoint3d
                point3dEnd = MathHelper.distanceBearingPoint(point3dStart, basicBearing, 500, QGis.Meters)
                point3dStartGeo = MathHelper.CrsTransformPoint(point3dStart.get_X(), point3dStart.get_Y(), define._xyCrs, define._latLonCrs, point3dStart.get_Z())
                point3dEndGeo = MathHelper.CrsTransformPoint(point3dEnd.get_X(), point3dEnd.get_Y(), define._xyCrs, define._latLonCrs, point3dEnd.get_Z())
                resultBearing = MathHelper.getBearing(point3dStartGeo, point3dEndGeo, QGis.DecimalDegrees)
            else:
                point3dStart = basicPoint3d
                point3dStartGeo = MathHelper.CrsTransformPoint(point3dStart.get_X(), point3dStart.get_Y(), define._xyCrs, define._latLonCrs, point3dStart.get_Z())

                point3dEndGeo = MathHelper.distanceBearingPoint(point3dStartGeo, basicBearing, 500, QGis.DecimalDegrees)
                point3dEnd = MathHelper.CrsTransformPoint(point3dEndGeo.get_X(), point3dEndGeo.get_Y(), define._latLonCrs, define._xyCrs, point3dEndGeo.get_Z())
                resultBearing = MathHelper.getBearing(point3dStart, point3dEnd, QGis.Meters)
        else:
            if basicUnit == QGis.Meters:
                point3dStartGeo = basicPoint3d
                point3dStart = MathHelper.CrsTransformPoint(point3dStartGeo.get_X(), point3dStartGeo.get_Y(), define._latLonCrs, define._xyCrs, point3dStartGeo.get_Z())

                point3dEnd = MathHelper.distanceBearingPoint(point3dStart, basicBearing, 500, QGis.Meters)
                point3dEndGeo = MathHelper.CrsTransformPoint(point3dEnd.get_X(), point3dEnd.get_Y(), define._xyCrs, define._latLonCrs, point3dEnd.get_Z())
                resultBearing = MathHelper.getBearing(point3dStartGeo, point3dEndGeo, QGis.DecimalDegrees)
            else:
                point3dStartGeo = basicPoint3d
                point3dEndGeo = MathHelper.distanceBearingPoint(point3dStartGeo, basicBearing, 500, QGis.DecimalDegrees)

                point3dStart = MathHelper.CrsTransformPoint(point3dStartGeo.get_X(), point3dStartGeo.get_Y(), define._latLonCrs, define._xyCrs, point3dStartGeo.get_Z())
                point3dEnd = MathHelper.CrsTransformPoint(point3dEndGeo.get_X(), point3dEndGeo.get_Y(), define._latLonCrs, define._xyCrs, point3dEndGeo.get_Z())
                resultBearing = MathHelper.getBearing(point3dStart, point3dEnd, QGis.Meters)
        return Unit.ConvertRadToDeg(resultBearing)






    def btnCaptureRadialClicked(self):
        self.captureRadialTool = CaptureBearingTool(define._canvas, self.txtRadialPlan, self.txtRadialGeodetic)
        define._canvas.setMapTool(self.captureRadialTool)
        self.emit(SIGNAL("Event_1"), self)

    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def get_Caption(self):
        caption = self.captionLabel.text()
        findIndex = caption.indexOf("(")
        if findIndex > 0:
            val = caption.left(findIndex)
            return val
        return caption
    def set_Caption(self, captionStr):
        value = captionStr + "(" + self.captionUnits + "):"
        self.captionLabel.setText(value)
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def get_Value(self):
        try:
            if self.alwwaysShowString == "Geo":
                return float(self.txtRadialGeodetic.Value)
            else:
                if define._units == QGis.Meters:
                    return float(self.txtRadialPlan.Value)
                else:
                    return float(self.txtRadialGeodetic.Value)
        except:
            return 0.0

    def set_Value(self, val):
        if val == None:
            self.txtRadialPlan.Value = 0.0
            self.txtRadialGeodetic.Value = 0.0
            return
        try:
            test = float(val)
            if define._units == QGis.Meters:
                self.txtRadialPlan.Value = val
            else:
                self.txtRadialGeodetic.Value = val
        except:
            str0 = "You must put the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtRadialPlan.Value = 0.0
            self.txtRadialGeodetic.Value = 0.0
        pass

    Value = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return False
        # return self.txtRadialPlan.Value == "" or self.txtRadialPlan.text() == None
    IsEmpty = property(get_IsEmpty, None, None, None)


    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.txtRadialPlan.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtRadialPlan.setReadOnly(bool)
        self.txtRadialGeodetic.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.txtRadialPlan.isEnabled()
    def set_Enabled(self, bool):
        self.txtRadialPlan.setEnabled(bool)
        # self.btnCaptureRadial.setEnabled(bool)
        self.txtRadialGeodetic.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.btnCaptureRadial.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.btnCaptureRadial.setIcon(icon)
        self.btnCaptureRadial.setVisible(True)
    Button = property(None, set_Button, None, None)