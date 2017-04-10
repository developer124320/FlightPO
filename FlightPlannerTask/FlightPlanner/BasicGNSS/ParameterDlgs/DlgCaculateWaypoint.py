# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QFrame, QVBoxLayout, QGroupBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog, QDialogButtonBox, QMessageBox
from PyQt4.QtCore import QSize, QSizeF, Qt, SIGNAL, QObject

from FlightPlanner.captureCoordinateTool import CaptureCoordinateTool
import define
from qgis.gui import QgsMapToolPan
from qgis.core import QgsPoint
from FlightPlanner.types import RnavCommonWaypoint, DistanceUnits, AngleUnits, AircraftSpeedCategory
from FlightPlanner.QgisHelper import Point3D
from FlightPlanner.helpers import Unit, MathHelper, Distance
from FlightPlanner.BasicGNSS.rnavWaypoints import RnavWaypoints
from FlightPlanner.messages import Messages
from FlightPlanner.MeasureTool import MeasureTool
from FlightPlanner.CaptureBearingTool import CaptureBearingTool
from FlightPlanner.validations import Validations
import math


class CalcDlg(QDialog):
    def __init__(self, parent, rnavType, category, position_0, position_1, position_List, flagStr = None):
        QDialog.__init__(self, parent)
        self.flagStrName = flagStr
#         self.resize(326, 310)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(("verticalLayout"))
        self.groupBox = QGroupBox(self)
        self.groupBox.setTitle((""))
        self.groupBox.setObjectName(("groupBox"))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(("verticalLayout_2"))
        self.groupBox_5 = QGroupBox(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(("Arial"))
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName(("groupBox_5"))
        self.horizontalLayout_19 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setMargin(0)
        self.horizontalLayout_19.setObjectName(("horizontalLayout_19"))
        self.frame_18 = QFrame(self.groupBox_5)
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.frame_18.setObjectName(("frame_18"))
        self.verticalLayout_13 = QVBoxLayout(self.frame_18)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_13.setObjectName(("verticalLayout_13"))
        self.frame_19 = QFrame(self.frame_18)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_19.sizePolicy().hasHeightForWidth())
        self.frame_19.setSizePolicy(sizePolicy)
        self.frame_19.setFrameShape(QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Raised)
        self.frame_19.setObjectName(("frame_19"))
        self.horizontalLayout_20 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setMargin(0)
        self.horizontalLayout_20.setObjectName(("horizontalLayout_20"))
        self.label_9 = QLabel(self.frame_19)
        self.label_9.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName(("label_9"))
        self.horizontalLayout_20.addWidget(self.label_9)
        self.txtTHR_X = QLineEdit(self.frame_19)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtTHR_X.sizePolicy().hasHeightForWidth())
        self.txtTHR_X.setSizePolicy(sizePolicy)
        self.txtTHR_X.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtTHR_X.setFont(font)
        self.txtTHR_X.setObjectName(("txtTHR_X"))
        self.horizontalLayout_20.addWidget(self.txtTHR_X)
        self.verticalLayout_13.addWidget(self.frame_19)
        self.frame_20 = QFrame(self.frame_18)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy)
        self.frame_20.setFrameShape(QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Raised)
        self.frame_20.setObjectName(("frame_20"))
        self.horizontalLayout_21 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setMargin(0)
        self.horizontalLayout_21.setObjectName(("horizontalLayout_21"))
        self.label_10 = QLabel(self.frame_20)
        self.label_10.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName(("label_10"))
        self.horizontalLayout_21.addWidget(self.label_10)
        self.txtTHR_Y = QLineEdit(self.frame_20)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtTHR_Y.sizePolicy().hasHeightForWidth())
        self.txtTHR_Y.setSizePolicy(sizePolicy)
        self.txtTHR_Y.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtTHR_Y.setFont(font)
        self.txtTHR_Y.setObjectName(("txtTHR_Y"))
        self.horizontalLayout_21.addWidget(self.txtTHR_Y)
        self.verticalLayout_13.addWidget(self.frame_20)
        self.horizontalLayout_19.addWidget(self.frame_18)
        self.frame_21 = QFrame(self.groupBox_5)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_21.sizePolicy().hasHeightForWidth())
        self.frame_21.setSizePolicy(sizePolicy)
        self.frame_21.setMaximumSize(QSize(30, 70))
        self.frame_21.setFrameShape(QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Raised)
        self.frame_21.setObjectName(("frame_21"))
        self.verticalLayout_14 = QVBoxLayout(self.frame_21)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setMargin(0)
        self.verticalLayout_14.setObjectName(("verticalLayout_14"))
        self.btnCaptureRunwayTHR = QToolButton(self.frame_21)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCaptureRunwayTHR.sizePolicy().hasHeightForWidth())
        self.btnCaptureRunwayTHR.setSizePolicy(sizePolicy)
        self.btnCaptureRunwayTHR.setMaximumSize(QSize(16777215, 47))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)
        self.btnCaptureRunwayTHR.setIcon(icon)
        self.btnCaptureRunwayTHR.setObjectName(("btnCaptureRunwayTHR"))
        self.verticalLayout_14.addWidget(self.btnCaptureRunwayTHR)
