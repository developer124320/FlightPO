# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QSizePolicy, QVBoxLayout, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtCore import  SIGNAL
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.CheckedListBox import CheckedListBox
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.validations import Validations
from Type.FasDataBlockFile import FasDataBlockFile

from Type.QA.QaHeadingColumns import QaHeadingColumns


class DlgQaHeading(QDialog):
    rowLimit = 0
    ignoreNAcolumns = False
    def __init__(self, parent = None, bool_0 = None):
        QDialog.__init__(self, parent)
        
        self.resize(100, 70)
        self.setWindowTitle("QA Entry")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"))

        self.groupBox = GroupBox(self)
        self.groupBox.Caption = ""
        verticalLayoutDlg.addWidget(self.groupBox)

        # self.lblHeading = TextBoxPanel(self.groupBox)
        # self.lblHeading.Enabled = False
        # self.lblHeading.Caption = "Title"
        # self.lblHeading.LabelWidth = 120
        # self.groupBox.Add = self.lblHeading

        self.txtHeading = TextBoxPanel(self.groupBox)
        self.txtHeading.Caption = "Title"
        self.txtHeading.LabelWidth = 120
        self.txtHeading.Width = 200
        self.groupBox.Add = self.txtHeading

        self.chbLimit = CheckBox(self.groupBox)
        self.chbLimit.Caption = "Limit # of table entries to"
        self.groupBox.Add = self.chbLimit

        self.gbColumns = GroupBox(self.groupBox)
        self.groupBox.Add = self.gbColumns

        self.lstColumns = CheckedListBox(self.gbColumns)
        self.gbColumns.Add = self.lstColumns

        self.txtLimit = TextBoxPanel(self.groupBox)
        self.txtLimit.Caption = ""
        self.txtLimit.LabelWidth = 0
        self.txtLimit.Width = 200
        # self.txtLimit.LabelWidth = 120
        self.chbLimit.hLayout.addWidget(self.txtLimit)

        self.chbIgnoreNA = CheckBox(self.groupBox)
        self.chbIgnoreNA.Caption = "Ignore columns containing \"N/A\" values"
        self.groupBox.Add = self.chbIgnoreNA

        self.btnBoxOkCancel = QDialogButtonBox(self)
        self.btnBoxOkCancel.setObjectName(("btnBoxOkCancel"))
        self.btnBoxOkCancel.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        # btnOK = self.btnBoxOkCancel.button(QDialogButtonBox.Ok)
        # btnOK.setText("Create")
        self.connect(self.btnBoxOkCancel, SIGNAL("accepted()"), self.acceptDlg)
        self.connect(self.btnBoxOkCancel, SIGNAL("rejected()"), self.reject)


        verticalLayoutDlg.addWidget(self.btnBoxOkCancel)

        if bool_0 != None:
            if (bool_0):
                # int width = base.ClientSize.Width
                # System.Drawing.Size clientSize = base.ClientSize
                # base.ClientSize = new System.Drawing.Size(width, clientSize.Height - (this.gbColumns.Bottom - this.txtHeading.Bottom))
                self.chbLimit.Visible = False
                self.txtLimit.Visible = False
                self.chbIgnoreNA.Visible = False
                self.gbColumns.Visible = False
            self.connect(self.chbLimit, SIGNAL("Event_0"), self.chbLimit_Event_0)
        else:
            DlgQaHeading.rowLimit = 10
            DlgQaHeading.ignoreNAcolumns = True
    def chbLimit_Event_0(self):
        self.txtLimit.Enabled = self.chbLimit.Checked

    def acceptDlg(self):
        flag = False
        if self.txtHeading.Value == None and self.txtHeading.Value == "":
            QMessageBox.information(self, "Information", "Please input the title.");
            return
        if (self.gbColumns.Visible):
            if self.txtLimit.Value == "":
                QMessageBox.information(self, "Information", "Please input the limit.");
                return
            try:
                num = int(self.txtLimit.Value)
                if num < 0:
                    QMessageBox.information(self, "Information", "Limit must be positive. \n Please try again.");
                    return
            except:
                QMessageBox.information(self, "Information", "Limit must be number. \n Please try again.");
                return

            if (len(self.lstColumns.CheckedItems) == 0):
                QMessageBox.warning(self, "Information", Validations.PLEASE_SELECT_AT_LEAST_1_COLUMN);
                return
        self.accept()

    def getColumns(self):
        qaHeadingColumn = QaHeadingColumns()
        for item in self.lstColumns.Items:
            qaHeadingColumn.Add(item)
        return qaHeadingColumn
    def setColumns(self, columns):
        self.lstColumns.Clear()
        for qaHeadingColumn in columns:
            self.lstColumns.Add(qaHeadingColumn, qaHeadingColumn.Selected)
    Columns = property(getColumns, setColumns, None, None)

    def getHeading(self):
        return self.txtHeading.Value
    def setHeading(self, val):
        self.txtHeading.Value = val
    Heading = property(getHeading, setHeading, None, None)

    def getIgnoreNAcolumns(self):
        return DlgQaHeading.ignoreNAcolumns
    def setIgnoreNAcolumns(self, val):
        DlgQaHeading.ignoreNAcolumns = val
    IgnoreNAcolumns = property(getIgnoreNAcolumns, setIgnoreNAcolumns, None, None)

    def getRowLimit(self):
        return DlgQaHeading.rowLimit
    def setRowLimit(self, val):
        if val > 0:
            DlgQaHeading.rowLimit = val
    RowLimit = property(getRowLimit, setRowLimit, None, None)

    def getLimit(self):
        num = None
        if (self.txtLimit.Enabled):
            try:
                return int(self.txtLimit.Value)
            except:
                pass
        return -1
    def setLimit(self, val):
        if (val <= 0):
            self.txtLimit.Value = ""
            return
        self.txtLimit.Value = str(val)
    Limit = property(getLimit, setLimit, None, None)

    @staticmethod
    def smethod_0(iwin32Window_0, string_0):
        flag = False
        dlgQaHeading = DlgQaHeading(iwin32Window_0, True)
        dlgQaHeading.Heading = string_0
        resultDlg = dlgQaHeading.exec_()
        if (not resultDlg == QDialog.Accepted):
            return False, None
        else:
            string_0 = dlgQaHeading.Heading
            flag = True
        return flag, string_0

    @staticmethod
    def smethod_1(iwin32Window_0, string_0, int_0, qaHeadingColumns_0):
        flag = False
        dlgQaHeading = DlgQaHeading(iwin32Window_0, False)
        dlgQaHeading.Heading = string_0
        if (int_0 >= DlgQaHeading.rowLimit):
            dlgQaHeading.Limit = DlgQaHeading.rowLimit
        else:
            dlgQaHeading.Limit = int_0
        dlgQaHeading.Columns = qaHeadingColumns_0
        dlgQaHeading.chbIgnoreNA.Checked = DlgQaHeading.IgnoreNAcolumns
        resultDlg = dlgQaHeading.exec_()
        limit = None
        if (not resultDlg == QDialog.Accepted):
            return False, string_0, int_0, qaHeadingColumns_0
        else:
            string_0 = dlgQaHeading.Heading
            limit = dlgQaHeading.Limit
            if (limit >= 0 and limit < int_0):
                int_0 = limit
            DlgQaHeading.IgnoreNAcolumns = dlgQaHeading.chbIgnoreNA.Checked
            flag = True
        return flag, string_0, int_0, qaHeadingColumns_0