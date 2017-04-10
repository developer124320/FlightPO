'''
Created on Feb 9, 2015

@author: Administrator
'''
from PyQt4.QtGui import QDialog

class IlsOas(QDialog):
    
    obstacles = None
    obstaclesChecked = 0
    constants = None
    resultOCH = 0
    resultOCA = 0
    resultSocText = None
    resultCriticalObst = None

    def __init__(self):
        QDialog.__init__(self)