#         self.btnToolTHR = QToolButton(self.frame_21)
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btnToolTHR.sizePolicy().hasHeightForWidth())
#         self.btnToolTHR.setSizePolicy(sizePolicy)
#         self.btnToolTHR.setMaximumSize(QSize(16777215, 20))
#         icon1 = QIcon()
#         icon1.addPixmap(QPixmap(("Resource/sort2.png")), QIcon.Normal, QIcon.Off)
#         self.btnToolTHR.setIcon(icon1)
#         self.btnToolTHR.setObjectName(("btnToolTHR"))
#         self.verticalLayout_14.addWidget(self.btnToolTHR)
        self.horizontalLayout_19.addWidget(self.frame_21)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.groupBox_4 = QGroupBox(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(("Arial"))
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(("groupBox_4"))
        self.horizontalLayout_16 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setMargin(0)
        self.horizontalLayout_16.setObjectName(("horizontalLayout_16"))
        self.frame_14 = QFrame(self.groupBox_4)
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.frame_14.setObjectName(("frame_14"))
        self.verticalLayout_11 = QVBoxLayout(self.frame_14)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_11.setObjectName(("verticalLayout_11"))
        self.frame_15 = QFrame(self.frame_14)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy)
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.frame_15.setObjectName(("frame_15"))
        self.horizontalLayout_17 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setMargin(0)
        self.horizontalLayout_17.setObjectName(("horizontalLayout_17"))
        self.label_7 = QLabel(self.frame_15)
        self.label_7.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName(("label_7"))
        self.horizontalLayout_17.addWidget(self.label_7)
        self.txtEND_X = QLineEdit(self.frame_15)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtEND_X.sizePolicy().hasHeightForWidth())
        self.txtEND_X.setSizePolicy(sizePolicy)
        self.txtEND_X.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtEND_X.setFont(font)
        self.txtEND_X.setObjectName(("txtEND_X"))
        self.horizontalLayout_17.addWidget(self.txtEND_X)
        self.verticalLayout_11.addWidget(self.frame_15)
        self.frame_16 = QFrame(self.frame_14)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy)
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.frame_16.setObjectName(("frame_16"))
        self.horizontalLayout_18 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setMargin(0)
        self.horizontalLayout_18.setObjectName(("horizontalLayout_18"))
        self.label_8 = QLabel(self.frame_16)
        self.label_8.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName(("label_8"))
        self.horizontalLayout_18.addWidget(self.label_8)
        self.txtEND_Y = QLineEdit(self.frame_16)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtEND_Y.sizePolicy().hasHeightForWidth())
        self.txtEND_Y.setSizePolicy(sizePolicy)
        self.txtEND_Y.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtEND_Y.setFont(font)
        self.txtEND_Y.setObjectName(("txtEND_Y"))
        self.horizontalLayout_18.addWidget(self.txtEND_Y)
        self.verticalLayout_11.addWidget(self.frame_16)
        self.horizontalLayout_16.addWidget(self.frame_14)
        self.frame_17 = QFrame(self.groupBox_4)
        self.frame_17.setMaximumSize(QSize(30, 16777215))
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.frame_17.setObjectName(("frame_17"))
        self.verticalLayout_12 = QVBoxLayout(self.frame_17)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setMargin(0)
        self.verticalLayout_12.setObjectName(("verticalLayout_12"))
        self.btnCaptureRunwayEND = QToolButton(self.frame_17)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCaptureRunwayEND.sizePolicy().hasHeightForWidth())
        self.btnCaptureRunwayEND.setSizePolicy(sizePolicy)
        self.btnCaptureRunwayEND.setMaximumSize(QSize(16777215, 47))
        self.btnCaptureRunwayEND.setIcon(icon)
        self.btnCaptureRunwayEND.setObjectName(("btnCaptureRunwayEND"))
        self.verticalLayout_12.addWidget(self.btnCaptureRunwayEND)
