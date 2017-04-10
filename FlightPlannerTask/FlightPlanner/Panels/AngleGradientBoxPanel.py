# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''


from PyQt4.QtGui import QWidget, QFrame, QPushButton, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QIcon, QPixmap, QDialog, QSpacerItem
from PyQt4.QtCore import QSize, SIGNAL
from Type.String import String
from FlightPlanner.helpers import AngleGradientSlope, AngleGradientSlopeUnits
import define

class AngleGradientBoxPanel(QWidget):
    def __init__(self, parent, resoution = None):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("AngleGradientBoxPanel" + str(len(parent.findChildren(AngleGradientBoxPanel))))
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
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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

        self.txtDegree = QLineEdit(self.frameBoxPanelIn)
        self.txtDegree.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDegree.setFont(font)
        self.txtDegree.setObjectName(self.objectName() + "_txtDegree")
        self.txtDegree.setText("0.0")
        self.txtDegree.setMinimumWidth(70)
        self.txtDegree.setMaximumWidth(70)
        self.hLayoutframeBoxPanelIn.addWidget(self.txtDegree)

        self.labelDegree = QLabel(self.frameBoxPanelIn)
        self.labelDegree.setObjectName(("labelDegree"))
        self.labelDegree.setText(" " + define._degreeStr + " ")
        self.hLayoutframeBoxPanelIn.addWidget(self.labelDegree)

        self.txtPercent = QLineEdit(self.frameBoxPanelIn)
        self.txtPercent.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtPercent.setFont(font)
        self.txtPercent.setObjectName(self.objectName() + "_txtPercent")
        self.txtPercent.setText("0.0")
        self.txtPercent.setMinimumWidth(70)
        self.txtPercent.setMaximumWidth(70)
        self.hLayoutframeBoxPanelIn.addWidget(self.txtPercent)

        self.labelPercent = QLabel(self.frameBoxPanelIn)
        self.labelPercent.setObjectName(("labelPercent"))
        self.labelPercent.setText(" %")
        self.hLayoutframeBoxPanelIn.addWidget(self.labelPercent)
        
        self.hLayoutframeBoxPanel.addWidget(self.frameBoxPanelIn)
        
        

        # self.angleGradientBox = QLineEdit(self.frameBoxPanel)
        # self.angleGradientBox.setEnabled(True)
        # font = QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.angleGradientBox.setFont(font)
        # self.angleGradientBox.setObjectName(("angleGradientBox"))
        # self.angleGradientBox.setText("0.0")
        # self.angleGradientBox.setMinimumWidth(70)
        # self.angleGradientBox.setMaximumWidth(70)
        # self.hLayoutframeBoxPanel.addWidget(self.angleGradientBox)

        self.imageButton = QPushButton(self.frameBoxPanel)
        self.imageButton.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/convex_hull.png")), QIcon.Normal, QIcon.Off)
        self.imageButton.setIcon(icon)
        self.imageButton.setObjectName(("imageButton"))
        self.imageButton.setVisible(False)
        self.hLayoutframeBoxPanel.addWidget(self.imageButton)

        self.hLayoutBoxPanel.addWidget(self.frameBoxPanel)

        spacerItem = QSpacerItem(0,0,QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.hLayoutBoxPanel.addItem(spacerItem)

        self.txtDegree.textChanged.connect(self.txtDegreeChanged)
        self.txtPercent.textChanged.connect(self.txtPercentChanged)
        self.imageButton.clicked.connect(self.imageButtonClicked)

        self.numberResolution = resoution
        str0 = String.Number2String(6.6788, "0.00000")

        self.captionUnits = ""
        self.hidePercentBox()
        self.flag = 0
    def txtPercentChanged(self):
        try:
            test = float(self.txtPercent.text())
            if self.flag==0:
                self.flag=1;
            if self.flag==2:
                self.flag=0;
            if self.flag==1:
                try:
                    self.txtDegree.setText(str(round(AngleGradientSlope(float(self.txtPercent.text()), AngleGradientSlopeUnits.Percent).Degrees, 4)))
                except:
                    self.txtDegree.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtDegree.setText("0.0")


    def txtDegreeChanged(self):
        try:
            test = float(self.txtDegree.text())
            if self.flag==0:
                self.flag=2;
            if self.flag==1:
                self.flag=0;
            if self.flag==2:
                try:
                    self.txtPercent.setText(str(round(AngleGradientSlope(float(self.txtDegree.text())).Percent, 4)))
                except:
                    self.txtPercent.setText("0.0")
                self.emit(SIGNAL("Event_0"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtPercent.setText("0.0")
    def hidePercentBox(self):
        self.txtPercent.setVisible(False)
        self.labelPercent.setVisible(False)
    def showPercentBox(self):
        self.txtPercent.setVisible(True)
        self.labelPercent.setVisible(True)
    def imageButtonClicked(self):
        self.emit(SIGNAL("Event_1"), self)
    def method_6(self, string_0):
        return "%s%s\t%f %s"%(string_0, self.Caption, self.Value, self.CaptionUnits);

    def ToString(self):
        caption = self.captionLabel.text();
        value = self.txtDegree.text();
        return "{0}, {1}".format(caption, value);

    def get_CaptionUnits(self):
        return self.captionUnits
    def set_CaptionUnits(self, captionUnits):
        self.captionUnits = captionUnits
    CaptionUnits = property(get_CaptionUnits, set_CaptionUnits, None, None)

    def get_Caption(self):
        caption = self.captionLabel.text()
        # findIndex = caption.indexOf("(")
        # if findIndex > 0:
        #     val = caption.left(findIndex)
        #     return val
        return caption
    def set_Caption(self, captionStr):
        self.captionLabel.setText(captionStr + ":")
        # value = ""
        # if self.captionUnits == AngleGradientSlopeUnits.Degrees:
        #     value = captionStr + "(" + define._degreeStr + ")"
        # elif self.captionUnits == AngleGradientSlopeUnits.Percent:
        #     value = captionStr + "(%)"
        # elif self.captionUnits == AngleGradientSlopeUnits.Slope:
        #     value = captionStr + "(1:)"
        # self.captionLabel.setText(value + ":")
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    # def get_IsEmpty(self):
    #     return self.angleGradientBox.text() == ""
    # IsEmpty = property(get_IsEmpty, None, None, None)

    def get_Value(self):
        return AngleGradientSlope(float(self.txtDegree.text()))
        # if self.captionUnits == AngleGradientSlopeUnits.Degrees:
        #     try:
        #         return AngleGradientSlope(float(self.angleGradientBox.text()))
        #     except:
        #         return None
        # elif self.captionUnits == AngleGradientSlopeUnits.Percent:
        #     try:
        #         return AngleGradientSlope(float(self.angleGradientBox.text()), AngleGradientSlopeUnits.Percent)
        #     except:
        #         return None
        # elif self.captionUnits == AngleGradientSlopeUnits.Slope:
        #     try:
        #         return AngleGradientSlope(float(self.angleGradientBox.text()), AngleGradientSlopeUnits.Slope)
        #     except:
        #         return None

    def set_Value(self, value):
        if isinstance(value, AngleGradientSlope):
            self.txtDegree.setText(str(round(value.Degrees, 4)))
            return
            # if self.captionUnits == AngleGradientSlopeUnits.Degrees:
            #     rStr = String.Number2String(value.Degrees, self.numberResolution)
            #     self.angleGradientBox.setText(rStr)
            # elif self.captionUnits == AngleGradientSlopeUnits.Percent:
            #     rStr = String.Number2String(value.Percent, self.numberResolution)
            #     self.angleGradientBox.setText(rStr)
            # elif self.captionUnits == AngleGradientSlopeUnits.Slope:
            #     rStr = String.Number2String(value.Slope, self.numberResolution)
            #     self.angleGradientBox.setText(rStr)
            # return



        try:
            test = float(value)
            rStr = String.Number2String(test, self.numberResolution)
            self.txtDegree.setText(rStr)
        except:
            str0 = "You must put the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            # rStr = String.Number2String(0, self.numberResolution)
            self.txtDegree.setText("0.0")
    Value = property(get_Value, set_Value, None, None)

    # def get_IsEmpty(self):
    #     return self.angleGradientBox.text() == "" or self.angleGradientBox.text() == None
    # IsEmpty = property(get_IsEmpty, None, None, None)

    def get_ReadOnly(self):
        return self.txtDegree.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtDegree.setReadOnly(bool)
        self.txtPercent.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

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