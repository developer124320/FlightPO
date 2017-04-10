# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QPushButton, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QIcon, QPixmap, QDialog, QSpacerItem, QSpinBox
from PyQt4.QtCore import QSize, SIGNAL, QString

from Type.String import String

class NumberBoxPanel(QWidget):
    def __init__(self, parent, resoution = "0.0000"):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("NumberBoxPanel" + str(len(parent.findChildren(NumberBoxPanel))))


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

        if resoution != None:
            self.numberBox = QLineEdit(self.frameBoxPanel)
            self.numberBox.setEnabled(True)
            font = QFont()
            font.setBold(False)
            font.setWeight(50)
            self.numberBox.setFont(font)
            self.numberBox.setObjectName(self.objectName() + "_numberBox")
            self.numberBox.setText("0.0")
            self.numberBox.setMinimumWidth(70)
            self.numberBox.setMaximumWidth(70)
            self.hLayoutframeBoxPanel.addWidget(self.numberBox)
            self.numberBox.textChanged.connect(self.numberBoxChanged)
            self.numberBox.editingFinished.connect(self.numberBoxEditingFinished)
        else:
            self.numberBox = QSpinBox(self.frameBoxPanel)
            self.numberBox.setObjectName(self.objectName() + "_numberBox")
            self.numberBox.setMinimumWidth(70)
            self.numberBox.setMaximumWidth(70)
            self.numberBox.setMinimum(-100000000)
            self.numberBox.setMaximum(100000000)
            self.numberBox.setValue(1)
            self.hLayoutframeBoxPanel.addWidget(self.numberBox)

        self.imageButton = QPushButton(self.frameBoxPanel)

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


        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.numberResolution = resoution
        str0 = String.Number2String(6.6788, "0.0000")
        self.Value = 0
        self.captionUnits = ""
    def imageButtonClicked(self):
        self.emit(SIGNAL("Event_1"), self)
    def method_6(self, string_0):
        return "%s%s\t%f %s"%(string_0, self.Caption, self.Value, self.CaptionUnits);
    def numberBoxEditingFinished(self):
        self.emit(SIGNAL("editingFinished"), self)
    def numberBoxChanged(self):
        try:
            test = float(self.numberBox.text())
            self.emit(SIGNAL("Event_0"), self)
        except:
            if self.numberBox.text() == "" or self.numberBox.text() == "-" or self.numberBox.text() == "+":
                return
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.numberBox.setText("0.0")

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
        if self.CaptionUnits != "" and self.CaptionUnits != None:
            self.captionLabel.setText(QString(captionStr + "(") + self.CaptionUnits + QString("):"))
        else:
            self.captionLabel.setText(captionStr + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def get_Value(self):
        try:
            if self.numberResolution != None:
                return float(self.numberBox.text())
            else:
                return self.numberBox.value()
        except:
            return 0.0

    def set_Value(self, valueFloat):
        if self.numberResolution != None:
            if valueFloat == None or valueFloat == "":
                rStr = String.Number2String(0, self.numberResolution)
                self.numberBox.setText(rStr)
                return
            try:
                test = float(valueFloat)
                rStr = String.Number2String(test, self.numberResolution)
                self.numberBox.setText(rStr)
            except:
                str0 = "You must put the float type in \"%s\"."%(self.Caption)
                QMessageBox.warning(self, "Warning" , str0)
                rStr = String.Number2String(0, self.numberResolution)
                self.numberBox.setText(rStr)
        else:
            try:
                test = int(valueFloat)
                self.numberBox.setValue(test)
            except:
                str0 = "You must put the float type in \"%s\"."%(self.Caption)
                QMessageBox.warning(self, "Warning" , str0)
                self.numberBox.setValue(0)
    Value = property(get_Value, set_Value, None, None)

    # def get_IsEmpty(self):
    #     return self.numberBox.text() == "" or self.numberBox.text() == None
    # IsEmpty = property(get_IsEmpty, None, None, None)

    def get_ReadOnly(self):
        return self.numberBox.isReadOnly()
    def set_ReadOnly(self, bool):
        self.numberBox.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def set_Width(self, width):
        self.numberBox.setMinimumSize(QSize(width, 0))
        self.numberBox.setMaximumSize(QSize(width, 16777215))
    Width = property(None, set_Width, None, None)

    def get_Enabled(self):
        return self.isEnabled()
    def set_Enabled(self, bool):
        self.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def set_Button(self, imageName):
        if imageName == None or imageName == "":
            self.imageButton.setVisible(False)
            return
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/" + imageName)), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setVisible(True)
    Button = property(None, set_Button, None, None)
