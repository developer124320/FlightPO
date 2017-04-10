'''
Created on 12 Jul 2015

@author: Administrator
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from FlightPlanner.IasHelp.ui_IasHelp import ui_IasHelpDlg
class IasHelpDlg(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.uiLogInDialog = ui_IasHelpDlg()
        self.uiLogInDialog.setupUi(self)