'''
Created on Aug 20, 2014

@author: JIN
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class cellsizeWnd(QDialog):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.cellsize=2.0
        QDialog.__init__(self)
        carLayout = QGridLayout()
        self.setFixedWidth(300)
        self.setFixedHeight(150)
        self.textedit1=QLineEdit()
        self.textedit1.setFixedWidth(200)
        self.textedit1.setFixedHeight(30)
        self.textedit1.setText("2.0")
        button1=QPushButton("OK")
        button1.setFixedWidth(50)
        button1.setFixedHeight(30)
#         button2=QPushButton("Cancel")
#         button2.setFixedWidth(50)
#         button2.setFixedHeight(30)
        label1=QLabel("Cell Size(Km) :")
        carLayout.addWidget(label1, 0, 0)       
        carLayout.addWidget(self.textedit1, 0, 1)
        carLayout.addWidget(button1, 1, 0)       
#         carLayout.addWidget(button2, 1, 1)
        self.setLayout(carLayout)
        self.connect(button1, SIGNAL("clicked()"), self.insert)
        #self.connect(button2, SIGNAL("clicked()"), self.close)
    def insert(self):
        self.cellsize = float(self.textedit1.text())
        self.done(1)