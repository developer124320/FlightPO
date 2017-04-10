# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_GeoDeterminePosition.ui'
#
# Created: Mon Mar 07 18:59:10 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, SpeedUnits, Speed
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_GeoDetermine(object):
    def setupUi(self, GeoDetermine):
        GeoDetermine.setObjectName(_fromUtf8("GeoDetermine"))
        GeoDetermine.resize(483, 428)
        self.horizontalLayout_GeoDetermine = QtGui.QHBoxLayout(GeoDetermine)
        self.horizontalLayout_GeoDetermine.setObjectName(_fromUtf8("horizontalLayout_GeoDetermine"))
        self.tabGeneral = QtGui.QTabWidget(GeoDetermine)
        self.tabGeneral.setObjectName(_fromUtf8("tabGeneral"))
        self.tabGeoDeterminePosition = QtGui.QWidget(GeoDetermine)
        self.tabGeoDeterminePosition.setObjectName(_fromUtf8("tabGeoDeterminePosition"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabGeoDeterminePosition)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.gbStartPosP = QtGui.QGroupBox(self.tabGeoDeterminePosition)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbStartPosP.sizePolicy().hasHeightForWidth())
        self.gbStartPosP.setSizePolicy(sizePolicy)
        self.gbStartPosP.setObjectName(_fromUtf8("gbStartPosP"))
        self.verticalLayout_gbStartPosP = QtGui.QVBoxLayout(self.gbStartPosP)
        self.verticalLayout_gbStartPosP.setObjectName(_fromUtf8("verticalLayout_gbStartPosP"))

        self.verticalLayout.addWidget(self.gbStartPosP)
        self.grbParametersP = QtGui.QGroupBox(self.tabGeoDeterminePosition)
        self.grbParametersP.setObjectName(_fromUtf8("grbParametersP"))
        self.vLayout_grbParametersP = QtGui.QVBoxLayout(self.grbParametersP)
        self.vLayout_grbParametersP.setObjectName(_fromUtf8("vLayout_grbParametersP"))

        self.chbAutoFinishMagVar = CheckBox(self.grbParametersP)
        self.chbAutoFinishMagVar.Caption = "Automatically Calculate Magnetic Variation"
        self.chbAutoFinishMagVar.Checked = True
        self.vLayout_grbParametersP.addWidget(self.chbAutoFinishMagVar)

        self.txtForwardTP = TrackRadialBoxPanel(self.grbParametersP, "Geo")
        self.txtForwardTP.Caption = "Forward True Bearing"
        self.vLayout_grbParametersP.addWidget(self.txtForwardTP)

        self.txtForwardMP = TrackRadialBoxPanel(self.grbParametersP, "Geo")
        self.txtForwardMP.Caption = "Forward Magnetic Bearing"
        self.txtForwardMP.Button = None
        self.vLayout_grbParametersP.addWidget(self.txtForwardMP)

        self.txtDistanceP = DistanceBoxPanel(self.grbParametersP, DistanceUnits.NM)
        self.txtDistanceP.Caption = "Distance Between Positions"
        self.vLayout_grbParametersP.addWidget(self.txtDistanceP)

        self.cmbCalculationTypeP = ComboBoxPanel(self.grbParametersP)
        self.cmbCalculationTypeP.Caption = "Calculation Type"
        self.cmbCalculationTypeP.Items = ["GreatCircle", "Ellipsoid"]
        self.cmbCalculationTypeP.SelectedIndex = 1
        self.vLayout_grbParametersP.addWidget(self.cmbCalculationTypeP)


        self.frameP = QtGui.QFrame(self.grbParametersP)
        self.frameP.setMinimumSize(QtCore.QSize(0, 0))
        self.frameP.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameP.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameP.setFrameShadow(QtGui.QFrame.Raised)
        self.frameP.setObjectName(_fromUtf8("frameP"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frameP)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.chbMarkPointsP = QtGui.QCheckBox(self.frameP)
        self.chbMarkPointsP.setMinimumSize(QtCore.QSize(200, 0))
        self.chbMarkPointsP.setMaximumSize(QtCore.QSize(200, 16777215))
        self.chbMarkPointsP.setObjectName(_fromUtf8("chbMarkPointsP"))
        self.horizontalLayout_2.addWidget(self.chbMarkPointsP)
        self.chbDrawLineP = QtGui.QCheckBox(self.frameP)
        self.chbDrawLineP.setObjectName(_fromUtf8("chbDrawLineP"))
        self.horizontalLayout_2.addWidget(self.chbDrawLineP)
        self.vLayout_grbParametersP.addWidget(self.frameP)



        self.gbResultP = QtGui.QGroupBox(self.grbParametersP)
        self.gbResultP.setObjectName(_fromUtf8("gbResultP"))
        self.horizontalLayout_gbResultP = QtGui.QHBoxLayout(self.gbResultP)
        self.horizontalLayout_gbResultP.setObjectName(_fromUtf8("horizontalLayout_gbResultP"))
        self.tblResultP = QtGui.QTableView(self.gbResultP)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblResultP.sizePolicy().hasHeightForWidth())
        self.tblResultP.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.tblResultP.setFont(font)
        self.tblResultP.setObjectName(_fromUtf8("tblResultP"))
        self.horizontalLayout_gbResultP.addWidget(self.tblResultP)
        self.btnResultP = QtGui.QPushButton(self.gbResultP)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnResultP.sizePolicy().hasHeightForWidth())
        self.btnResultP.setSizePolicy(sizePolicy)
        self.btnResultP.setMinimumSize(QtCore.QSize(23, 0))
        self.btnResultP.setMaximumSize(QtCore.QSize(23, 16777215))
        self.btnResultP.setText(_fromUtf8(""))
        self.btnResultP.setObjectName(_fromUtf8("btnResultP"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnResultP.setIcon(icon)
        self.horizontalLayout_gbResultP.addWidget(self.btnResultP)
        self.vLayout_grbParametersP.addWidget(self.gbResultP)


        self.verticalLayout.addWidget(self.grbParametersP)
        self.tabGeneral.addTab(self.tabGeoDeterminePosition, _fromUtf8(""))
        self.tabGeoDetermineBD = QtGui.QWidget(GeoDetermine)
        self.tabGeoDetermineBD.setObjectName(_fromUtf8("tabGeoDetermineBD"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabGeoDetermineBD)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gbStartPosBD = QtGui.QGroupBox(self.tabGeoDetermineBD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbStartPosBD.sizePolicy().hasHeightForWidth())
        self.gbStartPosBD.setSizePolicy(sizePolicy)
        self.gbStartPosBD.setObjectName(_fromUtf8("gbStartPosBD"))
        self.verticalLayout_gbStartPosBD = QtGui.QVBoxLayout(self.gbStartPosBD)
        self.verticalLayout_gbStartPosBD.setObjectName(_fromUtf8("verticalLayout_gbStartPosBD"))

        self.verticalLayout_2.addWidget(self.gbStartPosBD)
        self.gbFinishPosBD = QtGui.QGroupBox(self.tabGeoDetermineBD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbFinishPosBD.sizePolicy().hasHeightForWidth())
        self.gbFinishPosBD.setSizePolicy(sizePolicy)
        self.gbFinishPosBD.setObjectName(_fromUtf8("gbFinishPosBD"))
        self.verticalLayout_gbFinishPosBD = QtGui.QVBoxLayout(self.gbFinishPosBD)
        self.verticalLayout_gbFinishPosBD.setObjectName(_fromUtf8("verticalLayout_gbFinishPosBD"))

        self.verticalLayout_2.addWidget(self.gbFinishPosBD)
        self.grbParametersBD = QtGui.QGroupBox(self.tabGeoDetermineBD)
        self.grbParametersBD.setObjectName(_fromUtf8("grbParametersBD"))
        self.vLayout_grbParametersBD = QtGui.QVBoxLayout(self.grbParametersBD)
        self.vLayout_grbParametersBD.setObjectName(_fromUtf8("vLayout_grbParametersBD"))

        self.cmbCalculationTypeBD = ComboBoxPanel(self.grbParametersBD)
        self.cmbCalculationTypeBD.Caption = "Calculation Type"
        self.cmbCalculationTypeBD.Items = ["GreatCircle", "Ellipsoid"]
        self.cmbCalculationTypeBD.SelectedIndex = 1
        self.vLayout_grbParametersBD.addWidget(self.cmbCalculationTypeBD)

        self.chbAutoVarBD = QtGui.QCheckBox(self.grbParametersBD)
        self.chbAutoVarBD.setObjectName(_fromUtf8("chbAutoVarBD"))
        self.vLayout_grbParametersBD.addWidget(self.chbAutoVarBD)
        self.frameBD = QtGui.QFrame(self.grbParametersBD)
        self.frameBD.setMinimumSize(QtCore.QSize(0, 0))
        self.frameBD.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameBD.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameBD.setFrameShadow(QtGui.QFrame.Raised)
        self.frameBD.setObjectName(_fromUtf8("frameBD"))
        self.horizontalLayout_BD = QtGui.QHBoxLayout(self.frameBD)
        self.horizontalLayout_BD.setSpacing(0)
        self.horizontalLayout_BD.setMargin(0)
        self.horizontalLayout_BD.setObjectName(_fromUtf8("horizontalLayout_BD"))

        self.chbMarkPointsBD = QtGui.QCheckBox(self.frameBD)
        self.chbMarkPointsBD.setMinimumSize(QtCore.QSize(200, 0))
        self.chbMarkPointsBD.setMaximumSize(QtCore.QSize(200, 16777215))
        self.chbMarkPointsBD.setObjectName(_fromUtf8("chbMarkPointsBD"))
        self.horizontalLayout_BD.addWidget(self.chbMarkPointsBD)

        self.chbDrawLineBD = QtGui.QCheckBox(self.frameBD)
        self.chbDrawLineBD.setObjectName(_fromUtf8("chbDrawLineBD"))
        self.horizontalLayout_BD.addWidget(self.chbDrawLineBD)

        self.vLayout_grbParametersBD.addWidget(self.frameBD)
        self.gbResultBD = QtGui.QGroupBox(self.grbParametersBD)
        self.gbResultBD.setObjectName(_fromUtf8("gbResultBD"))
        self.horizontalLayout_gbResultBD = QtGui.QHBoxLayout(self.gbResultBD)
        self.horizontalLayout_gbResultBD.setObjectName(_fromUtf8("horizontalLayout_gbResultBD"))
        self.tblResultBD = QtGui.QTableView(self.gbResultBD)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        self.tblResultBD.setFont(font)
        self.tblResultBD.setObjectName(_fromUtf8("tblResultBD"))
        self.horizontalLayout_gbResultBD.addWidget(self.tblResultBD)
        self.btnResultBD = QtGui.QPushButton(self.gbResultBD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnResultBD.sizePolicy().hasHeightForWidth())
        self.btnResultBD.setSizePolicy(sizePolicy)
        self.btnResultBD.setMinimumSize(QtCore.QSize(23, 0))
        self.btnResultBD.setMaximumSize(QtCore.QSize(23, 16777215))
        self.btnResultBD.setText(_fromUtf8(""))
        self.btnResultBD.setObjectName(_fromUtf8("btnResultBD"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnResultBD.setIcon(icon)
        self.horizontalLayout_gbResultBD.addWidget(self.btnResultBD)
        self.vLayout_grbParametersBD.addWidget(self.gbResultBD)
        self.verticalLayout_2.addWidget(self.grbParametersBD)
        self.tabGeneral.addTab(self.tabGeoDetermineBD, _fromUtf8(""))

        self.tabGeoDetermineMV = QtGui.QWidget(GeoDetermine)
        self.tabGeoDetermineMV.setObjectName(_fromUtf8("tabGeoDetermineMV"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabGeoDetermineMV.sizePolicy().hasHeightForWidth())
        self.tabGeoDetermineMV.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabGeoDetermineMV)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.grbParametersMVD = QtGui.QGroupBox(self.tabGeoDetermineMV)
        self.grbParametersMVD.setObjectName(_fromUtf8("grbParametersMVD"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grbParametersMVD.sizePolicy().hasHeightForWidth())
        self.grbParametersMVD.setSizePolicy(sizePolicy)
        self.vLayout_grbParametersMVD = QtGui.QVBoxLayout(self.grbParametersMVD)
        self.vLayout_grbParametersMVD.setObjectName(_fromUtf8("vLayout_grbParametersMVD"))

        self.frame_dtpDate = QtGui.QFrame(self.grbParametersMVD)
        self.frame_dtpDate.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_dtpDate.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_dtpDate.setObjectName(_fromUtf8("frame_dtpDate"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_dtpDate.sizePolicy().hasHeightForWidth())
        self.frame_dtpDate.setSizePolicy(sizePolicy)
        self.horizontalLayout_dtpDate = QtGui.QHBoxLayout(self.frame_dtpDate)
        self.horizontalLayout_dtpDate.setSpacing(0)
        self.horizontalLayout_dtpDate.setMargin(0)
        self.horizontalLayout_dtpDate.setObjectName(_fromUtf8("horizontalLayout_dtpDate"))
        self.label_80 = QtGui.QLabel(self.frame_dtpDate)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_80.sizePolicy().hasHeightForWidth())
        self.label_80.setSizePolicy(sizePolicy)
        self.label_80.setMinimumSize(QtCore.QSize(200, 0))
        self.label_80.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_80.setFont(font)
        self.label_80.setObjectName(_fromUtf8("label_80"))
        self.horizontalLayout_dtpDate.addWidget(self.label_80)

        self.frame_ForwardTInP_2 = QtGui.QFrame(self.frame_dtpDate)
        self.frame_ForwardTInP_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_ForwardTInP_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_ForwardTInP_2.setObjectName(_fromUtf8("frame_ForwardTInP_2"))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_ForwardTInP_2.sizePolicy().hasHeightForWidth())
        self.frame_ForwardTInP_2.setSizePolicy(sizePolicy)
        self.horizontalLayout_ForwardTInP_2 = QtGui.QHBoxLayout(self.frame_ForwardTInP_2)
        self.horizontalLayout_ForwardTInP_2.setSpacing(0)
        self.horizontalLayout_ForwardTInP_2.setMargin(0)
        self.horizontalLayout_ForwardTInP_2.setObjectName(_fromUtf8("horizontalLayout_ForwardTInP_2"))
        self.dtpDate = QtGui.QDateEdit(self.frame_ForwardTInP_2)
        self.dtpDate.setObjectName(_fromUtf8("dtpDate"))
        self.dtpDate.setMaximumWidth(80)
        self.dtpDate.setMinimumWidth(80)
        self.horizontalLayout_ForwardTInP_2.addWidget(self.dtpDate)
        self.btnDtpDate = QtGui.QToolButton(self.frame_ForwardTInP_2)
        self.btnDtpDate.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/calender.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDtpDate.setIcon(icon)
        self.btnDtpDate.setObjectName(_fromUtf8("btnDtpDate"))
        self.horizontalLayout_ForwardTInP_2.addWidget(self.btnDtpDate)
        self.horizontalLayout_dtpDate.addWidget(self.frame_ForwardTInP_2)
        self.vLayout_grbParametersMVD.addWidget(self.frame_dtpDate)

        self.cmbModel = ComboBoxPanel(self.grbParametersMVD)
        self.cmbModel.Caption = "Model"
        self.cmbModel.Items = ["WMM2015", "WMM2010" , "WMM2005", "WMM2000", "WMM95", "WMM90", "WMM85", "IGRF2000", "IGRF95", "IGRF90"]
        # self.cmbModel.SelectedIndex = 1
        self.vLayout_grbParametersMVD.addWidget(self.cmbModel)


        self.gbResultMVD = QtGui.QGroupBox(self.grbParametersMVD)
        self.gbResultMVD.setObjectName(_fromUtf8("gbResultMVD"))
        self.horizontalLayout_gbResultMVD = QtGui.QHBoxLayout(self.gbResultMVD)
        self.horizontalLayout_gbResultMVD.setObjectName(_fromUtf8("horizontalLayout_gbResultMVD"))


        self.txtResult = TextBoxPanel(self.gbResultMVD)
        self.txtResult.Caption = "Magnetic Variation"
        self.horizontalLayout_gbResultMVD.addWidget(self.txtResult)

        self.vLayout_grbParametersMVD.addWidget(self.gbResultMVD)
        self.verticalLayout_3.addWidget(self.grbParametersMVD)

        spacerItem = QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)

        self.tabGeneral.addTab(self.tabGeoDetermineMV, _fromUtf8(""))
        self.horizontalLayout_GeoDetermine.addWidget(self.tabGeneral)

        self.retranslateUi(GeoDetermine)
        self.tabGeneral.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(GeoDetermine)

    def retranslateUi(self, GeoDetermine):
        GeoDetermine.setWindowTitle(_translate("GeoDetermine", "GeoDetermine", None))
        self.gbStartPosP.setTitle(_translate("GeoDetermine", "Starting Position", None))
        self.grbParametersP.setTitle(_translate("GeoDetermine", "Parameters", None))
        # self.label_74.setText(_translate("GeoDetermine", "Forward True Bearing(°):", None))
        # self.txtForwardTP.setText(_translate("GeoDetermine", "90", None))
        # self.label_3.setText(_translate("GeoDetermine", "Forward Magnetic Bearing (°):", None))
        # self.txtForwardMP.setText(_translate("GeoDetermine", "0", None))
        # self.label_75.setText(_translate("GeoDetermine", "Distance Between Positions(nm):", None))
        # self.txtDistanceP.setText(_translate("GeoDetermine", "2", None))
        # self.label_69.setText(_translate("GeoDetermine", "Calculation Type:", None))
        self.chbMarkPointsP.setText(_translate("GeoDetermine", "Mark Points", None))
        self.chbDrawLineP.setText(_translate("GeoDetermine", "Draw a Line", None))
        self.gbResultP.setTitle(_translate("GeoDetermine", "Result", None))
        self.tabGeneral.setTabText(self.tabGeneral.indexOf(self.tabGeoDeterminePosition), _translate("GeoDetermine", "Position", None))
        self.gbStartPosBD.setTitle(_translate("GeoDetermine", "Starting Position", None))
        self.gbFinishPosBD.setTitle(_translate("GeoDetermine", "Finishing Position", None))
        self.grbParametersBD.setTitle(_translate("GeoDetermine", "Parameters", None))
        # self.label_70.setText(_translate("GeoDetermine", "Calculation Type:", None))
        self.chbAutoVarBD.setText(_translate("GeoDetermine", "Automatically Calculate Magnetic Variation", None))
        self.chbMarkPointsBD.setText(_translate("GeoDetermine", "Mark Points", None))
        self.chbDrawLineBD.setText(_translate("GeoDetermine", "Draw a Line", None))
        self.gbResultBD.setTitle(_translate("GeoDetermine", "Result", None))
        self.tabGeneral.setTabText(self.tabGeneral.indexOf(self.tabGeoDetermineBD), _translate("GeoDetermine", "Bearing and Distance", None))
        self.grbParametersMVD.setTitle(_translate("GeoDetermine", "Parameters", None))
        self.label_80.setText(_translate("GeoDetermine", "Date:", None))
        # self.label_71.setText(_translate("GeoDetermine", "Model:", None))
        self.gbResultMVD.setTitle(_translate("GeoDetermine", "Result", None))
        # self.label_78.setText(_translate("GeoDetermine", "Magnetic Variation:", None))
        self.tabGeneral.setTabText(self.tabGeneral.indexOf(self.tabGeoDetermineMV), _translate("GeoDetermine", "Theoretical Magnetic Variation", None))