#         self.btnToolEND = QToolButton(self.frame_17)
#         sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.btnToolEND.sizePolicy().hasHeightForWidth())
#         self.btnToolEND.setSizePolicy(sizePolicy)
#         self.btnToolEND.setMaximumSize(QSize(16777215, 20))
#         self.btnToolEND.setIcon(icon1)
#         self.btnToolEND.setObjectName(("btnToolEND"))
#         self.verticalLayout_12.addWidget(self.btnToolEND)
        self.horizontalLayout_16.addWidget(self.frame_17)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.lbl1 = QLabel(self.groupBox)
        font = QFont()
        font.setFamily(("Arial"))
        self.lbl1.setFont(font)
        self.lbl1.setText((""))
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.lbl1.setWordWrap(False)
        self.lbl1.setMargin(0)
        self.lbl1.setObjectName(("lbl1"))
        self.verticalLayout_2.addWidget(self.lbl1)
        self.lbl2 = QLabel(self.groupBox)
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.lbl2.setFont(font)
        self.lbl2.setText((""))
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.lbl2.setObjectName(("lbl2"))
        self.verticalLayout_2.addWidget(self.lbl2)
        self.frame_22 = QFrame(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_22.sizePolicy().hasHeightForWidth())
        self.frame_22.setSizePolicy(sizePolicy)
        self.frame_22.setFrameShape(QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Raised)
        self.frame_22.setObjectName(("frame_22"))
        self.horizontalLayout_22 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setMargin(0)
        self.horizontalLayout_22.setObjectName(("horizontalLayout_22"))
        self.label_11 = QLabel(self.frame_22)
        self.label_11.setMinimumSize(QSize(170, 0))
        self.label_11.setMaximumSize(QSize(180, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName(("label_11"))
        self.horizontalLayout_22.addWidget(self.label_11)
        self.txtForm = QLineEdit(self.frame_22)
        self.txtForm.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtForm.sizePolicy().hasHeightForWidth())
        self.txtForm.setSizePolicy(sizePolicy)
        self.txtForm.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtForm.setFont(font)
        self.txtForm.setObjectName(("txtForm"))
        self.horizontalLayout_22.addWidget(self.txtForm)
        self.verticalLayout_2.addWidget(self.frame_22)
        self.frame_23 = QFrame(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_23.sizePolicy().hasHeightForWidth())
        self.frame_23.setSizePolicy(sizePolicy)
        self.frame_23.setFrameShape(QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Raised)
        self.frame_23.setObjectName(("frame_23"))
        self.horizontalLayout_23 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setMargin(0)
        self.horizontalLayout_23.setObjectName(("horizontalLayout_23"))
        self.label_12 = QLabel(self.frame_23)
        self.label_12.setMinimumSize(QSize(170, 0))
        self.label_12.setMaximumSize(QSize(180, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName(("label_12"))
        self.horizontalLayout_23.addWidget(self.label_12)
        self.txtBearing = QLineEdit(self.frame_23)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtBearing.sizePolicy().hasHeightForWidth())
        self.txtBearing.setSizePolicy(sizePolicy)
        self.txtBearing.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtBearing.setFont(font)
        self.txtBearing.setObjectName(("txtBearing"))
        self.horizontalLayout_23.addWidget(self.txtBearing)
        self.btnCaptureBearing = QToolButton(self.frame_23)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCaptureBearing.sizePolicy().hasHeightForWidth())
        self.btnCaptureBearing.setSizePolicy(sizePolicy)
        self.btnCaptureBearing.setMaximumSize(QSize(16777215, 25))
        self.btnCaptureBearing.setStyleSheet((""))
        self.btnCaptureBearing.setIcon(icon)
        self.btnCaptureBearing.setObjectName(("btnCaptureBearing"))
        self.horizontalLayout_23.addWidget(self.btnCaptureBearing)
        self.verticalLayout_2.addWidget(self.frame_23)
        self.frame_24 = QFrame(self.groupBox)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_24.sizePolicy().hasHeightForWidth())
        self.frame_24.setSizePolicy(sizePolicy)
        self.frame_24.setFrameShape(QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Raised)
        self.frame_24.setObjectName(("frame_24"))
        self.horizontalLayout_24 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setMargin(0)
        self.horizontalLayout_24.setObjectName(("horizontalLayout_24"))
        self.lblDistance = QLabel(self.frame_24)
        self.lblDistance.setMinimumSize(QSize(170, 0))
        self.lblDistance.setMaximumSize(QSize(180, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.lblDistance.setFont(font)
        self.lblDistance.setObjectName(("lblDistance"))
        self.horizontalLayout_24.addWidget(self.lblDistance)
        self.txtDistance = QLineEdit(self.frame_24)
        self.txtDistance.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtDistance.sizePolicy().hasHeightForWidth())
        self.txtDistance.setSizePolicy(sizePolicy)
        self.txtDistance.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(("Arial"))
        self.txtDistance.setFont(font)
        self.txtDistance.setObjectName(("txtDistance"))
        self.horizontalLayout_24.addWidget(self.txtDistance)
        self.btnCaptureDistance = QToolButton(self.frame_24)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCaptureDistance.sizePolicy().hasHeightForWidth())
        self.btnCaptureDistance.setSizePolicy(sizePolicy)
        self.btnCaptureDistance.setMaximumSize(QSize(16777215, 23))
        self.btnCaptureDistance.setStyleSheet((""))
        self.btnCaptureDistance.setIcon(icon)
        self.btnCaptureDistance.setObjectName(("btnCaptureDistance"))
        self.horizontalLayout_24.addWidget(self.btnCaptureDistance)
        self.verticalLayout_2.addWidget(self.frame_24)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.btnCaptureDistance.clicked.connect(self.method_9)
        self.btnCaptureBearing.clicked.connect(self.method_8)
        self.txtEND_X.textChanged.connect(self.method_4)
        self.txtEND_Y.textChanged.connect(self.method_4)
        self.txtTHR_X.textChanged.connect(self.method_4)
        self.txtTHR_Y.textChanged.connect(self.method_4)
        self.type = rnavType
        self.category = category
        self.resultPosionList = position_List
        self.MinBearing2 = 0
        self.MaxBearing2= 0
        self.waypoint = None
        self.distanceMeasureTool = MeasureTool(define._canvas, self.txtDistance, DistanceUnits.NM)
        self.bearingTool = CaptureBearingTool(define._canvas, self.txtBearing)
        self.CaptureTHRCoordTool = CaptureCoordinateTool(define._canvas, self.txtTHR_X, self.txtTHR_Y)
        self.CaptureTHRCoordTool.rubberBandClick.setColor(Qt.green)        
        self.CaptureENDCoordTool = CaptureCoordinateTool(define._canvas, self.txtEND_X, self.txtEND_Y)
        self.CaptureENDCoordTool.rubberBandClick.setColor(Qt.blue)
        if rnavType == RnavCommonWaypoint.FAWP or rnavType == RnavCommonWaypoint.MAWP:
            self.from1 = position_0
            
            self.resize(326, 310)
            if position_List[0] != None:        
                self.setThrPosition(position_List[0].x(),position_List[0].y())
                self.CaptureTHRCoordTool.rubberBandClick.addPoint(QgsPoint(position_List[0].x(),position_List[0].y()))
