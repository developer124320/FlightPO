# -*- coding: UTF-8 -*-
'''
Created on 23 Feb 2015

@author: Administrator
'''

from PyQt4.QtGui import QWidget, QFrame, QVBoxLayout, QGroupBox, QSizePolicy, QHBoxLayout, \
    QLabel, QFont, QLineEdit, QToolButton, QIcon, QPixmap, QDialog, QMessageBox, QSpacerItem
from PyQt4.QtCore import QSize, QSizeF, SIGNAL
from FlightPlanner.QgisHelper import Point3D
from FlightPlanner.captureCoordinateTool import CaptureCoordinateToolUpdate
from qgis.core import QgsPoint, QGis
from FlightPlanner.helpers import Unit, Altitude
from FlightPlanner.QgisHelper import QgisHelper, Geo
from FlightPlanner.types import DegreesType, PositionType
from FlightPlanner.Panels.Frame import Frame
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from Type.Degrees import Degrees
from Type.Position import Position




import define, math

from PyQt4 import QtCore, QtGui

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


class PositionPanel(QWidget):
    def __init__(self, parent , annotation = None, parentDialog = None, alwaysShowString = None):
        QWidget.__init__(self, parent)

        while not isinstance(parent, QDialog):
            parent = parent.parent()
        self.setObjectName("PositionPanel" + str(len(parent.findChildren(PositionPanel))))

        self.resize(200, 200)
        self.horizontalLayout = QtGui.QHBoxLayout(self)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.hLayoutGroupBox = QtGui.QHBoxLayout(self.groupBox)
        self.hLayoutGroupBox.setSpacing(0)
        self.hLayoutGroupBox.setMargin(0)
        self.hLayoutGroupBox.setObjectName(_fromUtf8("hLayoutGroupBox"))
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutGroupBox.addItem(spacerItem)
        self.basicFrame = QtGui.QFrame(self.groupBox)
        self.basicFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.basicFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.basicFrame.setObjectName(_fromUtf8("basicFrame"))
        self.hLayout_basicFrame = QtGui.QHBoxLayout(self.basicFrame)
        self.hLayout_basicFrame.setSpacing(6)
        self.hLayout_basicFrame.setMargin(0)
        self.hLayout_basicFrame.setObjectName(_fromUtf8("hLayout_basicFrame"))
        self.framePositionContents = QtGui.QFrame(self.basicFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framePositionContents.sizePolicy().hasHeightForWidth())
        self.framePositionContents.setSizePolicy(sizePolicy)
        self.framePositionContents.setFrameShape(QtGui.QFrame.StyledPanel)
        self.framePositionContents.setFrameShadow(QtGui.QFrame.Raised)
        self.framePositionContents.setObjectName(_fromUtf8("framePositionContents"))
        self.vLayoutPositionContents = QtGui.QVBoxLayout(self.framePositionContents)
        self.vLayoutPositionContents.setSpacing(6)
        self.vLayoutPositionContents.setMargin(0)
        self.vLayoutPositionContents.setObjectName(_fromUtf8("vLayoutPositionContents"))
        self.frameID = QtGui.QFrame(self.framePositionContents)
        self.frameID.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameID.setFrameShadow(QtGui.QFrame.Raised)
        self.frameID.setObjectName(_fromUtf8("frameID"))
        self.hLayoutID = QtGui.QHBoxLayout(self.frameID)
        self.hLayoutID.setSpacing(0)
        self.hLayoutID.setMargin(0)
        self.hLayoutID.setObjectName(_fromUtf8("hLayoutID"))
        self.frameIDContent = QtGui.QFrame(self.frameID)
        self.frameIDContent.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameIDContent.setFrameShadow(QtGui.QFrame.Raised)
        self.frameIDContent.setObjectName(_fromUtf8("frameIDContent"))
        self.hLayoutIDContent = QtGui.QHBoxLayout(self.frameIDContent)
        self.hLayoutIDContent.setSpacing(0)
        self.hLayoutIDContent.setMargin(0)
        self.hLayoutIDContent.setObjectName(_fromUtf8("hLayoutIDContent"))
        self.labelID = QtGui.QLabel(self.frameID)
        self.labelID.setMinimumSize(QtCore.QSize(52, 0))
        self.labelID.setMaximumSize(QtCore.QSize(52, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelID.setFont(font)
        self.labelID.setObjectName(_fromUtf8("labelID"))
        self.hLayoutID.addWidget(self.labelID)
        self.txtID = QtGui.QLineEdit(self.frameID)
        self.txtID.setMinimumSize(QtCore.QSize(100, 0))
        self.txtID.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtID.setFont(font)
        self.txtID.setObjectName(_fromUtf8("txtIID"))
        self.hLayoutID.addWidget(self.txtID)
        # self.hLayoutID.addWidget(self.frameIDContent)
        spacerItem1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutID.addItem(spacerItem1)
        self.vLayoutPositionContents.addWidget(self.frameID)
        self.frameXY_LL = QtGui.QFrame(self.framePositionContents)
        self.frameXY_LL.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameXY_LL.setFrameShadow(QtGui.QFrame.Raised)
        self.frameXY_LL.setObjectName(_fromUtf8("frameXY_LL"))
        self.hLayoutXYLL = QtGui.QHBoxLayout(self.frameXY_LL)
        self.hLayoutXYLL.setSpacing(0)
        self.hLayoutXYLL.setMargin(0)
        self.hLayoutXYLL.setObjectName(_fromUtf8("hLayoutXYLL"))
        self.frameXY = QtGui.QFrame(self.frameXY_LL)
        self.frameXY.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameXY.setFrameShadow(QtGui.QFrame.Raised)
        self.frameXY.setObjectName(_fromUtf8("frameXY"))
        self.vLayoutXY = QtGui.QVBoxLayout(self.frameXY)
        self.vLayoutXY.setSpacing(6)
        self.vLayoutXY.setMargin(0)
        self.vLayoutXY.setObjectName(_fromUtf8("vLayoutXY"))
        self.frameX = QtGui.QFrame(self.frameXY)
        self.frameX.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameX.setFrameShadow(QtGui.QFrame.Raised)
        self.frameX.setObjectName(_fromUtf8("frameX"))
        self.hLayoutX = QtGui.QHBoxLayout(self.frameX)
        self.hLayoutX.setSpacing(0)
        self.hLayoutX.setMargin(0)
        self.hLayoutX.setObjectName(_fromUtf8("hLayoutX"))
        self.labelX = QtGui.QLabel(self.frameX)
        self.labelX.setMinimumSize(QtCore.QSize(50, 0))
        self.labelX.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelX.setFont(font)
        self.labelX.setObjectName(_fromUtf8("labelX"))
        self.hLayoutX.addWidget(self.labelX)
        self.txtPointX = QtGui.QLineEdit(self.frameX)
        self.txtPointX.setMinimumSize(QtCore.QSize(100, 0))
        self.txtPointX.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtPointX.setFont(font)
        self.txtPointX.setObjectName(_fromUtf8("txtPointX"))
        self.hLayoutX.addWidget(self.txtPointX)
        self.vLayoutXY.addWidget(self.frameX)
        self.frameY = QtGui.QFrame(self.frameXY)
        self.frameY.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameY.setFrameShadow(QtGui.QFrame.Raised)
        self.frameY.setObjectName(_fromUtf8("frameY"))
        self.hLayoutY = QtGui.QHBoxLayout(self.frameY)
        self.hLayoutY.setSpacing(0)
        self.hLayoutY.setMargin(0)
        self.hLayoutY.setObjectName(_fromUtf8("hLayoutY"))
        self.labelY = QtGui.QLabel(self.frameY)
        self.labelY.setMinimumSize(QtCore.QSize(50, 0))
        self.labelY.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelY.setFont(font)
        self.labelY.setObjectName(_fromUtf8("labelY"))
        self.hLayoutY.addWidget(self.labelY)
        self.txtPointY = QtGui.QLineEdit(self.frameY)
        self.txtPointY.setMinimumSize(QtCore.QSize(100, 0))
        self.txtPointY.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtPointY.setFont(font)
        self.txtPointY.setObjectName(_fromUtf8("txtPointY"))
        self.hLayoutY.addWidget(self.txtPointY)
        self.vLayoutXY.addWidget(self.frameY)
        self.hLayoutXYLL.addWidget(self.frameXY)
        spacerItem2 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutXYLL.addItem(spacerItem2)
        self.vLayoutPositionContents.addWidget(self.frameXY_LL)
        self.frameAltitude = QtGui.QFrame(self.framePositionContents)
        self.frameAltitude.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameAltitude.setFrameShadow(QtGui.QFrame.Raised)
        self.frameAltitude.setObjectName(_fromUtf8("frameAlitude"))
        self.hLayoutAltitude = QtGui.QHBoxLayout(self.frameAltitude)
        self.hLayoutAltitude.setSpacing(0)
        self.hLayoutAltitude.setMargin(0)
        self.hLayoutAltitude.setObjectName(_fromUtf8("hLayoutAltitude"))

        self.labelAltitude = QtGui.QLabel(self.frameAltitude)
        self.labelAltitude.setMinimumSize(QtCore.QSize(52, 0))
        self.labelAltitude.setMaximumSize(QtCore.QSize(52, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelAltitude.setFont(font)
        self.labelAltitude.setObjectName(_fromUtf8("labelAltitude"))
        self.hLayoutAltitude.addWidget(self.labelAltitude)
        self.frameAltitudeVal = QtGui.QFrame(self.frameAltitude)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameAltitudeVal.sizePolicy().hasHeightForWidth())
        self.frameAltitudeVal.setSizePolicy(sizePolicy)
        self.frameAltitudeVal.setMinimumSize(QtCore.QSize(0, 0))
        self.frameAltitudeVal.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frameAltitudeVal.setFrameShape(QtGui.QFrame.NoFrame)
        self.frameAltitudeVal.setFrameShadow(QtGui.QFrame.Raised)
        self.frameAltitudeVal.setObjectName(_fromUtf8("frameAltitudeVal"))
        self.hLayoutAltitudeVal = QtGui.QHBoxLayout(self.frameAltitudeVal)
        self.hLayoutAltitudeVal.setSpacing(0)
        self.hLayoutAltitudeVal.setMargin(0)
        self.hLayoutAltitudeVal.setObjectName(_fromUtf8("hLayoutAltitudeVal"))

        self.frameAltitudeM = Frame(self.frameAltitudeVal, "HL")
        self.hLayoutAltitudeVal.addWidget(self.frameAltitudeM)

        self.txtAltitudeM = QtGui.QLineEdit(self.frameAltitudeM)
        self.txtAltitudeM.setMinimumSize(QtCore.QSize(100, 20))
        self.txtAltitudeM.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitudeM.setFont(font)
        self.txtAltitudeM.setObjectName(_fromUtf8("txtAltitudeM"))
        self.frameAltitudeM.Add =  self.txtAltitudeM
        self.labelM = QtGui.QLabel(self.frameAltitudeVal)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelM.setFont(font)
        self.labelM.setObjectName(_fromUtf8("labelM"))
        self.labelM.setMinimumSize(QtCore.QSize(20, 20))
        self.frameAltitudeM.Add = self.labelM

        self.frameAltitudeFt = Frame(self.frameAltitudeVal, "HL")
        self.hLayoutAltitudeVal.addWidget(self.frameAltitudeFt)

        self.txtAltitudeFt = QtGui.QLineEdit(self.frameAltitudeFt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtAltitudeFt.sizePolicy().hasHeightForWidth())
        self.txtAltitudeFt.setSizePolicy(sizePolicy)
        self.txtAltitudeFt.setMinimumSize(QtCore.QSize(100, 20))
        self.txtAltitudeFt.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.txtAltitudeFt.setFont(font)
        self.txtAltitudeFt.setObjectName(_fromUtf8("txtAltitudeFt"))
        self.frameAltitudeFt.Add = self.txtAltitudeFt
        self.labelFt = QtGui.QLabel(self.frameAltitudeVal)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelFt.setFont(font)
        self.labelFt.setObjectName(_fromUtf8("labelFt"))
        self.labelFt.setMinimumSize(QtCore.QSize(20, 20))
        self.frameAltitudeFt.Add = self.labelFt
        self.hLayoutAltitude.addWidget(self.frameAltitudeVal)
        spacerItem3 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutAltitude.addItem(spacerItem3)
        self.vLayoutPositionContents.addWidget(self.frameAltitude)
        self.hLayout_basicFrame.addWidget(self.framePositionContents)
        self.btnCapture = QtGui.QPushButton(self.basicFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCapture.sizePolicy().hasHeightForWidth())
        self.btnCapture.setSizePolicy(sizePolicy)
        self.btnCapture.setMinimumSize(QtCore.QSize(25, 0))
        self.btnCapture.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btnCapture.setText(_fromUtf8(""))
        self.btnCapture.setObjectName(_fromUtf8("btnCapture"))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/coordinate_capture.png")), QIcon.Normal, QIcon.Off)
        self.btnCapture.setIcon(icon)

        self.hLayout_basicFrame.addWidget(self.btnCapture)
        self.btnCalculater = QtGui.QPushButton(self.basicFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCalculater.sizePolicy().hasHeightForWidth())
        self.btnCalculater.setSizePolicy(sizePolicy)
        self.btnCalculater.setMinimumSize(QtCore.QSize(25, 0))
        self.btnCalculater.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btnCalculater.setText(_fromUtf8(""))
        self.btnCalculater.setObjectName(_fromUtf8("btnCalculater"))
        icon = QIcon()
        icon.addPixmap(QPixmap(("Resource/Calculator.bmp")), QIcon.Normal, QIcon.Off)
        self.btnCalculater.setIcon(icon)

        self.hLayout_basicFrame.addWidget(self.btnCalculater)
        self.hLayoutGroupBox.addWidget(self.basicFrame)
        spacerItem4 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hLayoutGroupBox.addItem(spacerItem4)
        self.horizontalLayout.addWidget(self.groupBox)


        self.frameLL = Frame(self.frameXY_LL)
        self.frameLL.Spacing = 6
        self.hLayoutXYLL.addWidget(self.frameLL)

        self.txtLat = TextBoxPanel(self.frameLL)
        self.txtLat.Caption = "Latitude"
        self.txtLat.LabelWidth = 60
        self.txtLat.textBox.setMaximumWidth(100)
        self.txtLat.textBox.setMinimumWidth(100)
        self.frameLL.Add = self.txtLat

        self.txtLong = TextBoxPanel(self.frameLL)
        self.txtLong.Caption = "Longitude"
        self.txtLong.LabelWidth = 60
        self.txtLong.textBox.setMaximumWidth(100)
        self.txtLong.textBox.setMinimumWidth(100)
        self.frameLL.Add = self.txtLong

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)



        self.btnCapture.clicked.connect(self.capturePosition)
        self.annotation = annotation
        if self.annotation != None:
            self.annotation.setFrameSize( QSizeF( 41, 20 ) )
        self.CaptureCoordTool = CaptureCoordinateToolUpdate(define._canvas, self.annotation)
        self.connect(self.CaptureCoordTool, SIGNAL("resultPointValueList"), self.resultPointValueListMethod)
        self.txtPointX.editingFinished.connect(self.positionXYChanged)
        self.txtPointY.editingFinished.connect(self.positionXYChanged)
        # self.txtPointX.textChanged.connect(self.positionXYChanged)
        # self.txtPointY.textChanged.connect(self.positionXYChanged)

        self.txtLat.textBox.editingFinished.connect(self.positionGeoChanged)
        self.txtLong.textBox.editingFinished.connect(self.positionGeoChanged)
        # self.txtLong.textBox.textChanged.connect(self.positionGeoChanged)
        # self.txtLong.textBox.textChanged.connect(self.positionGeoChanged)

        # self.txtAltitudeM.textChanged.connect(self.setAnnotation)
        self.txtAltitudeM.textChanged.connect(self._chageFromMToFt)
        self.txtAltitudeFt.textChanged.connect(self._chageFromFtToM)
        self.txtAltitudeM.textChanged.connect(self.setAnnotation)
        self.txtID.textChanged.connect(self.txtID_textChanged)
        # define._canvas.mapUnitsChanged.connect(self.changeMapUnit)
#         self.connect(self, SIGNAL("mapUnitChanged()"), dlg, SLOT("changeMapUnit(dlg)") )
        self.flag = 0
        self.parentDialog = parentDialog
        self.txtAltitudeM.setText("0")

        self.hasAltitudeResult = True
        self.id = None
        self.frameID.hide()

        self.alwwaysShowString = alwaysShowString
        if self.alwwaysShowString == "Degree":
            # self.label_9.setText("Longitude:")
            # self.label_10.setText("Latitude:")
            self.inputType = "LL"
        else:
            self.inputType = "XY"
        self.degreeFormat = None
        self.resultPoint3d = None

        self.flag1 = 0
        self.posType = PositionType.Position
    def positionXYChanged(self):
        try:
            if self.flag1==0:
                self.flag1=1
            if self.flag1==2:
                self.flag1=0
            if self.flag1==1:
                try:
                    flag, degreeLat, degreeLon = Geo.smethod_2(float(self.txtPointX.text()), float(self.txtPointY.text()))
                    self.txtLat.Value = degreeLat.ToString()
                    if len(str(int(degreeLon.value))) == 3:
                        self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                    else:
                        self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")

                    if self.alwwaysShowString == "Degree":
                        self.resultPoint3d = Point3D(degreeLon.value, degreeLat.value, float(self.txtAltitudeM.text()))
                    else:
                        if define._units == QGis.Meters:
                            self.resultPoint3d = Point3D(float(self.txtPointX.text()), float(self.txtPointY.text()), float(self.txtAltitudeM.text()))
                        else:
                            self.resultPoint3d = Point3D(degreeLon.value, degreeLat.value, float(self.txtAltitudeM.text()))

                except:
                    pass
            self.emit(SIGNAL("positionChanged"), self)
        except:
            raise "This plan coordinate can not be converted to geodetic coordinate."
            # QMessageBox.warning(self, "Warning", "This plan coordinate can not be converted to geodetic coordinate.")


    def mouseMoveEvent(self, mouseEvent):
        pt = mouseEvent.pos()
        c = self.childAt(pt)
        pass
    def positionGeoChanged(self):
        try:
            if self.flag1==0:
                self.flag1=2
            if self.flag1==1:
                self.flag1=0
            if self.flag1==2:
                latDegree = Degrees.String2Degree(self.txtLat.Value)
                lonDegree = Degrees.String2Degree(self.txtLong.Value)
                point3dPlan = QgisHelper.CrsTransformPoint(lonDegree.value, latDegree.value, define._latLonCrs, define._xyCrs)
                self.txtPointX.setText(str(point3dPlan.get_X()))
                self.txtPointY.setText(str(point3dPlan.get_Y()))

                if self.alwwaysShowString == "Degree":
                    self.resultPoint3d = Point3D(lonDegree.value, latDegree.value, float(self.txtAltitudeM.text()))
                else:
                    if define._units == QGis.Meters:
                        self.resultPoint3d = Point3D(float(self.txtPointX.text()), float(self.txtPointY.text()), float(self.txtAltitudeM.text()))
                    else:
                        self.resultPoint3d = Point3D(lonDegree.value, latDegree.value, float(self.txtAltitudeM.text()))
            self.emit(SIGNAL("positionChanged"), self)
        except:
            raise "This geodetic coordinate can not be converted to plan coordinate."
            # QMessageBox.warning(self, "Warning", "This geodetic coordinate can not be converted to plan coordinate.")

    def resultPointValueListMethod(self, resultValueList):
        degreeLat = None
        degreeLon = None
        if len(resultValueList) > 0:
            self.id = resultValueList[0]
            if define._units == QGis.Meters:
                self.txtPointX.setText(resultValueList[1])
                self.txtPointY.setText(resultValueList[2])
                try:
                    flag, degreeLat, degreeLon = Geo.smethod_2(float(self.txtPointX.text()), float(self.txtPointY.text()))
                    self.txtLat.Value = degreeLat.ToString()
                    if len(str(int(degreeLon.value))) == 3:
                        self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                    else:
                        self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")
                except:
                    pass
            else:
                degreeLat = Degrees(float(resultValueList[2]), None, None, DegreesType.Latitude)
                degreeLon = Degrees(float(resultValueList[1]), None, None, DegreesType.Longitude)
                self.txtLat.Value = degreeLat.ToString()
                if len(str(int(degreeLon.value))) == 3:
                    self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                else:
                    self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")

                flag, xVal, yVal = Geo.smethod_3(degreeLat, degreeLon)
                if flag:
                    self.txtPointX.setText(str(xVal))
                    self.txtPointY.setText(str(yVal))

            # self.txtPointX.setText(resultValueList[1])
            # self.txtPointY.setText(resultValueList[2])
            if self.alwwaysShowString == "Degree":
                self.resultPoint3d = Point3D(degreeLon.value, degreeLat.value, float(resultValueList[3]))
            else:
                self.resultPoint3d = Point3D(float(resultValueList[1]), float(resultValueList[2]), float(resultValueList[3]))
            self.resultPoint3d.ID = self.id
            self.txtAltitudeM.setText(str(round(float(resultValueList[3]))))
            self.txtID.setText(resultValueList[0])
            self.setAnnotation()
        self.emit(SIGNAL("captureFinished"), self)
        self.emit(SIGNAL("positionChanged"), self)

    def getUnit(self):
        if self.IsValid():
            if math.fabs(self.Point3d.get_X()) > 180 or math.fabs(self.Point3d.get_Y()) > 90:
                return QGis.Meters
            return QGis.DecimalDegrees
        return None


    def getPoint3D(self):
        return self.resultPoint3d

    def setPoint3D(self, point_0):
        degreeLon = None
        degreeLat = None
        if point_0 == None:
            self.txtPointX.setText("")
            self.txtPointY.setText("")
            self.txtLat.Value = ""
            self.txtLong.Value = ""
            self.txtAltitudeM.setText("0.0")
            self.resultPoint3d = None
            return
        else:
            if (math.fabs(point_0.get_X()) >= 89.99999999 and math.fabs(point_0.get_Y()) >= 180):
                self.txtPointX.setText(str(point_0.get_X()))
                self.txtPointY.setText(str(point_0.get_Y()))
                try:
                    flag, degreeLat, degreeLon = Geo.smethod_2(float(self.txtPointX.text()), float(self.txtPointY.text()))
                    self.txtLat.Value = degreeLat.ToString()
                    if len(str(int(degreeLon.value))) == 3:
                        self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                    else:
                        self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")
                except:
                    pass
            else:
                degreeLat = Degrees(point_0.get_Y(), None, None, DegreesType.Latitude)
                degreeLon = Degrees(point_0.get_X(), None, None, DegreesType.Longitude)
                self.txtLat.Value = degreeLat.ToString()
                if len(str(int(degreeLon.value))) == 3:
                    self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                else:
                    self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")

                flag, xVal, yVal = Geo.smethod_3(degreeLat, degreeLon)
                if flag:
                    self.txtPointX.setText(str(xVal))
                    self.txtPointY.setText(str(yVal))
            self.txtAltitudeM.setText(str(point_0.get_Z()))
            if isinstance(point_0, Point3D):
                self.txtID.setText(point_0.ID)
            if self.alwwaysShowString == "Degree" or define._units != QGis.Meters:
                self.resultPoint3d = Point3D(degreeLon.value, degreeLat.value, point_0.get_Z())
            else:
                self.resultPoint3d = Point3D(float(self.txtPointX.text()), float(self.txtPointY.text()), point_0.get_Z())
            self.setAnnotation()

    Point3d = property(getPoint3D, setPoint3D, None, None)
    def txtID_textChanged(self):
        self.id = self.txtID.text()
    def get_ID(self):
        if self.id == None:
            return ""
        return self.id
    def set_ID(self, idStr):
        self.txtID.setText(idStr)
    ID = property(get_ID, set_ID, None, None)

    def setPosition(self, x, y):
        degreeLat = None
        degreeLon = None
        if (math.fabs(x) >= 89.99999999 and math.fabs(y) >= 180):
            self.txtPointX.setText(str(x))
            self.txtPointY.setText(str(y))
            try:
                flag, degreeLat, degreeLon = Geo.smethod_2(float(self.txtPointX.text()), float(self.txtPointY.text()))
                self.txtLat.Value = degreeLat.ToString()
                if len(str(int(degreeLon.value))) == 3:
                    self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
                else:
                    self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")
            except:
                pass
        else:
            degreeLat = Degrees(y, None, None, DegreesType.Latitude)
            degreeLon = Degrees(x, None, None, DegreesType.Longitude)
            self.txtLat.Value = degreeLat.ToString()
            if len(str(int(degreeLon.value))) == 3:
                self.txtLong.Value = degreeLon.ToString("dddmmss.ssssH")
            else:
                self.txtLong.Value = degreeLon.ToString("ddmmss.ssssH")

            flag, xVal, yVal = Geo.smethod_3(degreeLat, degreeLon)
            if flag:
                self.txtPointX.setText(str(xVal))
                self.txtPointY.setText(str(yVal))
        if self.alwwaysShowString == "Degree":
            self.resultPoint3d = Point3D(degreeLon.value, degreeLat.value)
        else:
            self.resultPoint3d = Point3D(x, y)
        self.setAnnotation()

    def capturePosition(self):
#         if self.btnCapture.isChecked():
        define._canvas.setMapTool(self.CaptureCoordTool)
        
#             if self.parentDialog != None:
#                 self.parentDialog.hide()
#         else:
#             define._canvas.setMapTool(QgsMapToolPan(define._canvas))
    def setAnnotation(self):

        if self.txtPointX.text() !="" and self.txtPointY.text() != "" and self.annotation != None:            
            self.annotation.show()                                        
            self.annotation.setMapPosition(QgsPoint(float(self.txtPointX.text()), float(self.txtPointY.text())))

        self.emit(SIGNAL("positionChanged"), self)
    def _chageFromMToFt(self):
        if self.flag==0:
            self.flag=1
        if self.flag==2:
            self.flag=0
        if self.flag==1:
            try:
                self.txtAltitudeFt.setText(str(round(Unit.ConvertMeterToFeet(float(self.txtAltitudeM.text())), 4)))
                try:
                    self.resultPoint3d = Point3D(self.resultPoint3d.get_X(), self.resultPoint3d.get_Y(), float(self.txtAltitudeM.text()))
                except:
                    pass
            except ValueError:
                self.txtAltitudeFt.setText("")
    def _chageFromFtToM(self):
        if self.flag==0:
            self.flag=2
        if self.flag==1:
            self.flag=0
        if self.flag==2:
            try:
                self.txtAltitudeM.setText(str(round(Unit.ConvertFeetToMeter(float(self.txtAltitudeFt.text())), 4)))
                try:
                    self.resultPoint3d = Point3D(self.resultPoint3d.get_X(), self.resultPoint3d.get_Y(), float(self.txtAltitudeM.text()))
                except:
                    pass
            except ValueError:
                self.txtAltitudeM.setText("")
    def Altitude(self):
        try:
            return Altitude(float(self.txtAltitudeM.text()))
        except ValueError:
            return Altitude.NaN()
    def IsValid(self):
        try:
            x = float(self.txtPointX.text())
        except:
            return False
        try:
            y = float(self.txtPointY.text())
        except ValueError:
            return False
        if self.frameAltitude.isVisible():
            try:
                m = float(self.txtPointY.text())
            except ValueError:
                return False
        return True
    def hideframe_Altitude(self):
        self.frameAltitude.hide()
        self.hasAltitudeResult = False
    def hideframe_ID(self):
        self.frameID.setVisible(False)
    def showframe_ID(self):
        self.frameID.setVisible(True)
    def changeMapUnit(self):
        pass

    def get_hasAltitudeResult(self):
        return self.hasAltitudeResult
    hasAltitude = property(get_hasAltitudeResult, None, None, None)
    def method_3(self):#out Degrees degrees_0, out Degrees degrees_1)
        if self.getUnit() != QGis.Meters:
            try:
                return True, self.resultPoint3d.get_Y(), self.resultPoint3d.get_X()
            except:
                return False, None, None
        else:
            point3dGeo = QgisHelper.CrsTransformPoint(self.resultPoint3d.get_X(), self.resultPoint3d.get_Y(), define._xyCrs, define._latLonCrs)
            try:
                return True, point3dGeo.get_Y(), point3dGeo.get_X()
            except:
                return False, None, None
        
    def method_5(self, degrees_0, degrees_1):
        num = None
        num1 = None
        self.txtLat.Value = degrees_0.ToString()
        if len(str(int(degrees_1))) == 3:
            self.txtLong.Value = degrees_1.ToString("dddmmss.ssssH")
        else:
            self.txtLong.Value = degrees_1.ToString("ddmmss.ssssH")

        flag, xVal, yVal = Geo.smethod_3(degrees_0, degrees_1)
        if flag:
            self.txtPointX.setText(str(xVal))
            self.txtPointY.setText(str(yVal))
        self.resultPoint3d.ID = self.id
        self.txtAltitudeM.setText(str(0.0))
        self.resultPoint3d = Point3D(degrees_1.value, degrees_0.value)
        self.txtID.setText("")
        return True
    
    def method_8(self, string_0):
        # stringBuilder = None
        # if (self.hasID && self.txtID.Text.Trim() != "")
        # {
        #     stringBuilder.AppendLine(string.Format("{0}{1}\t{2}", string_0, self.lblID.Caption, self.txtID.Text))
        # }
        if self.IsValid():
            stringBuilder = "%s%s\t%s"%(string_0, self.labelX.text(), self.txtPointX.text()) + "\n"
            stringBuilder += "%s%s\t%s"%(string_0, self.labelY.text(), self.txtPointY.text()) + "\n"
            if self.hasAltitudeResult and self.txtAltitudeM.text() != "0":
                stringBuilder += "%s%s\t%s %s (%s %s)"%(string_0, "Altitude:", self.txtAltitudeM.text(), "m", self.txtAltitudeFt.text(), "Ft")
            return stringBuilder
        return ""

    def get_Caption(self):
        caption = self.groupBox.title()
        return caption
    def set_Caption(self, captionStr):
        self.groupBox.setTitle(captionStr)
    Caption = property(get_Caption, set_Caption, None, None)

    def get_Enabled(self):
        return self.groupBox.isEnabled()
    def set_Enabled(self, bool):
        self.groupBox.setEnabled(bool)
    Enabled = property(get_Enabled, set_Enabled, None, None)

    def get_Visible(self):
        return self.isVisible()
    def set_Visible(self, bool):
        self.setVisible(bool)
    Visible = property(get_Visible, set_Visible, None, None)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.labelID.setText(_translate("Form", "ID :", None))
        self.labelX.setText(_translate("Form", "X :", None))
        self.labelY.setText(_translate("Form", "Y :", None))
        self.labelAltitude.setText(_translate("Form", "Altitude:", None))
        self.labelM.setText(_translate("Form", "m", None))
        self.labelFt.setText(_translate("Form", "ft", None))

    def get_Position(self):
        position = None
        if(self.inputType != "XY"):
            position = Position(None, None, None, None, None, Degrees.smethod_1(self.Point3d.get_X()), Degrees.smethod_5(self.Point3d.get_Y()))
        else:
            position = Position(None, None, self.Point3d.get_X(), self.Point3d.get_Y())
        position.ID = self.txtID.text()
        if (self.hasAltitude):
            position.altitude = self.Point3d.get_Z()
        position.Type = self.posType
        return position
    def set_Position(self, position):
        num = None
        num1 = None
        degree = None
        degree1 = None
        # self.method_1()
        self.updating = True
        if (position == None):
            self.posType = PositionType.Position
        else:
            self.posType = position.Type
            self.txtID.setText(position.ID)
            self.Point3d = position.Point3d
    PositionValue = property(get_Position, set_Position, None, None)

