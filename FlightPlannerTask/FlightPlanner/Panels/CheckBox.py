# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QCheckBox, QWidget, QHBoxLayout, QSizePolicy, QDialog
from PyQt4.QtCore import SIGNAL, QSize

class CheckBox(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("CheckBox" + str(len(parent.findChildren(CheckBox))))

        self.hLayout = QHBoxLayout(self)
        self.hLayout.setObjectName("hLayout")
        self.hLayout.setSpacing(0)
        self.hLayout.setContentsMargins(0,0,0,0)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.checkBox = QCheckBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.checkBox.setObjectName(self.objectName() + "_checkbox")
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.hLayout.addWidget(self.checkBox)
        self.checkBox.setChecked(True)
        self.checkBox.clicked.connect(self.clicked)

    def clicked(self):
        self.emit(SIGNAL("Event_0"), self)
    def get_Caption(self):
        return self.checkBox.text()
    def set_Caption(self, captionStr):
        self.checkBox.setText(captionStr)
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Enabled(self):
        return self.isEnabled()
    def set_Enabled(self, bool):
        self.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def get_Checked(self):
        return self.checkBox.isChecked()
    def set_Checked(self, bool):
        self.checkBox.setChecked(bool)
    Checked = property(get_Checked, set_Checked, None, None)

    def set_LabelWidth(self, width):
        self.checkBox.setMinimumSize(QSize(width, 0))
        self.checkBox.setMaximumSize(QSize(width, 16777215))
    LabelWidth = property(None, set_LabelWidth, None, None)