#                 self.CaptureTHRCoordTool.rubberBandClick.show()
            if position_List[1] != None: 
                self.setEndPosition(position_List[1].x(),position_List[1].y())
                self.CaptureENDCoordTool.rubberBandClick.addPoint(QgsPoint(position_List[1].x(),position_List[1].y()))
#             self.setWaypoint(position_List[2])
        else:
            self.from1 = position_1
            num = RnavWaypoints.smethod_0(position_0, position_1)
            self.MinBearing = RnavWaypoints.smethod_7(rnavType, category, num)
            self.MaxBearing= RnavWaypoints.smethod_8(rnavType, category, num)
            self.MinDistance = RnavWaypoints.smethod_4(rnavType, category)
            if flagStr == "Y-Bar":
                if (rnavType == RnavCommonWaypoint.IAWP1):
                    self.setBearing(self.MaxBearing)
                elif (rnavType != RnavCommonWaypoint.IAWP3):
                    self.setBearing(num)
                else:
                    self.setBearing(self.MinBearing)
            else:
                if (rnavType == RnavCommonWaypoint.IAWP1):
                    self.setBearing(self.MinBearing)
                elif (rnavType != RnavCommonWaypoint.IAWP3):
                    self.setBearing(num)
                else:
                    self.setBearing(self.MaxBearing)
#             if self.txtDistance.isEnabled():
#             self.setDistance(RnavWaypoints.smethod_6(rnavType, category).NauticalMiles)
#             self.setWaypoint(position_List.pop(0))
        self.method_4()
        self.retranslateUi()
        QObject.connect(self.buttonBox, SIGNAL(("accepted()")), self.btnCalculate_Click)
        QObject.connect(self.buttonBox, SIGNAL(("rejected()")), self.reject)
#         QMetaObject.connectSlotsByName(Dialog)
        
#         self.btnToolEND.clicked.connect(self.removeEnd)
#         self.btnToolTHR.clicked.connect(self.removeThr)
        self.btnCaptureRunwayTHR.clicked.connect(self.captureTHR)
        self.btnCaptureRunwayEND.clicked.connect(self.captureEND)
        
    def retranslateUi(self):
        self.setWindowTitle("CaculaterDlg")
        self.groupBox_5.setTitle("Runway THR")
        self.label_9.setText("X:")
        self.label_10.setText("Y:")
        self.btnCaptureRunwayTHR.setText("...")
#         self.btnToolTHR.setText("...")
        self.groupBox_4.setTitle("Runway END")
        self.label_7.setText("X:")
        self.label_8.setText("Y:")
        self.btnCaptureRunwayEND.setText("...")
#         self.btnToolEND.setText("...")
        self.label_11.setText("From:")
        self.txtForm.setText("FAWP")
        self.label_12.setText(unicode("Back Azimuth (°) :", "utf-8"))
#         self.txtBearing.setText("188.25")
        self.btnCaptureBearing.setText("...")
        self.lblDistance.setText("Distance From RWY THR (nm):")
        self.txtDistance.setText("5")
        self.btnCaptureDistance.setText("...")
    def captureTHR(self):
        define._canvas.setMapTool(self.CaptureTHRCoordTool)
    def captureEND(self):
        define._canvas.setMapTool(self.CaptureENDCoordTool)
    def close(self):
        scene = define._canvas.scene()
        scene.removeItem(self.CaptureTHRCoordTool.rubberBandClick)
        scene.removeItem(self.CaptureENDCoordTool.rubberBandClick)
        scene.removeItem(self.bearingTool.rubberBand)
        scene.removeItem(self.distanceMeasureTool.rubberBand)
#         self.CaptureTHRCoordTool.rubberBand.hide()
#         self.CaptureENDCoordTool.rubberBand.hide()
        define._canvas.setMapTool(QgsMapToolPan(define._canvas))
