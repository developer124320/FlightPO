# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QVBoxLayout, QGroupBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog, QDateEdit,QComboBox, \
    QDialogButtonBox, QMenu, QCalendarWidget
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.QgisHelper import Point3D
from FlightPlanner.captureCoordinateTool import CaptureCoordinateTool, CaptureCoordinateToolUpdate
from qgis.gui import QgsMapToolPan
from qgis.core import QgsPoint, QGis
from FlightPlanner.helpers import Unit, Altitude
from FlightPlanner.QgisHelper import QgisHelper

import define



class DlgMagneticVariationParameters(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        
        self.resize(290, 136);
        self.setWindowTitle("Reference Positions")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth());
        self.setSizePolicy(sizePolicy);
        verticalLayoutDlg = QVBoxLayout(self)
        verticalLayoutDlg.setObjectName(("verticalLayoutDlg"));
        frameDate = QFrame(self);
        frameDate.setObjectName(("frameDate"));
        frameDate.setFrameShape(QFrame.StyledPanel);
        frameDate.setFrameShadow(QFrame.Raised);
        horizontalLayoutDate = QHBoxLayout(frameDate);
        horizontalLayoutDate.setObjectName(("horizontalLayoutDate"));
        labelDate = QLabel(frameDate);
        labelDate.setObjectName(("labelDate"));
        labelDate.setMinimumSize(QSize(70, 0));
        labelDate.setMaximumSize(QSize(70, 16777215));
        labelDate.setText("Date:")

        horizontalLayoutDate.addWidget(labelDate);

        self.dtpDate = QDateEdit(frameDate);
        self.dtpDate.setObjectName(("dtpDate"));

        horizontalLayoutDate.addWidget(self.dtpDate);

        self.btnDtpDate =  QToolButton(frameDate);
        self.btnDtpDate.setObjectName(("btnDtpDate"));
        sizePolicy.setHeightForWidth(self.btnDtpDate.sizePolicy().hasHeightForWidth());
        self.btnDtpDate.setSizePolicy(sizePolicy);
        self.btnDtpDate.setMinimumSize(QSize(25, 0));
        self.btnDtpDate.setMaximumSize(QSize(25, 16777215));
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/calender.png")), QIcon.Normal, QIcon.Off)
        self.btnDtpDate.setIcon(icon)

        horizontalLayoutDate.addWidget(self.btnDtpDate);


        verticalLayoutDlg.addWidget(frameDate);

        frameModel = QFrame(self);
        frameModel.setObjectName(("frameModel"));
        frameModel.setFrameShape(QFrame.StyledPanel);
        frameModel.setFrameShadow(QFrame.Raised);
        horizontalLayoutModel = QHBoxLayout(frameModel);
        horizontalLayoutModel.setObjectName(("horizontalLayoutModel"));
        labelModel = QLabel(frameModel);
        labelModel.setObjectName(("labelModel"));
        labelModel.setMinimumSize(QSize(70, 0));
        labelModel.setMaximumSize(QSize(70, 16777215));
        labelModel.setText("Model:")

        horizontalLayoutModel.addWidget(labelModel);

        self.cmbModel = QComboBox(frameModel);
        self.cmbModel.setObjectName(("cmbModel"));

        horizontalLayoutModel.addWidget(self.cmbModel);


        verticalLayoutDlg.addWidget(frameModel);

        self.buttonBox = QDialogButtonBox(self);
        self.buttonBox.setObjectName(("buttonBox"));
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok);
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)


        verticalLayoutDlg.addWidget(self.buttonBox);

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.calendar_clicked)
        self.menu = QMenu()
        layout = QVBoxLayout(self.menu)
        layout.addWidget(self.calendar)

        self.btnDtpDate.clicked.connect(self.btnDtpDate_clicked)
        self.cmbModel.addItems(["WMM2015", "WMM2010" , "WMM2005", "WMM2000", "WMM95", "WMM90", "WMM85", "IGRF2000", "IGRF95", "IGRF90"])

    def btnDtpDate_clicked(self):
        rcRect = self.btnDtpDate.geometry()
        ptPoint = rcRect.bottomLeft()

        self.menu.exec_( self.mapToGlobal(ptPoint) )

    def calendar_clicked(self, date):
        self.dtpDate.setDate(date)

    def get_Date(self):
        return self.dtpDate.date()
    def setDate(self, date):
        if date != None:
            self.dtpDate.setDate(date)
    Date = property(get_Date, setDate, None, None)

    def get_Model(self):
        return self.cmbModel.currentIndex()
    def set_Model(self, index):
        if index == None:
            self.cmbModel.setCurrentIndex(1)
            return
        self.cmbModel.setCurrentIndex(index)
    Model = property(get_Model, set_Model, None, None)

    @staticmethod
    def smethod_0(date_0, magneticModelIndex_0):

        dlgMagneticVariationParameters = DlgMagneticVariationParameters()
        dlgMagneticVariationParameters.Date = date_0
        dlgMagneticVariationParameters.Model = magneticModelIndex_0
        dialogResult = dlgMagneticVariationParameters.exec_()
        if dialogResult != QDialog.Accepted:
            return (False, None, None)
        else:
            date  = dlgMagneticVariationParameters.Date;
            magneticIndex = dlgMagneticVariationParameters.Model;
            return (True, date, magneticIndex)

