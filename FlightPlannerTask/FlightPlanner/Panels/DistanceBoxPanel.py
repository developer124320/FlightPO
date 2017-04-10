# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.helpers import Distance, Unit
from FlightPlanner.types import DistanceUnits

import define

class DistanceBoxPanel(QWidget):
    def __init__(self, parent, distanceUnit, distanceUnit1 = None):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("DistanceBoxPanel" + str(len(parent.findChildren(DistanceBoxPanel))))

        self.distanceUnit = distanceUnit
        self.distanceUnit1 = distanceUnit1

        self.hLayoutBoxPanel = QHBoxLayout(self)
        self.hLayoutBoxPanel.setSpacing(0)
        self.hLayoutBoxPanel.setContentsMargins(0,0,0,0)
        self.hLayoutBoxPanel.setObjectName(("hLayoutBoxPanel"))
        self.frameBoxPanel = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameBoxPanel.sizePolicy().hasHeightForWidth())
        self.frameBoxPanel.setSizePolicy(sizePolicy)
        self.frameBoxPanel.setFrameShape(QFrame.NoFrame)
        self.frameBoxPanel.setFrameShadow(QFrame.Raised)
        self.frameBoxPanel.setObjectName(("frameBoxPanel"))
        self.hLayoutframeBoxPanel = QHBoxLayout(self.frameBoxPanel)
        self.hLayoutframeBoxPanel.setSpacing(0)
        self.hLayoutframeBoxPanel.setMargin(0)
        self.hLayoutframeBoxPanel.setObjectName(("hLayoutframeBoxPanel"))
        self.captionLabel = QLabel(self.frameBoxPanel)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.captionLabel.sizePolicy().hasHeightForWidth())
        self.captionLabel.setSizePolicy(sizePolicy)
        self.captionLabel.setMinimumSize(QSize(200, 0))
        self.captionLabel.setMaximumSize(QSize(200, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.captionLabel.setFont(font)
        self.captionLabel.setObjectName(("captionLabel"))
        self.hLayoutframeBoxPanel.addWidget(self.captionLabel)

        self.frameBoxPanelIn = QFrame(self.frameBoxPanel)
        self.frameBoxPanelIn.setFrameShape(QFrame.StyledPanel)
        self.frameBoxPanelIn.setFrameShadow(QFrame.Raised)
        self.frameBoxPanelIn.setObjectName(("frameBoxPanelIn"))
        self.hLayoutframeBoxPanelIn = QHBoxLayout(self.frameBoxPanelIn)
        self.hLayoutframeBoxPanelIn.setSpacing(0)
        self.hLayoutframeBoxPanelIn.setMargin(0)
        self.hLayoutframeBoxPanelIn.setObjectName(("hLayoutframeBoxPanelIn"))

        self.txtDistance = QLineEdit(self.frameBoxPanelIn)
        self.txtDistance.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDistance.setFont(font)
        self.txtDistance.setObjectName(self.objectName() + "_txtDistance")
        self.txtDistance.setText("0.0")
        self.txtDistance.setMinimumWidth(70)
        self.txtDistance.setMaximumWidth(70)
        self.hLayoutframeBoxPanelIn.addWidget(self.txtDistance)

        if self.distanceUnit1 != None:
            labelM = QLabel(self.frameBoxPanelIn)
            labelM.setObjectName(("labelM"))
            value = ""
            if self.distanceUnit == DistanceUnits.NM:
                value = " nm "
            elif self.distanceUnit == DistanceUnits.M:
                value = " m "
            elif self.distanceUnit == DistanceUnits.KM:
                value = " km "
            elif self.distanceUnit == DistanceUnits.FT:
                value = " ft "
            elif self.distanceUnit == DistanceUnits.MM:
                value = " mm "
            else:
                value = ""
            labelM.setText(value)
            self.hLayoutframeBoxPanelIn.addWidget(labelM)

            self.txtDistance1 = QLineEdit(self.frameBoxPanelIn)
            self.txtDistance1.setEnabled(True)
            font = QFont()
            font.setBold(False)
            font.setWeight(50)
            self.txtDistance1.setFont(font)
            self.txtDistance1.setObjectName(self.objectName() + "_txtDistance1")
            self.txtDistance1.setText("0.0")
            self.txtDistance1.setMinimumWidth(70)
            self.txtDistance1.setMaximumWidth(70)
            self.txtDistance1.setText("0.0")
            self.hLayoutframeBoxPanelIn.addWidget(self.txtDistance1)

            label1 = QLabel(self.frameBoxPanelIn)
            label1.setObjectName(("labelFt"))
            value = ""
            if self.distanceUnit1 == DistanceUnits.NM:
                value = " nm "
            elif self.distanceUnit1 == DistanceUnits.M:
                value = " m "
            elif self.distanceUnit1 == DistanceUnits.KM:
                value = " km "
            elif self.distanceUnit1 == DistanceUnits.FT:
                value = " ft "
            elif self.distanceUnit1 == DistanceUnits.MM:
                value = " mm "
            else:
                value = ""
            label1.setText(value)
            self.hLayoutframeBoxPanelIn.addWidget(label1)

            # self.txtDistance.textChanged.connect(self.txtDistanceChanged)
            self.txtDistance1.textChanged.connect(self.txtDistance1Changed)
            self.txtDistance1.editingFinished.connect(self.txtDistanceEditingFinished)

        self.btnCaptureDistance = QToolButton(self.frameBoxPanelIn)
        self.btnCaptureDistance.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)
        self.btnCaptureDistance.setIcon(icon)
        self.btnCaptureDistance.setObjectName(("btnDegreeBoxPanel"))
        self.hLayoutframeBoxPanelIn.addWidget(self.btnCaptureDistance)

        self.hLayoutframeBoxPanel.addWidget(self.frameBoxPanelIn)
        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)




        self.txtDistance.textChanged.connect(self.txtDistanceChanged)
        self.txtDistance.editingFinished.connect(self.txtDistanceEditingFinished)
        self.btnCaptureDistance.clicked.connect(self.btnCaptureDistanceClicked)


        # self.value = 0.0



        self.flag = 0
        self.txtDistance.setText("0.0")

    def txtDistance1Changed(self):
        try:
            test = float(self.txtDistance1.text())
            if self.flag==0:
                self.flag=1;
            if self.flag==2:
                self.flag=0;
            if self.flag==1:
                try:
                    self.txtDistance.setText(str(round(Unit.ConvertNMToMeter(float(self.txtDistance1.text())), 4)))
                except:
                    self.txtDistance.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtDistance.setText("0.0")

    def txtDistanceEditingFinished(self):
        self.emit(SIGNAL("editingFinished"), self)
    def txtDistanceChanged(self):
        if self.distanceUnit1 != None:
            try:
                test = float(self.txtDistance.text())
                if self.flag==0:
                    self.flag=2;
                if self.flag==1:
                    self.flag=0;
                if self.flag==2:
                    try:
                        self.txtDistance1.setText(str(round(Unit.ConvertMeterToNM(float(self.txtDistance.text())), 4)))
                    except:
                        self.txtDistance1.setText("0.0")
                    self.emit(SIGNAL("Event_0"), self)
            except:
                str0 = "You must input the float type in \"%s\"."%(self.Caption)
                QMessageBox.warning(self, "Warning" , str0)
                self.txtDistance1.setText("0.0")
        else:
            try:
                test = float(self.txtDistance.text())
                self.emit(SIGNAL("Event_0"), self)
            except:
                str0 = "You must input the float type in \"%s\"."%(self.Caption)
                QMessageBox.warning(self, "Warning" , str0)
                self.txtDistance.setText("0.0")

    def method_6(self, string_0):
        value = None
        if self.distanceUnit == DistanceUnits.NM:
            value = self.txtDistance.text() + "nm"
        elif self.distanceUnit == DistanceUnits.M:
            value = self.txtDistance.text() + "m"
        elif self.distanceUnit == DistanceUnits.KM:
            value = self.txtDistance.text() + "km"
        elif self.distanceUnit == DistanceUnits.FT:
            value = self.txtDistance.text() + "ft"
        elif self.distanceUnit == DistanceUnits.MM:
            value = self.txtDistance.text() + "mm"
        else:
            value = ""


        return "%s%s\t%s"%(string_0, self.Caption, value);
    def btnCaptureDistanceClicked(self):
        measureDistanceTool = MeasureTool(define._canvas, self.txtDistance, self.distanceUnit)
        define._canvas.setMapTool(measureDistanceTool)
        self.connect(measureDistanceTool, SIGNAL("captureFinished"), self.txtDistanceEditingFinished)
        self.emit(SIGNAL("Event_1"), self)

    def get_CaptionUnits(self):
        return self.distanceUnit
    def set_CaptionUnits(self, distanceUnit):
        self.distanceUnit = distanceUnit
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def get_Caption(self):
        caption = self.captionLabel.text()
        findIndex = caption.indexOf("(")
        if findIndex > 0:
            val = caption.left(findIndex)
            return val
        return caption
    def set_Caption(self, captionStr):
        if self.distanceUnit1 == None:
            if self.distanceUnit == DistanceUnits.NM:
                value = captionStr + "(nm)"
            elif self.distanceUnit == DistanceUnits.M:
                value = captionStr + "(m)"
            elif self.distanceUnit == DistanceUnits.KM:
                value = captionStr + "(km)"
            elif self.distanceUnit == DistanceUnits.FT:
                value = captionStr + "(ft)"
            elif self.distanceUnit == DistanceUnits.MM:
                value = captionStr + "(mm)"
            else:
                value = ""
        else:
            value = captionStr
        self.captionLabel.setText(value + ":")
    Caption = property(get_Caption, set_Caption, None, None)



    def get_Value(self):
        try:
            return Distance(float(self.txtDistance.text()), self.distanceUnit)
        except:
            return Distance(0.0)

    def set_Value(self, distance):
        if distance == None:
            self.txtDistance.setText("0.0")
            # self.distanceUnit = DistanceUnits.NM
            return
        if isinstance(distance, Distance):
            if distance.IsNaN():
                self.txtDistance.setText("0.0")
                # self.distanceUnit = DistanceUnits.NM
                return
            if self.distanceUnit == DistanceUnits.NM:
                self.txtDistance.setText(str(round(distance.NauticalMiles, 4)))
                self.distanceUnit = DistanceUnits.NM
            elif self.distanceUnit == DistanceUnits.M:
                self.txtDistance.setText(str(round(distance.Metres, 4)))
                self.distanceUnit = DistanceUnits.M
            elif self.distanceUnit == DistanceUnits.KM:
                self.txtDistance.setText(str(round(distance.Kilometres, 4)))
                self.distanceUnit = DistanceUnits.KM
            elif self.distanceUnit == DistanceUnits.FT:
                self.txtDistance.setText(str(round(distance.Feet, 4)))
                self.distanceUnit = DistanceUnits.FT
            elif self.distanceUnit == DistanceUnits.MM:
                self.txtDistance.setText(str(int(distance.Milimeters)))
                self.distanceUnit = DistanceUnits.MM
            else:
                self.txtDistance.setText("0.0")
                self.distanceUnit = DistanceUnits.NM
        else:
            str0 = "You must input the type of \"Distance\" in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtDistance.setText("0.0")
    Value = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return self.txtDistance.text() == "" or self.txtDistance.text() == None
    IsEmpty = property(get_IsEmpty, None, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.txtDistance.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtDistance.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.txtDistance.isEnabled()
    def set_Enabled(self, bool):
        self.txtDistance.setEnabled(bool)
        if self.distanceUnit1 != None:
            self.txtDistance1.setEnabled(bool)
        self.btnCaptureDistance.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.btnCaptureDistance.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.btnCaptureDistance.setIcon(icon)
        self.btnCaptureDistance.setVisible(True)
    Button = property(None, set_Button, None, None)
