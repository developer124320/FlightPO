# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.helpers import Distance
from FlightPlanner.types import DistanceUnits
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel

import define

class MapScalePanel(QWidget):
    def __init__(self, parent, mapScaleDropDownType):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("DistanceBoxPanel" + str(len(parent.findChildren(MapScalePanel))))



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

        self.comboBox = ComboBoxPanel(self.frameBoxPanelIn)
        self.comboBox.Caption = "1"
        self.comboBox.LabelWidth = 20
        self.hLayoutframeBoxPanelIn.addWidget(self.comboBox)
        # self.txtDistance = QLineEdit(self.frameBoxPanelIn)
        # self.txtDistance.setEnabled(True)
        # font = QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.txtDistance.setFont(font)
        # self.txtDistance.setObjectName(("txtDistance"))
        # self.txtDistance.setText("0.0")
        # self.txtDistance.setMinimumWidth(70)
        # self.txtDistance.setMaximumWidth(70)
        # self.hLayoutframeBoxPanelIn.addWidget(self.txtDistance)

        self.imageButton = QToolButton(self.frameBoxPanelIn)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("btnDegreeBoxPanel"))
        self.hLayoutframeBoxPanelIn.addWidget(self.imageButton)

        self.hLayoutframeBoxPanel.addWidget(self.frameBoxPanelIn)
        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)

        self.imageButton.clicked.connect(self.imageButtonClicked)
        define._canvas.renderComplete.connect(self.canvas_renderComplete)
        self.connect(self.comboBox, SIGNAL("Event_0"), self.comboBox_Event_0)
        self.flag = 0
        self.dropDownType = mapScaleDropDownType
        self.method_5()
        self.imageButton.setVisible(False)
    def comboBox_Event_0(self):
        define._canvas.zoomScale(float(self.comboBox.SelectedItem))
    def canvas_renderComplete(self):
        self.comboBox.comboBox.setEditText(str(int(define._canvas.scale())))



    def method_4(self, mapScaleDropDownType_0):
        return (self.dropDownType & mapScaleDropDownType_0) == mapScaleDropDownType_0;
    def method_5(self):
        self.comboBox.Clear()
        if (self.method_4(MapScaleDropDownType.Aerodrome)):
            for i in range(2, 7):
                num = i * 5000;
                self.comboBox.Add(str(num))
        if (self.method_4(MapScaleDropDownType.Approach)):
            for j in range(4, 20):
                num1 = j * 50000;
                self.comboBox.Add(str(num1))
        if (self.method_4(MapScaleDropDownType.Enroute)):
            for k in range(2, 21):
                num2 = k * 500000;
                self.comboBox.Add(str(num2))
    # def method_6(self, string_0):
    #     value = None
    #     if self.distanceUnit == DistanceUnits.NM:
    #         value = self.txtDistance.text() + "nm"
    #     elif self.distanceUnit == DistanceUnits.M:
    #         value = self.txtDistance.text() + "m"
    #     elif self.distanceUnit == DistanceUnits.KM:
    #         value = self.txtDistance.text() + "km"
    #     elif self.distanceUnit == DistanceUnits.FT:
    #         value = self.txtDistance.text() + "ft"
    #     elif self.distanceUnit == DistanceUnits.MM:
    #         value = self.txtDistance.text() + "mm"
    #     else:
    #         value = ""
    # 
    # 
    #     return "%s%s\t%s"%(string_0, self.Caption, value);
    def txtDistanceChanged(self):
        try:
            test = float(self.txtDistance.text())
            self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtDistance.setText("0.0")
    def imageButtonClicked(self):
        measureDistanceTool = MeasureTool(define._canvas, self.txtDistance, self.distanceUnit)
        define._canvas.setMapTool(measureDistanceTool)
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
        # if self.distanceUnit == DistanceUnits.NM:
        #     value = captionStr + "(nm)"
        # elif self.distanceUnit == DistanceUnits.M:
        #     value = captionStr + "(m)"
        # elif self.distanceUnit == DistanceUnits.KM:
        #     value = captionStr + "(km)"
        # elif self.distanceUnit == DistanceUnits.FT:
        #     value = captionStr + "(ft)"
        # elif self.distanceUnit == DistanceUnits.MM:
        #     value = captionStr + "(mm)"
        # else:
        #     value = ""
        self.captionLabel.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_dropDownType(self):
        return self.dropDownType
    def set_dropDownType(self, val):
        self.dropDownType = val
    DropDownType = property(get_dropDownType, set_dropDownType, None, None)

    def get_Value(self):
        try:
            return self.comboBox.SelectedItem
        except:
            return ""

    # def set_Value(self, value):

    Value = property(get_Value, None, None, None)

    # def get_IsEmpty(self):
    #     return self.txtDistance.text() == "" or self.txtDistance.text() == None
    # IsEmpty = property(get_IsEmpty, None, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.comboBox.isReadOnly()
    def set_ReadOnly(self, bool):
        self.comboBox.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.comboBox.Enabled
    def set_Enabled(self, bool):
        self.comboBox.Enabled = bool
        self.imageButton.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.imageButton.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setVisible(True)
    Button = property(None, set_Button, None, None)
    
    # def method_5(self):
    #     self.comboBox.comboBox.clear()
    #     if (self.method_4(MapScaleDropDownType.Aerodrome))
    #     {
    #         for (int i = 2; i <= 6; i++)
    #         {
    #             int num = i * 5000;
    #             self.comboBox.Items.Add(num.ToString(Formats.MapScale));
    #         }
    #     }
    #     if (self.method_4(MapScaleDropDownType.Approach))
    #     {
    #         for (int j = 4; j < 20; j++)
    #         {
    #             int num1 = j * 50000;
    #             self.comboBox.Items.Add(num1.ToString(Formats.MapScale));
    #         }
    #     }
    #     if (self.method_4(MapScaleDropDownType.Enroute))
    #     {
    #         for (int k = 2; k <= 20; k++)
    #         {
    #             int num2 = k * 500000;
    #             self.comboBox.Items.Add(num2.ToString(Formats.MapScale));
    #         }
    #     }

class MapScaleDropDownType:
    Nothing = 0
    Aerodrome = 1
    Approach = 2
    Enroute = 4
    All = 7