#         self.reject()
    def reject(self):
        self.close()
        QDialog.reject(self)
    def getThrPoint3D(self):        
        if self.txtTHR_X.text() !="" and self.txtTHR_Y.text() !="":
            try:
                x = float(self.txtTHR_X.text())
            except ValueError:
                x = 0
            try:
                y = float(self.txtTHR_Y.text())
            except ValueError:
                y = 0
            return Point3D(x, y, 0)
        else:
            return None
    def getEndPoint3D(self):
        if self.txtEND_X.text() !="" and self.txtEND_Y.text() !="":
            try:
                x = float(self.txtEND_X.text())
            except ValueError:
                x = 0
            try:
                y = float(self.txtEND_Y.text())
            except ValueError:
                y = 0
            return Point3D(x, y, 0)
        else:
            return None
    def setEndPosition(self, x, y):
        self.txtEND_X.setText(str(x))
        self.txtEND_Y.setText(str(y))
    def setThrPosition(self, x, y):
        self.txtTHR_X.setText(str(x))
        self.txtTHR_Y.setText(str(y))
    def getWaypoint(self):
        if (self.type == RnavCommonWaypoint.FAWP):
            nauticalMiles = float(self.txtDistance.text())
            value = float(self.txtBearing.text())
            num1 = math.fabs(self.rethr - value)
            if (num1 > 180):
                num1 = 360 - num1
            num2 = math.sin(Unit.smethod_0(num1)) * 0.7559395
            num3 = Unit.smethod_1(math.asin(num2 / nauticalMiles))
            num4 = math.cos(Unit.smethod_0(num1)) * 0.755939525
            num5 = math.cos(Unit.smethod_0(num3)) * nauticalMiles
            return RnavWaypoints.smethod_3(self.pos1400m, float(self.txtBearing.text()), Distance(math.fabs(num5 - num4), DistanceUnits.NM))
        if (self.type != RnavCommonWaypoint.MAWP):
            return RnavWaypoints.smethod_3(self.from1, float(self.txtBearing.text()), Distance(float(self.txtDistance.text()), DistanceUnits.NM))
        angle = 90
        if (float(self.txtBearing.text()) > self.thrre or float(self.txtBearing.text()) - self.thrre >= 90):
            

            if self.flagStrName == "Y-Bar":
                angle = 70
            num = self.rethr - angle
            if (num < 0):
                num = num + 360
        else:
            num = self.rethr + angle
            if (num > 360):
                num = num - 360
        point3d1 = self.from1
        point3d2 = self.getThrPoint3D()
        point3d = MathHelper.getIntersectionPoint(point3d1, RnavWaypoints.smethod_3(self.from1, float(self.txtBearing.text()), Distance(1000)), point3d2, RnavWaypoints.smethod_3(self.getThrPoint3D(), num, Distance(1000)))
        if point3d == None: 
            raise UserWarning, Messages.ERR_FAILED_TO_CALCULATE_INTERSECTION_POINT        
        return RnavWaypoints.smethod_3(self.getThrPoint3D(), num, Distance(MathHelper.calcDistance(point3d2, point3d)))
        
    def setWaypoint(self, value):
        self.waypoint = value
        if self.from1 != None and self.waypoint != None: 
