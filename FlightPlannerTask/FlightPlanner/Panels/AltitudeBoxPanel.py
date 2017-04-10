# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, SIGNAL
from FlightPlanner.helpers import Unit, Altitude
from FlightPlanner.Panels.Frame import Frame


class AltitudeBoxPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("AltitudeBoxPanel" + str(len(parent.findChildren(AltitudeBoxPanel))))

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

        self.txtAltitudeM = QLineEdit(self.frameBoxPanelIn)
        self.txtAltitudeM.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitudeM.setFont(font)
        self.txtAltitudeM.setObjectName(self.objectName() + "_txtAltitudeM")
        self.txtAltitudeM.setText("0.0")
        self.txtAltitudeM.setMinimumWidth(70)
        self.txtAltitudeM.setMaximumWidth(70)
        self.hLayoutframeBoxPanelIn.addWidget(self.txtAltitudeM)

        labelM = QLabel(self.frameBoxPanelIn)
        labelM.setObjectName(("labelM"))
        labelM.setText(" m ")
        self.hLayoutframeBoxPanelIn.addWidget(labelM)

        self.txtAltitudeFt = QLineEdit(self.frameBoxPanelIn)
        self.txtAltitudeFt.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitudeFt.setFont(font)
        self.txtAltitudeFt.setObjectName(self.objectName() + "_txtAltitudeFt")
        self.txtAltitudeFt.setText("0.0")
        self.txtAltitudeFt.setMinimumWidth(70)
        self.txtAltitudeFt.setMaximumWidth(70)
        self.hLayoutframeBoxPanelIn.addWidget(self.txtAltitudeFt)

        labelFt = QLabel(self.frameBoxPanelIn)
        labelFt.setObjectName(("labelFt"))
        labelFt.setText(" ft")
        self.hLayoutframeBoxPanelIn.addWidget(labelFt)

        self.hLayoutframeBoxPanel.addWidget(self.frameBoxPanelIn)
        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)



        self.txtAltitudeM.textChanged.connect(self.txtAltitudeMChanged)
        self.txtAltitudeFt.textChanged.connect(self.txtAltitudeFtChanged)

        self.txtAltitudeM.editingFinished.connect(self.txtAltitude_returnPressed)
        self.txtAltitudeFt.editingFinished.connect(self.txtAltitude_returnPressed)

        self.value = 0.0
        self.captionUnits = "m"
        self.OriginalUnits = "m"

        self.flag = 0
        self.txtAltitudeM.setText("0.0")
    def mouseMoveEvent(self, mouseEvent):
        pt = mouseEvent.pos()
        c = self.childAt(pt)
        pass
    def method_8(self, string_0):
        if self.CaptionUnits == "m":
            return "%s%s\t%s %s"%(string_0, self.Caption, self.txtAltitudeM, self.CaptionUnits);
        else:
            return "%s%s\t%s %s"%(string_0, self.Caption, self.txtAltitudeFt, self.CaptionUnits);
    def txtAltitude_returnPressed(self):
        self.emit(SIGNAL("editingFinished"), self)
    def txtAltitudeFtChanged(self):
        try:
            test = float(self.txtAltitudeFt.text())
            if self.flag==0:
                self.flag=1;
            if self.flag==2:
                self.flag=0;
            if self.flag==1:
                try:
                    self.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.txtAltitudeFt.text())), 4)))
                except:
                    self.txtAltitudeM.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitudeM.setText("0.0")


    def txtAltitudeMChanged(self):
        try:
            test = float(self.txtAltitudeM.text())
            if self.flag==0:
                self.flag=2;
            if self.flag==1:
                self.flag=0;
            if self.flag==2:
                try:
                    self.txtAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.txtAltitudeM.text())), 4)))
                except:
                    self.txtAltitudeFt.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitudeFt.setText("0.0")

    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
        self.OriginalUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def get_Caption(self):
        caption = self.captionLabel.text()
        val = caption.left(caption.length() - 1)
        return val
    def set_Caption(self, captionStr):
        self.captionLabel.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def get_Value(self):
        try:
            return Altitude(float(self.txtAltitudeM.text()))
        except:
            return Altitude(0.0)

    def set_Value(self, altitude):
        if altitude == None:
            self.txtAltitudeM.setText(str("0.0"))
            return
        if isinstance(altitude, Altitude):
            if self.CaptionUnits == "m":
                self.txtAltitudeM.setText(str(round(altitude.Metres, 4)))
            else:
                self.txtAltitudeFt.setText(str(round(altitude.Feet, 4)))
        else:
            str0 = "You must input the type \"Altitude\" in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtAltitudeM.setText("0.0")
    Value = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return self.txtAltitudeM.text() == "" or self.txtAltitudeM.text() == None
    IsEmpty = property(get_IsEmpty, None, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.txtAltitudeM.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtAltitudeM.setReadOnly(bool)
        self.txtAltitudeFt.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.txtAltitudeM.isEnabled()
    def set_Enabled(self, bool):
        self.txtAltitudeM.setEnabled(bool)
        self.txtAltitudeFt.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

