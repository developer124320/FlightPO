# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QSpacerItem, QMessageBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
class DegreesBoxPanel(QWidget):
    def __init__(self, parent , boxType = None):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("DegreesBoxPanel" + str(len(parent.findChildren(DegreesBoxPanel))))


        self.hLayoutDegreesBoxPanel = QHBoxLayout(self)
        self.hLayoutDegreesBoxPanel.setSpacing(0)
        self.hLayoutDegreesBoxPanel.setContentsMargins(0,0,0,0)
        self.hLayoutDegreesBoxPanel.setObjectName(("hLayoutDegreesBoxPanel"))
        self.frameDegreesBoxPanel = QFrame(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameDegreesBoxPanel.sizePolicy().hasHeightForWidth())
        self.frameDegreesBoxPanel.setSizePolicy(sizePolicy)
        self.frameDegreesBoxPanel.setFrameShape(QFrame.NoFrame)
        self.frameDegreesBoxPanel.setFrameShadow(QFrame.Raised)
        self.frameDegreesBoxPanel.setObjectName(("frameDegreesBoxPanel"))
        self.hLayoutFrameDegreesBoxPanel = QHBoxLayout(self.frameDegreesBoxPanel)
        self.hLayoutFrameDegreesBoxPanel.setSpacing(0)
        self.hLayoutFrameDegreesBoxPanel.setMargin(0)
        self.hLayoutFrameDegreesBoxPanel.setObjectName(("hLayoutFrameDegreesBoxPanel"))
        self.captionLabel = QLabel(self.frameDegreesBoxPanel)
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
        self.hLayoutFrameDegreesBoxPanel.addWidget(self.captionLabel)
        self.frameDegreesBoxPanelIn = QFrame(self.frameDegreesBoxPanel)
        self.frameDegreesBoxPanelIn.setFrameShape(QFrame.StyledPanel)
        self.frameDegreesBoxPanelIn.setFrameShadow(QFrame.Raised)
        self.frameDegreesBoxPanelIn.setObjectName(("frameDegreesBoxPanelIn"))
        self.hLayoutFrameDegreesBoxPanelIn = QHBoxLayout(self.frameDegreesBoxPanelIn)
        self.hLayoutFrameDegreesBoxPanelIn.setSpacing(0)
        self.hLayoutFrameDegreesBoxPanelIn.setMargin(0)
        self.hLayoutFrameDegreesBoxPanelIn.setObjectName(("hLayoutFrameDegreesBoxPanelIn"))
        self.txtDegreeBox = QLineEdit(self.frameDegreesBoxPanelIn)
        self.txtDegreeBox.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtDegreeBox.setFont(font)
        self.txtDegreeBox.setObjectName(self.objectName() + "_txtDegreeBox")
        self.txtDegreeBox.setText("0.0")
        self.txtDegreeBox.setMinimumWidth(70)
        self.txtDegreeBox.setMaximumWidth(70)
        self.hLayoutFrameDegreesBoxPanelIn.addWidget(self.txtDegreeBox)
        self.btnDegreeBoxPanel = QToolButton(self.frameDegreesBoxPanelIn)
        self.btnDegreeBoxPanel.setText((""))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/Calculator.bmp")), QIcon.Normal, QIcon.Off)
        self.btnDegreeBoxPanel.setIcon(icon)
        self.btnDegreeBoxPanel.setObjectName(("btnDegreeBoxPanel"))
        self.hLayoutFrameDegreesBoxPanelIn.addWidget(self.btnDegreeBoxPanel)
        self.hLayoutFrameDegreesBoxPanel.addWidget(self.frameDegreesBoxPanelIn)
        self.hLayoutDegreesBoxPanel.addWidget(self.frameDegreesBoxPanel)

        spacerItem = QSpacerItem(10,10,QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayoutDegreesBoxPanel.addItem(spacerItem)


        self.btnDegreeBoxPanel.clicked.connect(self.btnDegreeBoxPanel_clicked)
        self.txtDegreeBox.textChanged.connect(self.txtDegreeBox_textChanged)

        self.boxType = boxType
        self.value = 0.0
    def txtDegreeBox_textChanged(self):
        try:
            test = float(self.txtDegreeBox.text())
            self.emit(SIGNAL("txtDegreeBox_textChanged"), self)
        except:
            str0 = "You must input the float type in \"%s\"."%(self.Caption)
            QMessageBox.warning(self, "Warning" , str0)
            self.txtDegreeBox.setText("0.0")

    def btnDegreeBoxPanel_clicked(self):
        self.emit(SIGNAL("btnDegreeBoxPanel_clicked"), self)

    def btnDegreeBoxPanel_visible(self, bool):
        self.btnDegreeBoxPanel.setVisible(bool)
    ButtonVisible = property(None, btnDegreeBoxPanel_visible, None, None)

    def get_Value(self):
        try:
            return float(self.txtDegreeBox.text())
        except:
            return 0.0

    def set_Value(self, value):
        self.txtDegreeBox.setText(str(value))
    Value = property(get_Value, set_Value, None, None)

    # def set_Enabled(self, bool):
    #     self.txtDegreeBox.setEnabled(bool)
    # Enabled = property(None, set_Enabled, None, None)
    
    def set_CaptionLabel(self, labelString):
        self.captionLabel.setText(labelString + ":")
    CaptionLabel = property(None, set_CaptionLabel, None, None)

    def set_LabelWidth(self, width):
        self.captionLabel.setMinimumSize(QSize(width, 0))
        self.captionLabel.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)

    def get_ReadOnly(self):
        return self.txtDegreeBox.isReadOnly()
    def set_ReadOnly(self, bool):
        self.txtDegreeBox.setReadOnly(bool)
    ReadOnly = property(get_ReadOnly, set_ReadOnly, None, None)

    def get_Enabled(self):
        return self.txtDegreeBox.isEnabled()
    def set_Enabled(self, bool):
        self.txtDegreeBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