#             self.setBearing(RnavWaypoints.smethod_0(self.from1, value))
#             if self.txtDistance.isEnabled():
#             print RnavWaypoints.smethod_2(self.from1, value).NauticalMiles
#             print RnavWaypoints.smethod_2(self.from1, value).NauticalMiles
            self.setDistance(RnavWaypoints.smethod_2(self.from1, value).NauticalMiles)
    def setDistance(self, value):
        self.txtDistance.setText("%i"%round(value))
    def setBearing(self, value):
        self.txtBearing.setText(str(value))
    def btnCalculate_Click(self):
        # try:
        if self.type == RnavCommonWaypoint.FAWP or self.type == RnavCommonWaypoint.MAWP:
            if self.getThrPoint3D() == None or self.getEndPoint3D() == None:
                return
        if not MathHelper.smethod_112(float(self.txtBearing.text()), self.MinBearing, self.MaxBearing, AngleUnits.Degrees):
            if self.type != RnavCommonWaypoint.MAWP or MathHelper.smethod_96(self.MinBearing2) or MathHelper.smethod_96(self.MaxBearing2):
                raise UserWarning, Messages.VALUE_NOT_WITHIN_ACCEPTABLE_RANGE
            elif not MathHelper.smethod_106(float(self.txtBearing.text()), self.MinBearing2, self.MaxBearing2):
                raise UserWarning, Messages.VALUE_NOT_WITHIN_ACCEPTABLE_RANGE
        if self.txtDistance.isEnabled() and Distance(float(self.txtDistance.text()),DistanceUnits.NM).Metres < (self.MinDistance.Metres - 100):
            raise UserWarning, Validations.VALUE_CANNOT_BE_SMALLER_THAN%self.MinDistance.NauticalMiles
        wayPoint = self.getWaypoint()
        if self.type == RnavCommonWaypoint.FAWP or self.type == RnavCommonWaypoint.MAWP:
            if self.type == RnavCommonWaypoint.FAWP:
                self.parent().gbFAWP.setPosition( wayPoint.x(), wayPoint.y())
                if len(self.parent().parameterCalcList) > 0:
                    self.parent().parameterCalcList.pop(0)
                self.parent().parameterCalcList.insert(0,(self.txtBearing.text(), self.txtDistance.text()))
                self.parent().annotationFAWP.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
            else:
                self.parent().gbMAWP.setPosition( wayPoint.x(), wayPoint.y())
                if len(self.parent().parameterCalcList) > 1:
                    self.parent().parameterCalcList.pop(1)
                self.parent().parameterCalcList.insert(1,(self.txtBearing.text(), self.txtDistance.text()))
                self.parent().annotationMAWP.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
            self.parent().RwyTHR = self.getThrPoint3D()
            self.parent().RwyEND = self.getEndPoint3D()
        elif self.type == RnavCommonWaypoint.MAHWP:
            self.parent().gbMAHWP.setPosition( wayPoint.x(), wayPoint.y())
            if len(self.parent().parameterCalcList) > 2:
                self.parent().parameterCalcList.pop(2)
            self.parent().parameterCalcList.insert(2,(self.txtBearing.text(), self.txtDistance.text()))
            self.parent().annotationMAHWP.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
        elif self.type == RnavCommonWaypoint.IWP:
            self.parent().gbIWP.setPosition( wayPoint.x(), wayPoint.y())
            if len(self.parent().parameterCalcList) > 3:
                self.parent().parameterCalcList.pop(3)
            self.parent().parameterCalcList.insert(3,(self.txtBearing.text(), self.txtDistance.text()))
            self.parent().annotationIWP.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
        elif self.type == RnavCommonWaypoint.IAWP1:
            self.parent().gbIAWP1.setPosition( wayPoint.x(), wayPoint.y())
            if len(self.parent().parameterCalcList) > 4:
                self.parent().parameterCalcList.pop(4)
            self.parent().parameterCalcList.insert(4,(self.txtBearing.text(), self.txtDistance.text()))
            self.parent().annotationIAWP1.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
        elif self.type == RnavCommonWaypoint.IAWP2:
            self.parent().gbIAWP2.setPosition( wayPoint.x(), wayPoint.y())
            if len(self.parent().parameterCalcList) > 5:
                self.parent().parameterCalcList.pop(5)
            self.parent().parameterCalcList.insert(5,(self.txtBearing.text(), self.txtDistance.text()))
            self.parent().annotationIAWP2.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
        elif self.type == RnavCommonWaypoint.IAWP3:
            self.parent().gbIAWP3.setPosition( wayPoint.x(), wayPoint.y())
            if len(self.parent().parameterCalcList) > 6:
                self.parent().parameterCalcList.pop(6)
            self.parent().parameterCalcList.insert(6,(self.txtBearing.text(), self.txtDistance.text()))
            self.parent().annotationIAWP3.setMapPosition(QgsPoint(wayPoint.x(), wayPoint.y()))
        self.close()
        QDialog.accept(self)
        # except UserWarning as e:
        #     pass
        #     # QMessageBox.warning(self, "warning", e.message)
        
    def method_9(self):
#         self.distanceMeasureTool = MeasureTool(define._canvas, self.txtDistance, DistanceUnits.NM)
        define._canvas.setMapTool(self.distanceMeasureTool)
        
    def method_8(self):
#         self.bearingTool = CaptureBearingTool(define._canvas, self.txtBearing)
        define._canvas.setMapTool(self.bearingTool)
    def method_4(self):
        num = None
        num1 = None
        num2 = None
        num3 = None
        num4 = None
        num5 = None
        num6 = None
        num7 = None
        num8 = None
        num9 = None
        self.lbl1.setText(Validations.PLEASE_ENTER_VALID_RUNWAY_POSITIONS)
        self.lbl2.setText(" ")
        if (self.type == RnavCommonWaypoint.FAWP):
            position = self.getThrPoint3D()
            position1 = self.getEndPoint3D()
            if position is None or position1 is None:
                self.txtBearing.setText("")
#                 self.txtDistance.setText("")
                return
            self.thrre = RnavWaypoints.smethod_0(position, position1)
            self.rethr = RnavWaypoints.smethod_0(position1, position)
            self.pos1400m = RnavWaypoints.smethod_3(position, self.rethr, Distance(1400))
            self.MinDistance = RnavWaypoints.smethod_4(self.type, self.category)
#             if self.txtDistance.isEnabled():
#             self.setDistance(RnavWaypoints.smethod_6(self.type, self.category).NauticalMiles)
            
            self.setBearing(self.rethr)
            self.MinBearing = RnavWaypoints.smethod_7(self.type, self.category, self.rethr)
            self.MaxBearing = RnavWaypoints.smethod_8(self.type, self.category, self.rethr)
