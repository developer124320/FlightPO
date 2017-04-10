# -*- coding: UTF-8 -*-
'''
Created on 1 July 2016

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel

class DlgQaComment(QDialog):
    def __init__(self, parent = None, string_0 = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70)
        self.setWindowTitle("Edit Comment")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.txtComment = TextBoxPanel(self)
        self.txtComment.Caption = ""
        self.txtComment.LabelWidth = 0
        verticalLayoutDlg.addWidget(self.txtComment)

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)
        self.connect(self.txtComment, SIGNAL("Event_0"), self.txtComment_TextChanged)

        self.txtComment.Value = string_0
        self.btnOK.setEnabled(False)
    def chbLimit_Event_0(self):
        self.txtLimit.Enabled = self.chbLimit.Checked

    def acceptDlg(self):
        self.accept()

    def txtComment_TextChanged(self):
        self.btnOK.setEnabled(self.txtComment.Value.trimmed() != "");

    def getComment(self):
        return self.txtComment.Value
    Comment = property(getComment, None, None, None)

