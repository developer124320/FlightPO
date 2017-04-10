# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.helpers import Speed, SpeedUnits

class SpeedBoxPanel(QWidget):
    def __init__(self, parent, speedUnits = SpeedUnits.KTS):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("SpeedBoxPanel" + str(len(parent.findChildren(SpeedBoxPanel))))


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

        self.textBox = QLineEdit(self.frameBoxPanel)
        self.textBox.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.textBox.setFont(font)
        self.textBox.setObjectName(("textBox"))
        self.textBox.setText("0.0")
        self.textBox.setMinimumWidth(70)
        self.textBox.setMaximumWidth(70)
        self.hLayoutframeBoxPanel.addWidget(self.textBox)

        self.imageButton = QToolButton(self.frameBoxPanel)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/convex_hull.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("imageButton"))
        self.imageButton.setVisible(False)
        self.hLayoutframeBoxPanel.addWidget(self.imageButton)

        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)

        self.textBox.textChanged.connect(self.textBoxChanged)
        self.textBox.editingFinished.connect(self.textBoxEditingFinished)
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.textBox.setText("0.0")

        self.captionUnits = speedUnits

    def textBoxEditingFinished(self):
        self.emit(SIGNAL("editingFinished"), self)

    def method_6(self, string_0):
        if self.CaptionUnits == SpeedUnits.KMH:
            unit = "kmh"
        elif self.CaptionUnits == SpeedUnits.KTS:
            unit = "kts"
        else:
            unit = ""
        value = self.textBox.text() + unit
        return "%s%s\t%s"%(string_0, self.Caption, value);

    def textBoxChanged(self):
        try:
            test = float(self.textBox.text())
            self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.textBox.setText("0.0")

    def imageButtonClicked(self):
        self.emit(SIGNAL("Event_1"), self)
    def get_Caption(self):
        caption = self.captionLabel.text()
        findIndex = caption.indexOf("(")
        if findIndex > 0:
            val = caption.left(findIndex)
            return val
        return caption
    def set_Caption(self, captionStr):
        if self.CaptionUnits  == SpeedUnits.KTS:
            self.captionLabel.setText(captionStr + "(kts)" + ":")
        elif self.CaptionUnits  == SpeedUnits.KMH:
            self.captionLabel.setText(captionStr + "(kmh)" + ":")
        else:
            self.captionLabel.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def set_ButtonVisible(self, bool):
        self.imageButton.setVisible(bool)
    ButtonVisible = property(None, set_ButtonVisible, None, None)

    def get_Value(self):
        try:
            return Speed(float(self.textBox.text()), self.CaptionUnits)
        except:
            return Speed(None)

    def set_Value(self, speed):
        if speed == None:
            self.textBox.setText("0.0")
            return
        try:
            if self.CaptionUnits == SpeedUnits.KMH:
                self.textBox.setText(str(round(speed.KilometresPerHour, 4)))
            elif self.CaptionUnits == SpeedUnits.KTS:
                self.textBox.setText(str(round(speed.Knots, 4)))
            else:
                self.textBox.setText("0.0")
        except:
            self.textBox.setText("0.0")
    Value = property(get_Value, set_Value, None, None)

    def get_IsEmpty(self):
        return self.textBox.text() == "" or self.textBox.text() == None
    IsEmpty = property(get_IsEmpty, None, None, None)

    def get_ReadOnly(self):
        return self.textBox.isReadOnly()
    def set_ReadOnly(self, bool):
        self.textBox.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_Enabled(self):
        return self.textBox.isEnabled()
    def set_Enabled(self, bool):
        self.textBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)
    
    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)