#             if self.waypoint is not None:
#                 self.setBearing(round(RnavWaypoints.smethod_0(self.pos1400m, self.waypoint), 2))
# #                 if self.txtDistance.isEnabled():
#                 self.setDistance(RnavWaypoints.smethod_2(position, self.waypoint).NauticalMiles)

        elif (self.type == RnavCommonWaypoint.MAWP):
            position2 = self.getThrPoint3D()
            position3 = self.getEndPoint3D()
            if position2 is None or position3 is None:
                self.txtBearing.setText("")
                return            
            self.thrre = RnavWaypoints.smethod_0(position2, position3)
            self.rethr = RnavWaypoints.smethod_0(position3, position2)           

            self.pos1400m = RnavWaypoints.smethod_3(position2, self.rethr, Distance(1400))
            num10 = RnavWaypoints.smethod_1(self.pos1400m, self.from1)
            num = RnavWaypoints.smethod_1(self.from1, self.pos1400m)
            num11 = 15
            position4 = None
            if (self.category == AircraftSpeedCategory.A or self.category == AircraftSpeedCategory.B or self.category == AircraftSpeedCategory.H):
                num11 = 30
            if (num10 > self.rethr or self.rethr - num10 >= 90):
                num1 = self.thrre + num11
                num2 = num
                if (num2 > 360):
                    num2 = num2 - 360                    
            else:
                num1 = num
                num2 = self.thrre - num11
                if (num2 < 0):
                    num2 = num2 + 360
            if (max(num1, num2) <= 270 or min(num1, num2) >= 90):
                num3 =min(num1, num2)
                num4 = max(num1, num2)
            else:
                num3 = max(num1, num2)
                num4 = min(num1, num2)
            position4 = RnavWaypoints.smethod_3(position2, self.thrre, Distance(466))
            num12 = RnavWaypoints.smethod_0(position4, self.from1)
            num13 = math.fabs(num12 - self.rethr)
            if (num13 > 180):
                num13 = 360 - num13
            if (num13 > 5):
                num5 = 0
                num6 = 0
                num7 = 0
                num8 = 0
            else:
                if (num12 > self.rethr or self.rethr - num12 >= 90):
                    num9 = self.rethr + 90
                    if (num9 > 360):
                        num9 = num9 - 360
                else:
                    num9 = self.rethr - 90
                    if (num9 < 0):
                        num9 = num9 + 360
                position5 = RnavWaypoints.smethod_3(self.pos1400m, num9, Distance(150))
                num5 = RnavWaypoints.smethod_0(self.from1, position5)
                num6 = RnavWaypoints.smethod_0(self.from1, self.pos1400m)
                if (max(num5, num6) <= 270 or min(num5, num6) >= 90):
                    num7 = min(num5, num6)
                    num8 = max(num5, num6)
                else:
                    num7 = max(num5, num6)
                    num8 = min(num5, num6)
            if (MathHelper.smethod_99(num, self.thrre, 1)):
                position6 = RnavWaypoints.smethod_3(self.pos1400m, self.rethr - 90, Distance(150))
                position7 = RnavWaypoints.smethod_3(self.pos1400m, self.rethr + 90, Distance(150))
                num1 = RnavWaypoints.smethod_0(self.from1, position6)
                num2 = RnavWaypoints.smethod_0(self.from1, position7)
                num7 = 0
                num8 = 0
                if (max(num1, num2) <= 270 or min(num1, num2) >= 90):
                    num3 = min(num1, num2)
                    num4 = max(num1, num2)
                else:
                    num3 = max(num1, num2)
                    num4 = min(num1, num2)
            if (MathHelper.smethod_96(num7) or MathHelper.smethod_96(num8)):
                self.MinBearing = MathHelper.smethod_3(num3)
                self.MaxBearing = MathHelper.smethod_3(num4)
                self.MinBearing2 = MathHelper.smethod_3(num7)
                self.MaxBearing2 = MathHelper.smethod_3(num8)
            elif (min(num3, num4) >= min(num7, num8)):
                if (MathHelper.smethod_99(num8, num3, 0.3)):
                    num8 = num4
                    num3 = 0
                    num4 = 0
                self.MinBearing = MathHelper.smethod_3(num7)
                self.MaxBearing = MathHelper.smethod_3(num8)
                self.MinBearing2 = MathHelper.smethod_3(num3)
                self.MaxBearing2 = MathHelper.smethod_3(num4)
            else:
                if (MathHelper.smethod_99(num4, num7, 0.3)):
                    num4 = num8
                    num7 = 0
                    num8 = 0
                self.MinBearing = MathHelper.smethod_3(num3)
                self.MaxBearing = MathHelper.smethod_3(num4)
                self.MinBearing2 = MathHelper.smethod_3(num7)
                self.MaxBearing2 = MathHelper.smethod_3(num8)
            self.MinDistance = RnavWaypoints.smethod_4(self.type, self.category)
#             if self.txtDistance.isEnabled():
#                 self.setDistance(RnavWaypoints.smethod_6(self.type, self.category).NauticalMiles)
            if (self.MinBearing <= self.MaxBearing):
                self.setBearing((self.MinBearing + self.MaxBearing) / 2)
            else:
                self.setBearing(MathHelper.smethod_3(self.MinBearing + (360 - self.MinBearing + self.MaxBearing)))
