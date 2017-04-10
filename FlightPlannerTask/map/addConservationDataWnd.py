'''
Created on Aug 18, 2014

@author: JIN
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class addDataWnd(QDialog):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''       
        QDialog.__init__(self)
        self.setResult(QDialog.Rejected)
        self.setFixedWidth(500)
        self.setFixedHeight(300)       
      
        carLayout = QGridLayout()
             
        self.textedit1=QLineEdit()
        self.textedit2=QLineEdit()
        self.textedit3=QLineEdit()        
        
        self.textedit1.setFixedWidth(300)
        self.textedit1.setFixedHeight(30)
        button1=QPushButton("...")
        button1.setFixedWidth(30)
        button1.setFixedHeight(30)
        label1=QLabel("Area Shape file :")        
        carLayout.addWidget(label1, 0, 0)       
        carLayout.addWidget(self.textedit1, 0, 1)
        carLayout.addWidget(button1, 0, 2)
        
        self.textedit2.setFixedWidth(300)
        self.textedit2.setFixedHeight(30)
        button2=QPushButton("...")
        button2.setFixedWidth(30)
        button2.setFixedHeight(30)
        label2=QLabel("Forest Shape File :")        
        carLayout.addWidget(label2, 1, 0)       
        carLayout.addWidget(self.textedit2, 1, 1)
        carLayout.addWidget(button2, 1, 2) 
           
#         self.textedit3.setFixedWidth(300)        
#         self.textedit3.setFixedHeight(30)
#         button3=QPushButton("...")
#         button3.setFixedWidth(30)
#         button3.setFixedHeight(30)
#         label3=QLabel("Species Point Shape File :")        
#         carLayout.addWidget(label3, 2, 0)       
#         carLayout.addWidget(self.textedit3, 2, 1)
#         carLayout.addWidget(button3, 2, 2)                
               
        vBoxLayout=QVBoxLayout()
        vBoxLayout.addLayout(carLayout)             
              
        buttonRun=QPushButton("Add")
        buttonRun.setFixedWidth(100)
        buttonRun.setFixedHeight(30)             
        vBoxLayout.addWidget(buttonRun)    
        
        self.setLayout(vBoxLayout)
        
        self.connect(button1, SIGNAL("clicked()"), self.openShapeFile1)
        self.connect(button2, SIGNAL("clicked()"), self.openShapeFile2)
#         self.connect(button3, SIGNAL("clicked()"), self.openShapeFile3)        
        self.connect(buttonRun, SIGNAL("clicked()"), self.running) 
    def openShapeFile1(self):
        file = QFileDialog.getOpenFileName(self, "Open ShapeFile",QCoreApplication.applicationDirPath (),"Shapefiles(*.shp *.geojson)")        
        self.textedit1.setText(file)
        if file=="":
            return
    def openShapeFile2(self):
        file = QFileDialog.getOpenFileName(self, "Open ShapeFile",QCoreApplication.applicationDirPath (),"Shapefiles(*.shp *.geojson)")        
        self.textedit2.setText(file)
        if file=="":
            return
#     def openShapeFile3(self):
#         file = QFileDialog.getOpenFileName(self, "Open ShapeFile",QCoreApplication.applicationDirPath (),"Shapefiles(*.shp *.geojson)")        
#         self.textedit3.setText(file)
#         if file=="":
#             return
    def running(self):
        #self.setResult(QDialog.Accepted)
        self.done(1)