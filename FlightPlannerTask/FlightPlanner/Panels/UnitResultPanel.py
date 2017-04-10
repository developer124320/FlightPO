'''
Created on Mar 18, 2015

@author: jin
'''

from PyQt4.QtGui import QFrame, QSizePolicy, QLabel, QHBoxLayout, QFont, QLineEdit, QComboBox, QMessageBox
from PyQt4.QtCore import QSize
class UnitResultPanel(QFrame):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
#         self.frame_WindIA = QFrame(parent)
        horizontalLayout_100 = QHBoxLayout(self);
        horizontalLayout_100.setSpacing(0);
        horizontalLayout_100.setContentsMargins(0, 0, 0, 0);
        horizontalLayout_100.setObjectName("horizontalLayout_100")
        self.txtSurface = QLineEdit(self);
        self.txtSurface.setObjectName("txtSurface")
        font = QFont()
        font.setFamily("Arial")
        self.txtSurface.setFont(font);

        horizontalLayout_100.addWidget(self.txtSurface);

        self.txtResult = QLineEdit(self);
        self.txtResult.setObjectName("txtOCHResults")
        self.txtResult.setFont(font);

        horizontalLayout_100.addWidget(self.txtResult);