#             if (self.waypoint is not None):
#                 self.setBearing(RnavWaypoints.smethod_0(self.from1, self.waypoint))
        if (MathHelper.smethod_96(self.MinBearing2) or MathHelper.smethod_96(self.MaxBearing2)):
            self.lbl1.setText(unicode("Acceptable bearings are %.1f° - %.1f°", "utf-8")%(self.MinBearing, self.MaxBearing))
        else:
            self.lbl1.setText(Validations.ACCEPTABLE_BEARINGS_ARE_X_Y_AND_X_Y%( self.MinBearing, self.MaxBearing, self.MinBearing2, self.MaxBearing2))
        if self.MinDistance != None and self.type != RnavCommonWaypoint.MAWP:
            self.lbl2.setText(Validations.ACCEPTABLE_MINIMUM_DISTANCE_IS_X%(self.MinDistance.NauticalMiles))
#     def removeEnd(self):
#         self.txtEND_X.setText("")
#         self.txtEND_Y.setText("")
#     def removeThr(self):
#         self.txtTHR_X.setText("")
#         self.txtTHR_Y.setText("")
#     @staticmethod
#     def smethod_0( parent, rnavCommonWaypoint_0, aircraftSpeedCategory_0, position_0, position_1, position_List):
#         flag = None
#         using (DlgCalculateWaypoint dlgCalculateWaypoint = new DlgCalculateWaypoint())
#         {
#             dlgCalculateWaypoint.Text = string.Format("{0} {1}", Captions.CALCULATE, EnumHelper.smethod_0(rnavCommonWaypoint_0))
#             dlgCalculateWaypoint.Type = rnavCommonWaypoint_0
#             dlgCalculateWaypoint.Category = aircraftSpeedCategory_0
#             dlgCalculateWaypoint.From = position_1
#             double num = RnavWaypoints.smethod_0(position_0, position_1)
#             dlgCalculateWaypoint.MinBearing = RnavWaypoints.smethod_7(rnavCommonWaypoint_0, aircraftSpeedCategory_0, num)
#             dlgCalculateWaypoint.MaxBearing = RnavWaypoints.smethod_8(rnavCommonWaypoint_0, aircraftSpeedCategory_0, num)
#             dlgCalculateWaypoint.MinDistance = RnavWaypoints.smethod_4(rnavCommonWaypoint_0, aircraftSpeedCategory_0)
#             if (rnavCommonWaypoint_0 == RnavCommonWaypoint.IAWP1)
#             {
#                 dlgCalculateWaypoint.Bearing = dlgCalculateWaypoint.MinBearing
#             }
#             else if (rnavCommonWaypoint_0 != RnavCommonWaypoint.IAWP3)
#             {
#                 dlgCalculateWaypoint.Bearing = num
#             }
#             else
#             {
#                 dlgCalculateWaypoint.Bearing = dlgCalculateWaypoint.MaxBearing
#             }
#             dlgCalculateWaypoint.Distance = RnavWaypoints.smethod_6(rnavCommonWaypoint_0, aircraftSpeedCategory_0)
#             dlgCalculateWaypoint.Waypoint = position_2
#             if (dlgCalculateWaypoint.method_2(iwin32Window_0) != System.Windows.Forms.DialogResult.OK)
#             {
#                 flag = false
#             }
#             else
#             {
#                 position_2 = dlgCalculateWaypoint.Waypoint
#                 flag = true
#             }
#         }
#         return flag
#     }
# 
#     public static bool smethod_1(IWin32Window iwin32Window_0, RnavCommonWaypoint rnavCommonWaypoint_0, AircraftSpeedCategory aircraftSpeedCategory_0, Position position_0, ref Position position_1, ref Position position_2, ref Position position_3)
#     {
#         bool flag
#         using (DlgCalculateWaypoint dlgCalculateWaypoint = new DlgCalculateWaypoint())
#         {
#             dlgCalculateWaypoint.Text = string.Format("{0} {1}", Captions.CALCULATE, EnumHelper.smethod_0(rnavCommonWaypoint_0))
#             dlgCalculateWaypoint.Type = rnavCommonWaypoint_0
#             dlgCalculateWaypoint.Category = aircraftSpeedCategory_0
#             dlgCalculateWaypoint.From = position_0
#             dlgCalculateWaypoint.RwyThr = position_1
#             dlgCalculateWaypoint.RwyEnd = position_2
#             dlgCalculateWaypoint.Waypoint = position_3
#             bool flag1 = dlgCalculateWaypoint.method_2(iwin32Window_0) == System.Windows.Forms.DialogResult.OK
#             position_1 = dlgCalculateWaypoint.RwyThr
#             position_2 = dlgCalculateWaypoint.RwyEnd
#             if (flag1)
#             {
#                 position_3 = dlgCalculateWaypoint.Waypoint
#             }
#             flag = flag1
#         }
#         return flag
#     }
# }