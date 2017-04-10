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


    def __init__(self,cellSize,cellCount,calcTime):
        '''
        Constructor
        '''
        self.cellsize = int(round(cellSize,1))

        self.cellCount = cellCount
        self.calcTime = calcTime
        self.initCellSize = int(round(self.cellsize, 1))
        self.cellRate = 1
        QDialog.__init__(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.lblWarning = QLabel("Number of calculation points is %i.Please change the cell size."%int(self.cellCount))
        
        layout.addWidget(self.lblWarning)
        frame = QFrame(self)
        frmLayout = QHBoxLayout()
        frame.setLayout(frmLayout)
        self.label1=QLabel("Cell Size(m) :")
        frmLayout.addWidget(self.label1)
        self.textedit1=QLineEdit()
        self.textedit1.setFixedWidth(150)
        self.textedit1.setFixedHeight(20)
        self.textedit1.setText(str(self.cellsize))
        self.spinBox=QSpinBox()
        self.spinBox.setFixedWidth(150)
        self.spinBox.setFixedHeight(20)
#         self.spinBox.setReadOnly(True)
        if self.cellsize != 1: 
            self.spinBox.setSingleStep(int(round(self.cellsize, 1)))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setValue(int(round(self.cellsize, 1)))
        frmLayout.addWidget(self.spinBox)
        layout.addWidget(frame)
        buttonBox = QDialogButtonBox(self);
        buttonBox.setObjectName("buttonBox")
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);

        layout.addWidget(buttonBox)
        
        self.connect(buttonBox, SIGNAL("accepted()"), self.acceptDialog)
        self.connect(buttonBox, SIGNAL("rejected()"), self.rejectDialog)
        self.spinBox.valueChanged.connect(self.valueChanged)


    def acceptDialog(self):
#         try:
        if self.spinBox.value() == 0:
            return
        
        self.cellCount = int(round(self.cellCount * self.cellsize / float(self.spinBox.value())* (self.cellsize / float(self.spinBox.value())), 1))            
        self.cellsize = self.spinBox.value()
        self.cellRate = int(self.spinBox.value() / self.initCellSize)
        self.done(1)
#         except:
#             QMessageBox.warning(self, "Error", "Input the number!")
        
    def rejectDialog(self):
        self.done(0)
    def valueChanged(self, value):
#         try:
        cellNum = int(round(self.cellCount * self.cellsize / float(value)*(self.cellsize / float(value)), 1))
        
        self.calcTime = cellNum * 0.03
        self.lblWarning.setText("Number of calculation points is %i.Please change the cell size."%int(cellNum))
#             self.done(1)
#         except:
#             QMessageBox.warning(self, "Error", "Input the number!")