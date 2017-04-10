'''
Created on 15 Jul 2015

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QPlainTextEdit, QVBoxLayout, QFont
# from PyQt4.QtCore import QFont
class tabControl(QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        QWidget.__init__(self, parent)
        
        self.resize(349, 400)
        verticalLayout = QVBoxLayout(self)
        verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QPlainTextEdit(self)
        self.plainTextEdit.setObjectName("plainTextEdit")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.plainTextEdit.setFont(font)
#         self.plainTextEdit.setReadOnly(True);

        verticalLayout.addWidget(self.plainTextEdit)
        