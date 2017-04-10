'''
Created on 12 Jul 2015

@author: Administrator
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from FlightPlanner.SelectFly.ui_SelectFlyDlg import Ui_SelectFly
class SelectFlyDlg(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui_SelectFly = Ui_SelectFly()
        self.ui_SelectFly.setupUi(self)
        self.setWindowTitle("Select Dialog")
        self.ui_SelectFly.btnOK.clicked.connect(self.accept)
    def get_SelectWptFly1(self):
        return 0 if self.ui_SelectFly.rBtnFlyby1.isChecked() else 1
    def set_SelectWptFly1(self, flyValue):
        if flyValue == 0:
            self.ui_SelectFly.rBtnFlyby1.setChecked(True)
        else:
            self.ui_SelectFly.rBtnFlyby1.setChecked(False)
    FlyWpt1 = property(get_SelectWptFly1,set_SelectWptFly1,None, None)

    def get_SelectWptFly2(self):
        return 0 if self.ui_SelectFly.rBtnFlyby2.isChecked() else 1
    def set_SelectWptFly2(self, flyValue):
        if flyValue == 0:
            self.ui_SelectFly.rBtnFlyby2.setChecked(True)
        else:
            self.ui_SelectFly.rBtnFlyby2.setChecked(False)
    FlyWpt2 = property(get_SelectWptFly2,set_SelectWptFly2,None, None)