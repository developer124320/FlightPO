# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HoldingRace_P.ui'
#
# Created: Fri Aug 21 18:44:01 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
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

class Ui_HoldingRace_P(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(467, 365)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        Form.setFont(font)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbVorDmePosition = QtGui.QGroupBox(Form)
        self.gbVorDmePosition.setObjectName(_fromUtf8("gbVorDmePosition"))
        self.vl_VorDmePosition = QtGui.QVBoxLayout(self.gbVorDmePosition)
        self.vl_VorDmePosition.setObjectName(_fromUtf8("vl_VorDmePosition"))
        self.verticalLayout.addWidget(self.gbVorDmePosition)
        self.gbParameters = QtGui.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(False)
        font.setWeight(50)
        self.gbParameters.setFont(font)
        self.gbParameters.setObjectName(_fromUtf8("gbParameters"))
        self.vl_gbParameters = QtGui.QVBoxLayout(self.gbParameters)
        self.vl_gbParameters.setObjectName(_fromUtf8("vl_gbParameters"))
        self.frameAircraftCategory = QtGui.QFrame(self.gbParameters)
        self.frameAircraftCategory.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameAircraftCategory.setFrameShadow(QtGui.QFrame.Raised)
        self.frameAircraftCategory.setObjectName(_fromUtf8("frameAircraftCategory"))
        self.horizontalLayout_61 = QtGui.QHBoxLayout(self.frameAircraftCategory)
        self.horizontalLayout_61.setSpacing(0)
        self.horizontalLayout_61.setMargin(0)
        self.horizontalLayout_61.setObjectName(_fromUtf8("horizontalLayout_61"))
        self.label_69 = QtGui.QLabel(self.frameAircraftCategory)
        self.label_69.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_69.setFont(font)
        self.label_69.setObjectName(_fromUtf8("label_69"))
        self.horizontalLayout_61.addWidget(self.label_69)
        self.cmbAircraftCategory = QtGui.QComboBox(self.frameAircraftCategory)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbAircraftCategory.sizePolicy().hasHeightForWidth())
        self.cmbAircraftCategory.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbAircraftCategory.setFont(font)
        self.cmbAircraftCategory.setObjectName(_fromUtf8("cmbAircraftCategory"))
        self.horizontalLayout_61.addWidget(self.cmbAircraftCategory)
        self.vl_gbParameters.addWidget(self.frameAircraftCategory)
        self.frameIas = QtGui.QFrame(self.gbParameters)
        self.frameIas.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameIas.setFrameShadow(QtGui.QFrame.Raised)
        self.frameIas.setObjectName(_fromUtf8("frameIas"))
        self.horizontalLayout_60 = QtGui.QHBoxLayout(self.frameIas)
        self.horizontalLayout_60.setSpacing(0)
        self.horizontalLayout_60.setMargin(0)
        self.horizontalLayout_60.setObjectName(_fromUtf8("horizontalLayout_60"))
        self.label_68 = QtGui.QLabel(self.frameIas)
        self.label_68.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_68.setFont(font)
        self.label_68.setObjectName(_fromUtf8("label_68"))
        self.horizontalLayout_60.addWidget(self.label_68)
        self.txtIas = QtGui.QLineEdit(self.frameIas)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtIas.setFont(font)
        self.txtIas.setObjectName(_fromUtf8("txtIas"))
        self.horizontalLayout_60.addWidget(self.txtIas)
        self.vl_gbParameters.addWidget(self.frameIas)
        self.frameTas = QtGui.QFrame(self.gbParameters)
        self.frameTas.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameTas.setFrameShadow(QtGui.QFrame.Raised)
        self.frameTas.setObjectName(_fromUtf8("frameTas"))
        self.horizontalLayout_68 = QtGui.QHBoxLayout(self.frameTas)
        self.horizontalLayout_68.setSpacing(0)
        self.horizontalLayout_68.setMargin(0)
        self.horizontalLayout_68.setObjectName(_fromUtf8("horizontalLayout_68"))
        self.label_76 = QtGui.QLabel(self.frameTas)
        self.label_76.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_76.setFont(font)
        self.label_76.setObjectName(_fromUtf8("label_76"))
        self.horizontalLayout_68.addWidget(self.label_76)
        self.txtTas = QtGui.QLineEdit(self.frameTas)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtTas.setFont(font)
        self.txtTas.setText(_fromUtf8(""))
        self.txtTas.setObjectName(_fromUtf8("txtTas"))
        self.horizontalLayout_68.addWidget(self.txtTas)
        self.vl_gbParameters.addWidget(self.frameTas)
        self.frameAltitude = QtGui.QFrame(self.gbParameters)
        self.frameAltitude.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameAltitude.setFrameShadow(QtGui.QFrame.Raised)
        self.frameAltitude.setObjectName(_fromUtf8("frameAltitude"))
        self.horizontalLayout_69 = QtGui.QHBoxLayout(self.frameAltitude)
        self.horizontalLayout_69.setSpacing(0)
        self.horizontalLayout_69.setMargin(0)
        self.horizontalLayout_69.setObjectName(_fromUtf8("horizontalLayout_69"))
        self.label_77 = QtGui.QLabel(self.frameAltitude)
        self.label_77.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_77.setFont(font)
        self.label_77.setObjectName(_fromUtf8("label_77"))
        self.horizontalLayout_69.addWidget(self.label_77)
        self.txtAltitude = QtGui.QLineEdit(self.frameAltitude)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitude.setFont(font)
        self.txtAltitude.setObjectName(_fromUtf8("txtAltitude"))
        self.horizontalLayout_69.addWidget(self.txtAltitude)
        self.vl_gbParameters.addWidget(self.frameAltitude)
        self.frameIsa = QtGui.QFrame(self.gbParameters)
        self.frameIsa.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameIsa.setFrameShadow(QtGui.QFrame.Raised)
        self.frameIsa.setObjectName(_fromUtf8("frameIsa"))
        self.horizontalLayout_72 = QtGui.QHBoxLayout(self.frameIsa)
        self.horizontalLayout_72.setSpacing(0)
        self.horizontalLayout_72.setMargin(0)
        self.horizontalLayout_72.setObjectName(_fromUtf8("horizontalLayout_72"))
        self.label_80 = QtGui.QLabel(self.frameIsa)
        self.label_80.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_80.setFont(font)
        self.label_80.setObjectName(_fromUtf8("label_80"))
        self.horizontalLayout_72.addWidget(self.label_80)
        self.txtIsa = QtGui.QLineEdit(self.frameIsa)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtIsa.setFont(font)
        self.txtIsa.setObjectName(_fromUtf8("txtIsa"))
        self.horizontalLayout_72.addWidget(self.txtIsa)
        self.vl_gbParameters.addWidget(self.frameIsa)
        self.frameMoc = QtGui.QFrame(self.gbParameters)
        self.frameMoc.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameMoc.setFrameShadow(QtGui.QFrame.Raised)
        self.frameMoc.setObjectName(_fromUtf8("frameMoc"))
        self.horizontalLayout_74 = QtGui.QHBoxLayout(self.frameMoc)
        self.horizontalLayout_74.setSpacing(0)
        self.horizontalLayout_74.setMargin(0)
        self.horizontalLayout_74.setObjectName(_fromUtf8("horizontalLayout_74"))
        self.label_82 = QtGui.QLabel(self.frameMoc)
        self.label_82.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_82.setFont(font)
        self.label_82.setObjectName(_fromUtf8("label_82"))
        self.horizontalLayout_74.addWidget(self.label_82)
        self.txtMoc = QtGui.QLineEdit(self.frameMoc)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtMoc.setFont(font)
        self.txtMoc.setObjectName(_fromUtf8("txtMoc"))
        self.horizontalLayout_74.addWidget(self.txtMoc)
        self.vl_gbParameters.addWidget(self.frameMoc)
        self.frameIas_2 = QtGui.QFrame(self.gbParameters)
        self.frameIas_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameIas_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frameIas_2.setObjectName(_fromUtf8("frameIas_2"))
        self.horizontalLayout_62 = QtGui.QHBoxLayout(self.frameIas_2)
        self.horizontalLayout_62.setSpacing(0)
        self.horizontalLayout_62.setMargin(0)
        self.horizontalLayout_62.setObjectName(_fromUtf8("horizontalLayout_62"))
        self.label_70 = QtGui.QLabel(self.frameIas_2)
        self.label_70.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_70.setFont(font)
        self.label_70.setObjectName(_fromUtf8("label_70"))
        self.horizontalLayout_62.addWidget(self.label_70)
        self.spinBoxMocmulipiler = QtGui.QSpinBox(self.frameIas_2)
        self.spinBoxMocmulipiler.setProperty("value", 1)
        self.spinBoxMocmulipiler.setObjectName(_fromUtf8("spinBoxMocmulipiler"))
        self.horizontalLayout_62.addWidget(self.spinBoxMocmulipiler)
        self.vl_gbParameters.addWidget(self.frameIas_2)
        self.verticalLayout.addWidget(self.gbParameters)
        self.gbOrientation = QtGui.QGroupBox(Form)
        self.gbOrientation.setObjectName(_fromUtf8("gbOrientation"))
        self.vl_gbOrientation = QtGui.QVBoxLayout(self.gbOrientation)
        self.vl_gbOrientation.setObjectName(_fromUtf8("vl_gbOrientation"))

        self.txtTrack = TrackRadialBoxPanel(self.gbOrientation)
        self.txtTrack.Caption = "In-bound Track"
        self.vl_gbOrientation.addWidget(self.txtTrack)
        # self.frameTrackRoot = QtGui.QFrame(self.gbOrientation)
        # self.frameTrackRoot.setFrameShape(QtGui.QFrame.NoFrame)
        # self.frameTrackRoot.setFrameShadow(QtGui.QFrame.Raised)
        # self.frameTrackRoot.setObjectName(_fromUtf8("frameTrackRoot"))
        # self.horizontalLayout_63 = QtGui.QHBoxLayout(self.frameTrackRoot)
        # self.horizontalLayout_63.setSpacing(0)
        # self.horizontalLayout_63.setMargin(0)
        # self.horizontalLayout_63.setObjectName(_fromUtf8("horizontalLayout_63"))
        # self.label_71 = QtGui.QLabel(self.frameTrackRoot)
        # self.label_71.setMinimumSize(QtCore.QSize(250, 0))
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.label_71.setFont(font)
        # self.label_71.setObjectName(_fromUtf8("label_71"))
        # self.horizontalLayout_63.addWidget(self.label_71)
        # self.frameTrack = QtGui.QFrame(self.frameTrackRoot)
        # self.frameTrack.setFrameShape(QtGui.QFrame.StyledPanel)
        # self.frameTrack.setFrameShadow(QtGui.QFrame.Raised)
        # self.frameTrack.setObjectName(_fromUtf8("frameTrack"))
        # self.horizontalLayout_10 = QtGui.QHBoxLayout(self.frameTrack)
        # self.horizontalLayout_10.setSpacing(0)
        # self.horizontalLayout_10.setMargin(0)
        # self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        # self.txtTrack = QtGui.QLineEdit(self.frameTrack)
        # self.txtTrack.setEnabled(True)
        # font = QtGui.QFont()
        # font.setBold(False)
        # font.setWeight(50)
        # self.txtTrack.setFont(font)
        # self.txtTrack.setObjectName(_fromUtf8("txtTrack"))
        # self.horizontalLayout_10.addWidget(self.txtTrack)
        # self.btnCaptureTrack = QtGui.QToolButton(self.frameTrack)
        # self.btnCaptureTrack.setText(_fromUtf8(""))
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8("Resource/coordinate_capture.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btnCaptureTrack.setIcon(icon)
        # self.btnCaptureTrack.setObjectName(_fromUtf8("btnCaptureTrack"))
        # self.horizontalLayout_10.addWidget(self.btnCaptureTrack)
        # self.horizontalLayout_63.addWidget(self.frameTrack)
        # self.vl_gbOrientation.addWidget(self.frameTrackRoot)
        self.frameOrientation = QtGui.QFrame(self.gbOrientation)
        self.frameOrientation.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameOrientation.setFrameShadow(QtGui.QFrame.Raised)
        self.frameOrientation.setObjectName(_fromUtf8("frameOrientation"))
        self.horizontalLayout_67 = QtGui.QHBoxLayout(self.frameOrientation)
        self.horizontalLayout_67.setSpacing(0)
        self.horizontalLayout_67.setMargin(0)
        self.horizontalLayout_67.setObjectName(_fromUtf8("horizontalLayout_67"))
        self.label_75 = QtGui.QLabel(self.frameOrientation)
        self.label_75.setMinimumSize(QtCore.QSize(250, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_75.setFont(font)
        self.label_75.setObjectName(_fromUtf8("label_75"))
        self.horizontalLayout_67.addWidget(self.label_75)
        self.cmbOrientation = QtGui.QComboBox(self.frameOrientation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrientation.sizePolicy().hasHeightForWidth())
        self.cmbOrientation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.cmbOrientation.setFont(font)
        self.cmbOrientation.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.cmbOrientation.setObjectName(_fromUtf8("cmbOrientation"))
        self.horizontalLayout_67.addWidget(self.cmbOrientation)
        self.vl_gbOrientation.addWidget(self.frameOrientation)
        self.verticalLayout.addWidget(self.gbOrientation)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.gbVorDmePosition.setTitle(_translate("Form", "Insertion Position", None))
        self.gbParameters.setTitle(_translate("Form", "Parameters", None))
        self.label_69.setText(_translate("Form", "Aircraft Category:", None))
        self.label_68.setText(_translate("Form", "IAS (kts):", None))
        self.txtIas.setText(_translate("Form", "250", None))
        self.label_76.setText(_translate("Form", "TAS (kts):", None))
        self.label_77.setText(_translate("Form", "Altitude (ft):", None))
        self.txtAltitude.setText(_translate("Form", "10000", None))
        self.label_80.setText(_translate("Form", "ISA (°C):", None))
        self.txtIsa.setText(_translate("Form", "15", None))
        self.label_82.setText(_translate("Form", "Moc (m):", None))
        self.txtMoc.setText(_translate("Form", "300", None))
        self.label_70.setText(_translate("Form", "MOCmultipiler:", None))
        self.gbOrientation.setTitle(_translate("Form", "Orientation", None))
        # self.label_71.setText(_translate("Form", "In-bound Track (°):", None))
        # self.txtTrack.setText(_translate("Form", "0", None))
        self.label_75.setText(_translate("Form", "Turns:", None))

