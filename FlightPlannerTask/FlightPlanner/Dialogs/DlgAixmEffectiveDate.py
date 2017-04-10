# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDateTimeEdit, QDialogButtonBox, QCalendarWidget

from PyQt4.QtCore import  SIGNAL, QDateTime
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.types import ListInsertPosition, CodeTypeDesigPtAixm, DegreesType
from FlightPlanner.validations import Validations
from Type.Degrees import Degrees
from Type.ProcEntity import ProcEntityDPN



class DlgAixmEffectiveDate(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Effective Date")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));

        self.groupBox = GroupBox(self)
        verticalLayoutDlg.addWidget(self.groupBox)

        self.dtpDate = QDateTimeEdit(self.groupBox);
        self.dtpDate.setObjectName(("dtpDate"));
        self.dtpDate.setDateTime(QDateTime.currentDateTime())
        self.groupBox.Add = self.dtpDate

        self.calendar = QCalendarWidget(self.groupBox)
        self.groupBox.Add = self.calendar
        self.calendar.clicked.connect(self.calendar_clicked)

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"));
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        # btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)

        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

    def calendar_clicked(self, date):
        self.dtpDate.setDate(date)

    def get_DateTime(self):
        return self.dtpDate.dateTime()
    def set_DateTime(self, dateTime):
        if dateTime != None:
            self.dtpDate.setDateTime(dateTime)
            self.calendar.setCurrentPage(dateTime.date().year(), dateTime.date().month())

    DateTime = property(get_DateTime, set_DateTime, None, None)

    def acceptDlg(self):
        self.accept()

    @staticmethod
    def smethod_0(dateTime_0):
        flag = False;
        dlgAixmEffectiveDate = DlgAixmEffectiveDate()
        dlgAixmEffectiveDate.dtpDate.setDateTime(dateTime_0)
        resultDlg = dlgAixmEffectiveDate.exec_()
        if (resultDlg != 1):
            return False, dateTime_0;
        else:
            dateTime_0 = dlgAixmEffectiveDate.DateTime;
            flag = True;
        return flag, dateTime_0;