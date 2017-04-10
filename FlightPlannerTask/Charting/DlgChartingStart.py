# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chartingBase.ui'
#
# Created: Tue Sep 13 14:44:21 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FlightPlanner.Panels.GroupBox import GroupBox
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel, AngleGradientSlope, AngleGradientSlopeUnits
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, DistanceUnits, Distance
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.AltitudeBoxPanel import Altitude, AltitudeBoxPanel
from FlightPlanner.types import AltitudeUnits
from Charting.DlgCharting import DlgCharting

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

class DlgChartingStart(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName(_fromUtf8("Dialog"))
        self.resize(200, 200)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.horizontalLayout_2 = QtGui.QVBoxLayout(self)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame_13 = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_13.setObjectName(_fromUtf8("frame_13"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.frame_13)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.frame_3 = QtGui.QFrame(self.frame_13)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))

        spacerItem111 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem111)

        self.gbGradientDist = GroupBox(self.frame_3)
        self.gbGradientDist.Caption = ""
        self.verticalLayout_9.addWidget(self.gbGradientDist)

        self.pnlDescentGradient = AngleGradientBoxPanel(self.gbGradientDist)
        self.pnlDescentGradient.CaptionUnits = AngleGradientSlopeUnits.Percent
        self.pnlDescentGradient.Caption = "Descent gradient"
        self.pnlDescentGradient.Value = AngleGradientSlope(5.0, AngleGradientSlopeUnits.Percent)
        self.pnlDescentGradient.showPercentBox()
        self.gbGradientDist.Add = self.pnlDescentGradient

        self.pnlDX = DistanceBoxPanel(self.gbGradientDist, DistanceUnits.M)
        self.pnlDX.Caption = "dX(THR-DME)"
        self.gbGradientDist.Add = self.pnlDX

        self.pnlThrAlt = AltitudeBoxPanel(self.gbGradientDist)
        self.pnlThrAlt.Caption = "THR Altitude"
        self.pnlThrAlt.Value = Altitude(734.0, AltitudeUnits.FT)
        self.gbGradientDist.Add = self.pnlThrAlt
        
        self.pnlRDHAlt = AltitudeBoxPanel(self.gbGradientDist)
        self.pnlRDHAlt.Caption = "RDH Altitude"
        self.pnlRDHAlt.Value = Altitude(50.0, AltitudeUnits.FT)
        self.gbGradientDist.Add = self.pnlRDHAlt


        self.pnlDistance = DistanceBoxPanel(self.gbGradientDist, DistanceUnits.NM)
        self.pnlDistance.Caption = "Distance between FAF-MAPt"
        self.pnlDistance.Value = Distance(6, DistanceUnits.NM)
        self.gbGradientDist.Add = self.pnlDistance

        self.gbCatOfACFT = QtGui.QGroupBox(self.frame_3)
        self.gbCatOfACFT.setObjectName("gbCatOfACFT")
        self.verticalLayoutgbCatOfACFT = QtGui.QVBoxLayout(self.gbCatOfACFT)
        self.verticalLayoutgbCatOfACFT.setObjectName("verticalLayoutgbCatOfACFT")
        self.cmbCatOfACFT = QtGui.QComboBox(self.gbCatOfACFT)
        self.cmbCatOfACFT.setObjectName("cmbCatOfACFT")
        self.verticalLayoutgbCatOfACFT.addWidget(self.cmbCatOfACFT)
        self.verticalLayout_9.addWidget(self.gbCatOfACFT)
        self.gbCatOfACFT.setTitle("Cat Of ACFT")
        self.cmbCatOfACFT.addItems(["A", "A, B", "A, B, C", "A, B, C, D", "A, B, C, D, DL",
                                   "A, B, C, D, DL, E", "A, B, C, D, E"])

        self.gbTemplate = QtGui.QGroupBox(self.frame_3)
        self.gbTemplate.setObjectName("gbTemplate")
        self.verticalLayoutgbTemplate = QtGui.QVBoxLayout(self.gbTemplate)
        self.verticalLayoutgbTemplate.setObjectName("self.verticalLayoutgbTemplate")
        self.cmbTemplate = QtGui.QComboBox(self.gbTemplate)
        self.cmbTemplate.setObjectName("cmbTemplate")


        self.verticalLayoutgbTemplate.addWidget(self.cmbTemplate)


        self.verticalLayout_9.addWidget(self.gbTemplate)
        self.gbTemplate.setTitle("Template")

        # self.cmbTemplate = ComboBoxPanel(self.gbTemplate)
        # self.cmbTemplate.LabelWidth = 0
        self.cmbTemplate.addItems(["ILS or LOC","LOC", "VOR", "NDB", "TACAN", "RNP BAROVNAV, SBAS, LNAV",
                                  "RNP BAROVNAV, LNAV", "RNP SBAS, LNAV", "RNP LNAV", "RNP AR", "RNAV STAR",
                                  "RNAV SID", "CONV STAR", "CONV SID"])
        # self.verticalLayoutgbTemplate.addWidget(self.cmbTemplate)

        self.gbStraightInApproach = QtGui.QGroupBox(self.frame_3)
        self.gbStraightInApproach.setObjectName("gbStraightInApproach")
        self.verticalLayoutgbStraightInApproach = QtGui.QVBoxLayout(self.gbStraightInApproach)
        self.verticalLayoutgbStraightInApproach.setObjectName("verticalLayoutgbStraightInApproach")
        self.chbCat1 = CheckBox(self.gbStraightInApproach)
        self.chbCat1.Caption = "Cat I"
        self.verticalLayoutgbStraightInApproach.addWidget(self.chbCat1)
        self.chbCat2 = CheckBox(self.gbStraightInApproach)
        self.chbCat2.Caption = "Cat II"
        self.verticalLayoutgbStraightInApproach.addWidget(self.chbCat2)
        self.chbLOC = CheckBox(self.gbStraightInApproach)
        self.chbLOC.Caption = "LOC"
        self.verticalLayoutgbStraightInApproach.addWidget(self.chbLOC)
        self.verticalLayout_9.addWidget(self.gbStraightInApproach)
        self.gbStraightInApproach.setTitle("Straight-In Approach")

        self.frmState = QtGui.QFrame(self.frame_3)

        self.frmState.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmState.setFrameShadow(QtGui.QFrame.Raised)
        self.frmState.setObjectName(_fromUtf8("frmState"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frmState)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblState = QtGui.QLabel(self.frmState)
        self.lblState.setMinimumSize(QtCore.QSize(90, 0))
        self.lblState.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblState.setObjectName(_fromUtf8("lblState"))
        self.horizontalLayout_3.addWidget(self.lblState)
        self.ddlState = QtGui.QComboBox(self.frmState)
        self.ddlState.setObjectName(_fromUtf8("ddlState"))
        self.horizontalLayout_3.addWidget(self.ddlState)
        self.verticalLayout_9.addWidget(self.frmState)
        self.frmAerodrome = QtGui.QFrame(self.frame_3)
        self.frmAerodrome.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmAerodrome.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAerodrome.setObjectName(_fromUtf8("frmAerodrome"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frmAerodrome)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lblAerodrome = QtGui.QLabel(self.frmAerodrome)
        self.lblAerodrome.setMinimumSize(QtCore.QSize(90, 0))
        self.lblAerodrome.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblAerodrome.setObjectName(_fromUtf8("lblAerodrome"))
        self.horizontalLayout_4.addWidget(self.lblAerodrome)
        self.ddlAerodrome = QtGui.QComboBox(self.frmAerodrome)
        self.ddlAerodrome.setObjectName(_fromUtf8("ddlAerodrome"))
        self.horizontalLayout_4.addWidget(self.ddlAerodrome)
        self.verticalLayout_9.addWidget(self.frmAerodrome)
        self.frmRunway = QtGui.QFrame(self.frame_3)
        self.frmRunway.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmRunway.setFrameShadow(QtGui.QFrame.Raised)
        self.frmRunway.setObjectName(_fromUtf8("frmRunway"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frmRunway)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lblRunway = QtGui.QLabel(self.frmRunway)
        self.lblRunway.setMinimumSize(QtCore.QSize(90, 0))
        self.lblRunway.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblRunway.setObjectName(_fromUtf8("lblRunway"))
        self.horizontalLayout_5.addWidget(self.lblRunway)
        self.ddlRunway1 = QtGui.QComboBox(self.frmRunway)
        self.ddlRunway1.setObjectName(_fromUtf8("ddlRunway1"))
        self.horizontalLayout_5.addWidget(self.ddlRunway1)
        self.ddlRunway2 = QtGui.QComboBox(self.frmRunway)
        self.ddlRunway2.setObjectName(_fromUtf8("ddlRunway2"))
        self.horizontalLayout_5.addWidget(self.ddlRunway2)
        self.verticalLayout_9.addWidget(self.frmRunway)
        self.frmSlope = QtGui.QFrame(self.frame_3)
        self.frmSlope.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmSlope.setFrameShadow(QtGui.QFrame.Raised)
        self.frmSlope.setObjectName(_fromUtf8("frmSlope"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.frmSlope)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.lblSlope = QtGui.QLabel(self.frmSlope)
        self.lblSlope.setMinimumSize(QtCore.QSize(90, 0))
        self.lblSlope.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblSlope.setObjectName(_fromUtf8("lblSlope"))
        self.horizontalLayout_7.addWidget(self.lblSlope)
        self.ddlSlope = QtGui.QComboBox(self.frmSlope)
        self.ddlSlope.setObjectName(_fromUtf8("ddlSlope"))
        self.horizontalLayout_7.addWidget(self.ddlSlope)
        self.verticalLayout_9.addWidget(self.frmSlope)
        self.frmPrintScale = QtGui.QFrame(self.frame_3)
        self.frmPrintScale.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmPrintScale.setFrameShadow(QtGui.QFrame.Raised)
        self.frmPrintScale.setObjectName(_fromUtf8("frmPrintScale"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.frmPrintScale)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.lblPrintScale = QtGui.QLabel(self.frmPrintScale)
        self.lblPrintScale.setMinimumSize(QtCore.QSize(90, 0))
        self.lblPrintScale.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblPrintScale.setObjectName(_fromUtf8("lblPrintScale"))
        self.horizontalLayout_8.addWidget(self.lblPrintScale)
        self.txtPrintScale = QtGui.QLineEdit(self.frmPrintScale)
        self.txtPrintScale.setObjectName(_fromUtf8("txtPrintScale"))
        self.horizontalLayout_8.addWidget(self.txtPrintScale)
        self.verticalLayout_9.addWidget(self.frmPrintScale)
        self.frmFontSize = QtGui.QFrame(self.frame_3)
        self.frmFontSize.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmFontSize.setFrameShadow(QtGui.QFrame.Raised)
        self.frmFontSize.setObjectName(_fromUtf8("frmFontSize"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.frmFontSize)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.lblFontSize = QtGui.QLabel(self.frmFontSize)
        self.lblFontSize.setMinimumSize(QtCore.QSize(90, 0))
        self.lblFontSize.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lblFontSize.setObjectName(_fromUtf8("lblFontSize"))
        self.horizontalLayout_9.addWidget(self.lblFontSize)
        self.txtFontSize = QtGui.QLineEdit(self.frmFontSize)
        self.txtFontSize.setObjectName(_fromUtf8("txtFontSize"))
        self.horizontalLayout_9.addWidget(self.txtFontSize)
        self.verticalLayout_9.addWidget(self.frmFontSize)
        self.gbSizes = QtGui.QGroupBox(self.frame_3)
        self.gbSizes.setObjectName(_fromUtf8("gbSizes"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.gbSizes)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.ddlPageSizes = QtGui.QComboBox(self.gbSizes)
        self.ddlPageSizes.setObjectName(_fromUtf8("ddlPageSizes"))
        self.verticalLayout_10.addWidget(self.ddlPageSizes)
        self.frame_11 = QtGui.QFrame(self.gbSizes)
        self.frame_11.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_11.setObjectName(_fromUtf8("frame_11"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout(self.frame_11)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))

        self.labelUnit = QtGui.QLabel(self.frame_11)
        self.labelUnit.setObjectName("labelUint")
        self.labelUnit.setText("Unit")
        self.horizontalLayout_10.addWidget(self.labelUnit)

        self.cmbUnit = QtGui.QComboBox(self.frame_11)
        self.cmbUnit.setObjectName("cmbUnit")
        self.cmbUnit.addItems(["mm", "inch"])
        self.horizontalLayout_10.addWidget(self.cmbUnit)

        self.verticalLayout_10.addWidget(self.frame_11)
        self.frmWidth = QtGui.QFrame(self.gbSizes)
        self.frmWidth.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmWidth.setFrameShadow(QtGui.QFrame.Raised)
        self.frmWidth.setObjectName(_fromUtf8("frmWidth"))
        self.horizontalLayout_12 = QtGui.QHBoxLayout(self.frmWidth)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.lblWidth = QtGui.QLabel(self.frmWidth)
        self.lblWidth.setMinimumSize(QtCore.QSize(81, 0))
        self.lblWidth.setMaximumSize(QtCore.QSize(81, 16777215))
        self.lblWidth.setObjectName(_fromUtf8("lblWidth"))
        self.horizontalLayout_12.addWidget(self.lblWidth)
        self.txtWidth = QtGui.QLineEdit(self.frmWidth)
        self.txtWidth.setObjectName(_fromUtf8("txtWidth"))
        self.horizontalLayout_12.addWidget(self.txtWidth)
        self.verticalLayout_10.addWidget(self.frmWidth)
        self.frmHeight = QtGui.QFrame(self.gbSizes)
        self.frmHeight.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frmHeight.setFrameShadow(QtGui.QFrame.Raised)
        self.frmHeight.setObjectName(_fromUtf8("frmHeight"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout(self.frmHeight)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.lblHeight = QtGui.QLabel(self.frmHeight)
        self.lblHeight.setMinimumSize(QtCore.QSize(81, 0))
        self.lblHeight.setMaximumSize(QtCore.QSize(81, 16777215))
        self.lblHeight.setObjectName(_fromUtf8("lblHeight"))
        self.horizontalLayout_13.addWidget(self.lblHeight)
        self.txtHeight = QtGui.QLineEdit(self.frmHeight)
        self.txtHeight.setObjectName(_fromUtf8("txtHeight"))
        self.horizontalLayout_13.addWidget(self.txtHeight)
        self.verticalLayout_10.addWidget(self.frmHeight)
        self.verticalLayout_9.addWidget(self.gbSizes)
        self.gbPageOrientation = QtGui.QGroupBox(self.frame_3)
        self.gbPageOrientation.setObjectName(_fromUtf8("gbPageOrientation"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout(self.gbPageOrientation)
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))

        # self.labelPageOrientation = QtGui.QLabel(self.gbPageOrientation)
        # self.labelPageOrientation.setObjectName("labelPageOrientation")
        # self.labelPageOrientation.setText("Page Orientation")
        # self.horizontalLayout_14.addWidget(self.labelPageOrientation)

        self.cmbPageOrientation = QtGui.QComboBox(self.gbPageOrientation)
        self.cmbPageOrientation.setObjectName("cmbPageOrientation")
        self.cmbPageOrientation.addItems(["Portrait", "Landscape"])
        self.horizontalLayout_14.addWidget(self.cmbPageOrientation)

        # self.rbtLandscape = QtGui.QRadioButton(self.gbPageOrientation)
        # self.rbtLandscape.setObjectName(_fromUtf8("radioButton"))
        # self.horizontalLayout_14.addWidget(self.rbtLandscape)
        # self.rbtPortrait = QtGui.QRadioButton(self.gbPageOrientation)
        # self.rbtPortrait.setChecked(True)
        # self.rbtPortrait.setObjectName(_fromUtf8("rblLandscape"))
        # self.horizontalLayout_14.addWidget(self.rbtPortrait)
        self.verticalLayout_9.addWidget(self.gbPageOrientation)
        self.horizontalLayout_6.addWidget(self.frame_3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.horizontalLayout_2.addWidget(self.frame_13)

        self.frame = QtGui.QFrame(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem15 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem15)
        self.btnPrevious = QtGui.QPushButton(self.frame)
        self.btnPrevious.setObjectName(_fromUtf8("btnPrevious"))
        self.horizontalLayout.addWidget(self.btnPrevious)
        self.btnNext = QtGui.QPushButton(self.frame)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnExit = QtGui.QPushButton(self.frame)
        self.btnExit.setObjectName(_fromUtf8("btnExit"))
        self.horizontalLayout.addWidget(self.btnExit)
        spacerItem16 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem16)
        self.horizontalLayout_2.addWidget(self.frame)

        self.frmState.setVisible(False)
        self.frmAerodrome.setVisible(False)
        self.frmRunway.setVisible(False)
        self.frmSlope.setVisible(False)
        self.ddlPageSizes.setVisible(False)

        self.txtPrintScale.setText("10")
        self.txtFontSize.setText("10")
        self.txtWidth.setText("210")
        self.txtHeight.setText("290")


        # self.rbtnmm.setChecked(True)
        self.retranslateUi()
        # self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.btnPrevious.setEnabled(False)
        self.btnNext.clicked.connect(self.btnNext_clicked)
        self.btnExit.setVisible(False)

        self.gbStraightInApproach.setVisible(self.cmbCatOfACFT.currentIndex() == 0)

        self.cmbUnit.currentIndexChanged.connect(self.paperResize)
        self.txtHeight.textChanged.connect(self.pageOrientationChange)
        self.txtWidth.textChanged.connect(self.pageOrientationChange)

        self.cmbTemplate.currentIndexChanged.connect(self.cmbCatOfACFT_currentIndexChanged)
        self.cmbTemplate.activated.connect(self.cmbCatOfACFT_activated)
        self.cmbCatOfACFT.currentIndexChanged.connect(self.cmbCatOfACFT_currentIndexChanged)

        self.connect(self.chbCat1, QtCore.SIGNAL("Event_0"), self.chbCat1_clicked)
        self.connect(self.chbCat2, QtCore.SIGNAL("Event_0"), self.chbCat2_clicked)
        self.connect(self.chbLOC, QtCore.SIGNAL("Event_0"), self.chbLOC_clicked)

        # self.cmbPageOrientation.currentIndexChanged.connect(self.widthHeighChange)
        self.dlg = None
        self.straightCount = 3
        self.catOfAcftCount = 1
    def cmbCatOfACFT_currentIndexChanged(self):
        if self.cmbCatOfACFT.currentIndex() == 6:
            self.catOfAcftCount = 5
        else:
            self.catOfAcftCount = self.cmbCatOfACFT.currentIndex() + 1
    def chbCat1_clicked(self):
        if self.chbCat1.Checked:
            self.straightCount += 1
        else:
            self.straightCount -= 1
    def chbCat2_clicked(self):
        if self.chbCat2.Checked:
            self.straightCount += 1
        else:
            self.straightCount -= 1
    def chbLOC_clicked(self):
        if self.chbLOC.Checked:
            self.straightCount += 1
        else:
            self.straightCount -= 1
    def cmbCatOfACFT_activated(self, index):
        self.gbStraightInApproach.setVisible(index == 0)
    def widthHeighChange(self):

        w = float(self.txtWidth.text())
        h = float(self.txtHeight.text())

        self.txtWidth.setText(str(round(h, 2)))
        self.txtHeight.setText(str(round(w, 2)))

    def pageOrientationChange(self):
        w = float(self.txtWidth.text())
        h = float(self.txtHeight.text())
        if w < h:
            self.cmbPageOrientation.setCurrentIndex(0)
        else:
            self.cmbPageOrientation.setCurrentIndex(1)

    def paperResize(self):
        w = float(self.txtWidth.text())
        h = float(self.txtHeight.text())

        if self.cmbUnit.currentIndex() != 0:
            w /= 25.4
            h /= 25.4
        else:
            w *= 25.4
            h *= 25.4
        self.txtWidth.setText(str(round(w, 2)))
        self.txtHeight.setText(str(round(h, 2)))

    def btnNext_clicked(self):
        # self.btnPrevious.setEnabled(True)
        w = float(self.txtWidth.text())
        h = float(self.txtHeight.text())

        if self.cmbUnit.currentIndex() != 0:
            w *= 25.4
            h *= 25.4
        data = {"PrintScale": int(self.txtPrintScale.text()),
                "FontSize": int(self.txtFontSize.text()),
                "Sizes": "mm" if self.cmbUnit.currentIndex() == 0 else "inch",
                "Width": int(w),
                "Height": int(h),
                "PageOrientation": "L" if self.cmbPageOrientation.currentIndex() == 1 else "P",
                "StraightCount": self.straightCount,
                "Template": [self.cmbTemplate.currentIndex(), self.cmbTemplate.currentText()],
                "CatOfAcftCount": [self.catOfAcftCount, self.cmbCatOfACFT.currentIndex()],
                "Distance": self.pnlDistance.Value.NauticalMiles,
                "DescentGradient": self.pnlDescentGradient.Value.Degrees,
                "ThrAltitude": self.pnlThrAlt.Value.Feet,
                "RDHAltitude": self.pnlRDHAlt.Value.Feet,
                "dX": self.pnlDX.Value.Metres}
        if self.dlg == None:
            self.dlg = DlgCharting(self, data )
        if data["Template"][1].contains("RNP"):
            self.dlg.ui.txtText7.setText("RNP RWY 19")
        elif data["Template"][1].contains("RNAV"):
            self.dlg.ui.txtText7.setText("RNAV RWY 19")
        elif data["Template"][1].contains("CONV"):
            self.dlg.ui.txtText7.setText("CONV RWY 19")
        else:
            self.dlg.ui.txtText7.setText(data["Template"][1] + " RWY 19")
        if data["Template"][1].contains("RNP AR"):
            self.dlg.ui.txtText7.setText("RNP AR RWY 19")
        self.dlg.show()
        self.hide()
        self.dlg.refreshData(data)
    def retranslateUi(self):
        self.setWindowTitle(_translate("Dialog", "Charting Tool 1", None))
        self.lblState.setText(_translate("Dialog", "State: ", None))
        self.lblAerodrome.setText(_translate("Dialog", "Aerodrome: ", None))
        self.lblRunway.setText(_translate("Dialog", "Runway: ", None))
        self.lblSlope.setText(_translate("Dialog", "Slope: ", None))
        self.lblPrintScale.setText(_translate("Dialog", "Print Scale: ", None))
        self.lblFontSize.setText(_translate("Dialog", "Font Size(Point): ", None))
        self.gbSizes.setTitle(_translate("Dialog", "Sizes", None))
        # self.rbtnInch.setText(_translate("Dialog", "Inch", None))
        # self.rbtnmm.setText(_translate("Dialog", "MM", None))
        self.lblWidth.setText(_translate("Dialog", "Width:", None))
        self.lblHeight.setText(_translate("Dialog", "Height: ", None))
        self.gbPageOrientation.setTitle(_translate("Dialog", "Page Orientation", None))
        # self.rbtLandscape.setText(_translate("Dialog", "Landscape", None))
        # self.rbtPortrait.setText(_translate("Dialog", "Portrait", None))
        self.btnPrevious.setText(_translate("Dialog", "Previous", None))
        self.btnNext.setText(_translate("Dialog", "Next", None))
        self.btnExit.setText(_translate("Dialog", "Finish", None))

