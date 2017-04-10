# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QFont, QLabel, QFrame, QDialog,\
    QHBoxLayout, QMessageBox, QLineEdit, QSpinBox
from PyQt4.QtCore import QString, QFileInfo, QSize
from PyQt4.QtCore import  SIGNAL, QCoreApplication
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.GroupBox import GroupBox
from Type.FasDataBlockFile import FasDataBlockFile


class DlgUserInputPanel(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.resize(100, 70);
        self.setWindowTitle("User Input Panel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox1 = GroupBox(self)
        self.groupBox1.Caption = ""
        verticalLayoutDlg.addWidget(self.groupBox1)

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
        self.captionLabel.setMinimumSize(QSize(60, 0))
        self.captionLabel.setMaximumSize(QSize(60, 16777215))
        self.captionLabel.setText("Radius:")
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.captionLabel.setFont(font)
        self.captionLabel.setObjectName(("captionLabel"))
        self.hLayoutframeBoxPanel.addWidget(self.captionLabel)

        self.spinBox = QLineEdit(self.frameBoxPanel)
        # self.spinBox.setMaximum(1000000000)
        # self.spinBox.setMinimum(-1000000000)
        self.spinBox.setText("0")
        self.spinBox.setMinimumSize(QSize(150, 0))

        self.hLayoutframeBoxPanel.addWidget(self.spinBox)

        self.groupBox1.Add = self.frameBoxPanel

    def getValue(self):
        return float(self.spinBox.text())

    def setValue(self, val):
        if isinstance(val, int) or isinstance(val, float):
            self.spinBox.setText(str(round(val, 4)))
    Value = property(getValue, setValue, None, None)





