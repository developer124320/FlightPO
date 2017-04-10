# -*- coding: UTF-8 -*-
'''
Created on Mar 24, 2015

@author: Administrator
'''
import math

from PyQt4.QtCore import QAbstractTableModel, Qt, QVariant, SIGNAL, QModelIndex
from PyQt4.QtGui import QStandardItem

from FlightPlanner.types import Point3D, RnpArSegmentType, AngleUnits, \
        AngleGradientSlopeUnits, RnpArLegType, TurnDirection, RnpArCalculatedLegType, \
        AircraftSpeedCategory, AltitudeUnits, ObstacleTableColumnType, \
        CriticalObstacleType, SurfaceTypes
        
from FlightPlanner.helpers import Unit, MathHelper, Speed, Altitude, Distance, AngleGradientSlope
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint
from FlightPlanner.Obstacle.ObstacleArea import PrimaryObstacleArea
from FlightPlanner.Polyline import Polyline, PolylinePoint
from FlightPlanner.Captions import Captions
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.Obstacle.ObstacleTable import ObstacleTable
from FlightPlanner.AcadHelper import AcadHelper

from qgis.core import QGis, QgsVectorLayer, QgsFeature, QgsGeometry, QgsField
import define

class RnpArLeg:

    def __init__(self, rnpArLegType_0):
        self.method_0()
        self.Type = rnpArLegType_0

    def get_type_text(self):
        if (not self.IsFAP):
            return self.Type
        return self.Type + " - " + Captions.FAP


    def set_type_text(self, value):
        self.Type = value[0:1]


    def del_type_text(self):
        del self.__TypeText


    def get_rnp(self):
        return self.__Rnp


    def set_rnp(self, value):
        self.__Rnp = value


    def del_rnp(self):
        del self.__Rnp


    def RnpArLeg(self, xmlFile_0, xmlNode_0):
        self.method_0();
        self.method_1(xmlFile_0, xmlNode_0)

    def method_0(self):
        self.Altitude = None
        self.Bank = None
        self.Inbound = None
        self.Previous = Point3D()
        self.Position = Point3D()
        self.Radius = Distance.NaN()
        self.Rnp = None
        self.Wind = Speed.NaN()
        self.IsFAP = False

    def method_1(self, xmlFile_0, xmlElement_0):
        pass
#         xmlFile_0.method_15(xmlElement_0, "Type", out num1);
#         self.Type = (RnpArLegType)num1;
#         xmlFile_0.method_63(xmlElement_0, "Position", out position);
#         self.Position = position;
#         xmlFile_0.method_23(xmlElement_0, "RNP", out num);
#         self.Rnp = num;
#         xmlFile_0.method_35(xmlElement_0, "Altitude", out altitude);
#         self.Altitude = altitude;
#         xmlFile_0.method_43(xmlElement_0, "Wind", out speed);
#         self.Wind = speed;
#         xmlFile_0.method_23(xmlElement_0, "Bank", out num);
#         self.Bank = num;
#         xmlFile_0.method_11(xmlElement_0, "IsFAP", out flag);
#         self.IsFAP = flag;
#         xmlFile_0.method_23(xmlElement_0, "Inbound", out num);
#         self.Inbound = num;
#         xmlFile_0.method_39(xmlElement_0, "Radius", out distance);
#         self.Radius = distance;
#         xmlFile_0.method_15(xmlElement_0, "Segment", out num1);
#         self.Segment = (RnpArSegmentType)num1;
#         xmlFile_0.method_63(xmlElement_0, "Previous", out position);
#         self.Previous = position;

    def method_2(self, xmlFile_0, xmlNode_0):
        pass
#         XmlElement xmlElement = xmlFile_0.CreateElement("RnpArLeg");
#         xmlFile_0.method_17(xmlElement, "Type", (int)self.Type);
#         xmlFile_0.method_65(xmlElement, "Position", self.Position);
#         xmlFile_0.method_25(xmlElement, "RNP", self.Rnp);
#         xmlFile_0.method_37(xmlElement, "Altitude", self.Altitude);
#         xmlFile_0.method_45(xmlElement, "Wind", self.Wind);
#         xmlFile_0.method_25(xmlElement, "Bank", self.Bank);
#         xmlFile_0.method_13(xmlElement, "IsFAP", self.IsFAP);
#         xmlFile_0.method_25(xmlElement, "Inbound", self.Inbound);
#         xmlFile_0.method_41(xmlElement, "Radius", self.Radius);
#         xmlFile_0.method_17(xmlElement, "Segment", (int)self.Segment);
#         xmlFile_0.method_65(xmlElement, "Previous", self.Previous);
#         xmlNode_0.AppendChild(xmlElement);

    def method_3(self, rnpArDataGroup_0):
        if self.Segment == RnpArSegmentType.Initial:
            return rnpArDataGroup_0.IAS_IA;
        elif self.Segment == RnpArSegmentType.Intermediate:
            return rnpArDataGroup_0.IAS_I;
        elif self.Segment == RnpArSegmentType.Final:
            return rnpArDataGroup_0.IAS_FA;
        elif self.Segment == RnpArSegmentType.Missed:
            return rnpArDataGroup_0.IAS_MA;
        else:
            raise UserWarning, "Unsupported RNP AR segment type"

    def method_4(self, rnpArDataGroup_0):
        stringBuilder = "    LEG - " + self.TypeText + "\n"
        point3d = self.Position;
        x = point3d.x();
        y = point3d.y();
        if define._units == QGis.Meters:
            stringBuilder += "%s%s\t%f" % ("        ", "X", x)
            stringBuilder += "%s%s\t%f" % ("        ", "Y", y)#.ToString(Formats.GridXYFormat)));
        else:
            stringBuilder += "%s%s\t%f" % ("        ", "Longitude", x)
            stringBuilder += "%s%s\t%f" % ("        ", "Latitude", y)
        rnp = self.Rnp;
        stringBuilder += "%s%s\t%f" % ("        ", "RNP", rnp)
        altitude = self.Altitude;
        stringBuilder += "%s%s\t%f" % ("        ", "Altitude", altitude.method_0(":u"))
        speed = self.method_3(rnpArDataGroup_0);
        stringBuilder += "%s%s\t%f" % ("        ", "IAS", speed.method_0(":u"))
        wind = self.Wind;
        stringBuilder += "%s%s\t%f" % ("        ", "Wind", wind.method_0(":u"))
        num = self.Rnp;
        stringBuilder += "%s%s\t%.1f°" % ("        ", "Bank Angle", num)
        if (self.Type == RnpArLegType.RF):
            radius = self.Radius
            stringBuilder += "%s%s\t%f" % ("        ", "r", radius.method_0(":u"))
        return stringBuilder
    Rnp = property(get_rnp, set_rnp, del_rnp, "RNP")
    TypeText = property(get_type_text, set_type_text, del_type_text, "TypeText's docstring")

class RnpArLegs(QAbstractTableModel): #BindingList<RnpArLeg>

    ColType = 0
    ColRNP = 1
    ColAltitude = 2
    ColWind = 3
    ColBank = 4
    ColInbound = 5
    ColRadius = 6
    ColIsFAP = 7
    ColPreviousX = 8
    ColPreviousY = 9
    ColPositionX = 10
    ColPositionY = 11
    ColCenterPositionX = 12
    ColCenterPositionY = 13
    ColSegment = 14
    
    def __init__(self, type = ""):
        QAbstractTableModel.__init__(self)
        self.dirty = False
        self.rnpArLegsList = []
        # self.dataChanged.connect(self.dataChanged_Event)
        self.type = type
    def updateRow(self, rowIndex, leg):
        self.setData(self.index(rowIndex, 0), QVariant(leg.TypeText))
        self.setData(self.index(rowIndex, 1), QVariant(leg.Rnp))
        self.setData(self.index(rowIndex, 2), QVariant(leg.Altitude.Feet))
        self.setData(self.index(rowIndex, 3), QVariant(leg.Wind.Knots))
        self.setData(self.index(rowIndex, 4), QVariant(leg.Bank))
        self.setData(self.index(rowIndex, 5), QVariant(leg.Inbound))
        self.setData(self.index(rowIndex, 6), QVariant(leg.Radius))
        self.setData(self.index(rowIndex, 7), QVariant(leg.IsFAP))
        self.setData(self.index(rowIndex, 8), QVariant(leg.Previous.x()))
        self.setData(self.index(rowIndex, 9), QVariant(leg.Previous.y()))
        self.setData(self.index(rowIndex, 10), QVariant(leg.Position.x()))
        self.setData(self.index(rowIndex, 11), QVariant(leg.Position.y()))




    def Add(self, rnpArLeg):
        self.beginInsertRows(QModelIndex(), self.RowCount, self.RowCount)
        self.rnpArLegsList.append(rnpArLeg)
        self.endInsertRows()
        self.dirty = True
        return True
    
    def RemoveAt(self, idx):
        self.removeRow(idx)
        
    def removeEndRow(self):
        self.removeRow(self.RowCount - 1)
        
    def get_Count(self):
        return len(self.rnpArLegsList)
    Count = property(get_Count, None, None, None)
    
    def __getitem__(self, i):
        return self.rnpArLegsList[i]
    
    def __setitem__(self, i, value):
        self.rnpArLegsList[i] = value
        
    def __iter__(self):
        return self.rnpArLegsList.__iter__()
    
    def get_rowCount(self):
        return len(self.rnpArLegsList)
    RowCount = property(get_rowCount, None, None, None)
    
    def get_columnCount(self):
        return 15
    ColumnCount = property(get_columnCount, None, None, None)
    
    def rowCount(self, index=QModelIndex()):
        return len(self.rnpArLegsList)
    
    def columnCount(self, index=QModelIndex()):
        return 15
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or \
            not (0 <= index.row() < len(self.rnpArLegsList)):
            return QVariant()
        rnpArLeg = self.rnpArLegsList[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == RnpArLegs.ColType:
                return QVariant(rnpArLeg.TypeText)
            elif column == RnpArLegs.ColRNP:
                return QVariant(rnpArLeg.Rnp)
            elif column == RnpArLegs.ColAltitude:
                return QVariant("%.2f ft" % rnpArLeg.Altitude.Feet)
            elif column == RnpArLegs.ColWind:
                return QVariant("%.2f kts" % rnpArLeg.Wind.Knots if rnpArLeg.Wind.Knots != None else None)
            elif column == RnpArLegs.ColBank:
                return QVariant(unicode("%.2f °" % rnpArLeg.Bank, "utf-8") if rnpArLeg.Bank != None else None)
            elif column == RnpArLegs.ColInbound:
                return QVariant("%.2f" % rnpArLeg.Inbound if rnpArLeg.Inbound != None else None)            
            elif column == RnpArLegs.ColRadius:
                return QVariant("%.2f m" % rnpArLeg.Radius.Metres if rnpArLeg.Radius.IsValid() else None)
            elif column == RnpArLegs.ColIsFAP:
                return QVariant("1" if rnpArLeg.IsFAP else "0")
            elif column == RnpArLegs.ColPositionX:
                return QVariant(str(rnpArLeg.Position.x()))
            elif column == RnpArLegs.ColPositionY:
                return QVariant(str(rnpArLeg.Position.y()))
            elif column == RnpArLegs.ColPreviousX:
                return QVariant(str(rnpArLeg.Previous.x()))
            elif column == RnpArLegs.ColPreviousY:
                return QVariant(str(rnpArLeg.Previous.y()))
            elif column == RnpArLegs.ColSegment:
                return QVariant(str(rnpArLeg.Segment))
            elif column == RnpArLegs.ColCenterPositionX:
                if rnpArLeg.Type == "RF":
                    centerPoint = MathHelper.CalcCenter(rnpArLeg.Inbound, rnpArLeg.Previous, rnpArLeg.Position)
                    return QVariant(str(centerPoint.x()))
                else:
                    return QVariant(None)
            elif column == RnpArLegs.ColCenterPositionY:
                if rnpArLeg.Type == "RF":
                    centerPoint = MathHelper.CalcCenter(rnpArLeg.Inbound, rnpArLeg.Previous, rnpArLeg.Position)
                    return QVariant(str(centerPoint.y()))
                else:
                    return QVariant(None)
            
#             elif column == RnpArLegs.ColPositionZ:
#                 return QVariant(rnpArLeg.Position.get_Z())
        elif role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif (role == Qt.EditRole):
            if column == RnpArLegs.ColType:
                return QVariant(rnpArLeg.TypeText)
            elif column == RnpArLegs.ColRNP:
                return QVariant(rnpArLeg.Rnp)
            elif column == RnpArLegs.ColAltitude:
                return QVariant("%.2f" % rnpArLeg.Altitude.Feet)
            elif column == RnpArLegs.ColWind:
                return QVariant("%.2f" % rnpArLeg.Wind.Knots if rnpArLeg.Wind.Knots != None else None)
            elif column == RnpArLegs.ColBank:
                return QVariant(unicode("%.2f" % rnpArLeg.Bank, "utf-8") if rnpArLeg.Bank != None else None)
            elif column == RnpArLegs.ColInbound:
                return QVariant("%.2f" % rnpArLeg.Inbound if rnpArLeg.Inbound != None else None)            
            elif column == RnpArLegs.ColRadius:
                return QVariant("%.2f" % rnpArLeg.Radius.Metres if rnpArLeg.Radius.IsValid() else None)
            elif column == RnpArLegs.ColIsFAP:
                return QVariant("1" if rnpArLeg.IsFAP else "0")
            elif column == RnpArLegs.ColPositionX:
                return QVariant(str(rnpArLeg.Position.x()))
            elif column == RnpArLegs.ColPositionY:
                return QVariant(str(rnpArLeg.Position.y()))
            elif column == RnpArLegs.ColPreviousX:
                return QVariant(str(rnpArLeg.Previous.x()))
            elif column == RnpArLegs.ColPreviousY:
                return QVariant(str(rnpArLeg.Previous.y()))
            elif column == RnpArLegs.ColSegment:
                return QVariant(str(rnpArLeg.Segment))
            elif column == RnpArLegs.ColCenterPositionX:
                if rnpArLeg.Type == "RF":
                    centerPoint = MathHelper.CalcCenter(rnpArLeg.Inbound, rnpArLeg.Previous, rnpArLeg.Position)
                    return QVariant(str(centerPoint.x()))
            elif column == RnpArLegs.ColCenterPositionY:
                if rnpArLeg.Type == "RF":
                    centerPoint = MathHelper.CalcCenter(rnpArLeg.Inbound, rnpArLeg.Previous, rnpArLeg.Position)
                    return QVariant(str(centerPoint.y()))
        return QVariant()
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == RnpArLegs.ColType:
                return QVariant("Type")
            elif section == RnpArLegs.ColRNP:
                return QVariant("RNP")
            elif section == RnpArLegs.ColAltitude:
                return QVariant("Altitude")
            elif section == RnpArLegs.ColWind:
                return QVariant("Wind")
            elif section == RnpArLegs.ColBank:
                return QVariant("Bank")
            elif section == RnpArLegs.ColInbound:
                return QVariant("Inbound")            
            elif section == RnpArLegs.ColRadius:
                return QVariant("Radius")
            elif section == RnpArLegs.ColIsFAP:
                return QVariant("IsFap")
            elif section == RnpArLegs.ColPositionX:
                return QVariant("EndPointX")
            elif section == RnpArLegs.ColPositionY:
                return QVariant("EndPointY")
            elif section == RnpArLegs.ColPreviousX:
                return QVariant("StartPointX")
            elif section == RnpArLegs.ColPreviousY:
                return QVariant("StartPointY")
            elif section == RnpArLegs.ColCenterPositionX:
                return QVariant("CenterPointX")
            elif section == RnpArLegs.ColCenterPositionY:
                return QVariant("CenterPointY")
            elif section == RnpArLegs.ColSegment:
                return QVariant("Segment")
        return QVariant(int(section + 1))

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)|
                            Qt.ItemIsEditable)

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.rnpArLegsList):
            ship = self.rnpArLegsList[index.row()]
            column = index.column()
            if column == RnpArLegs.ColType:
                ship.Type = str(value.toString())[:2]
            elif column == RnpArLegs.ColSegment:
                ship.Segment = value.toString()
            elif column == RnpArLegs.ColRNP:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Rnp = value
                    
            elif column == RnpArLegs.ColAltitude:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Altitude = Altitude(value, AltitudeUnits.FT)
                # if self.type == "FA":
                #     lptPoint = self.rnpArLegsList[0].Previous
                #     altitudeMetre = Unit.ConvertFeetToMeter(value)
                #     re = 6367435.67964 # radius of the Earth (Metre)
                #     metres = re * math.log1p((re + altitudeMetre)/(re + fAP.Previous.get_Z() + rnpArDataGroup_0.RDH.Metres) - 1)/ rnpArDataGroup_0.VPA.Percent


            elif column == RnpArLegs.ColWind:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Wind = Speed(value)
            elif column == RnpArLegs.ColBank:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Bank = value
            elif column == RnpArLegs.ColInbound:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Inbound = value
                           
            elif column == RnpArLegs.ColRadius:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Radius = Distance(value)
                
            elif column == RnpArLegs.ColIsFAP:
                value, ok = value.toInt()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.IsFAP = value
                
            elif column == RnpArLegs.ColPositionX:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Position.setX(value)
                
            elif column == RnpArLegs.ColPositionY:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Position.setY(value)
                    
            elif column == RnpArLegs.ColPreviousX:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Previous.setX(value)
                
            elif column == RnpArLegs.ColPreviousY:
                value, ok = value.toDouble()
                if not ok:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                ship.Previous.setY(value)
                    
            self.dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
                      index, index)
            return True
        return False

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position,
                             position + rows - 1)
        for row in range(rows):
            self.rnpArLegsList.insert(position + row, RnpArLeg(RnpArLegType.TF))
        self.endInsertRows()
        self.dirty = True
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position,
                             position + rows - 1)
        self.rnpArLegsList = self.rnpArLegsList[:position] + \
                        self.rnpArLegsList[position + rows:]
        self.endRemoveRows()
        self.dirty = True
        return True

    def method_0(self, xmlFile_0, xmlNode_0, string_0):
        xmlNodes = xmlFile_0.CreateElement(string_0)
        for rnpArLeg in self:
            rnpArLeg.method_2(xmlFile_0, xmlNodes);
        xmlNode_0.AppendChild(xmlNodes);

    def method_1(self, rnpArDataGroup_0):
        if (self.RowCount == 0):
            return rnpArDataGroup_0.LTP
        return self[self.RowCount - 1].Position

    def method_2(self, rnpArDataGroup_0, rnpArSegmentType_0): #out bool bool_0)
        bool_0 = False
        if (self.RowCount == 0):
            if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
                return (None, bool_0)
            bool_0 = True
            return MathHelper.getBearing(rnpArDataGroup_0.Legs_FA[0].Position, rnpArDataGroup_0.LTP), bool_0
        if (self.RowCount == 1):
            if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
                return (MathHelper.getBearing(rnpArDataGroup_0.Legs_FA[0].Position, rnpArDataGroup_0.LTP), bool_0)
            return MathHelper.getBearing(rnpArDataGroup_0.LTP, rnpArDataGroup_0.Legs_FA[0].Position), bool_0
        item = self[self.RowCount - 1]
        if (item.Type == RnpArLegType.TF):
            return MathHelper.getBearing(self[self.RowCount - 2].Position, self[self.RowCount - 1].Position), bool_0
        point3d1 = self[self.RowCount - 2].Position
        point3d2 = self[self.RowCount - 1].Position
        point3d3 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d2), MathHelper.calcDistance(point3d1, point3d2) / 2);
        point3d4 = MathHelper.distanceBearingPoint(point3d1, item.Inbound - 1.5707963267949, 100);
        point3d5 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d1, point3d2) - 1.5707963267949, 100);
        point3d = MathHelper.getIntersectionPoint(point3d1, point3d4, point3d3, point3d5)
        point3d4 = MathHelper.distanceBearingPoint(point3d1, item.Inbound, 100);
        bool_0 = True
        if (MathHelper.smethod_115(point3d, point3d1, point3d4)):
            return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) - 1.5707963267949), bool_0
        return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) + 1.5707963267949), bool_0

    def method_3(self, rnpArDataGroup_0):
        if (self.RowCount == 0):
            return None
        if (self.RowCount == 1):
            return MathHelper.getBearing(rnpArDataGroup_0.LTP, self[self.RowCount - 1].Position)
        item = self[self.RowCount - 1]
        point3d1 = self[self.Count - 2].Position
        point3d2 = self[self.Count - 1].Position
        if (item.Type == RnpArLegType.TF):
            return MathHelper.getBearing(point3d1, point3d2)
        point3d3 = MathHelper.distanceBearingPoint(point3d1, MathHelper.getBearing(point3d1, point3d2), MathHelper.calcDistance(point3d1, point3d2) / 2)
        point3d4 = MathHelper.distanceBearingPoint(point3d1, item.Inbound - 1.5707963267949, 100);
        point3d5 = MathHelper.distanceBearingPoint(point3d3, MathHelper.getBearing(point3d1, point3d2) - 1.5707963267949, 100);
        point3d = MathHelper.getIntersectionPoint(point3d1, point3d4, point3d3, point3d5)
        if (MathHelper.smethod_115(point3d, point3d1, MathHelper.distanceBearingPoint(point3d1, item.Inbound, 100))):
            return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) - 1.5707963267949);
        return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) + 1.5707963267949);

    def method_4(self, rnpArDataGroup_0, rnpArSegmentType_0):
        if (self.Count == 0):
            return None
        polyline = Polyline()
        point3d = rnpArDataGroup_0.Smas if rnpArSegmentType_0 == RnpArSegmentType.Missed else rnpArDataGroup_0.LTP
        polyline.AddVertexAt(polyline.get_NumberOfVertices(), point3d, 0, 0, 0)
        for item in self:
            point3d1 = item.Position
            if (item.Type != RnpArLegType.TF):
                polyline.SetBulgeAt(polyline.get_NumberOfVertices() - 1, MathHelper.smethod_59(item.Inbound, point3d, point3d1));
            else:
                polyline.SetBulgeAt(polyline.get_NumberOfVertices() - 1, 0);
            num = 4 * Unit.ConvertNMToMeter(item.Rnp)
            polyline.SetStartWidthAt(polyline.get_NumberOfVertices() - 1, num);
            polyline.SetEndWidthAt(polyline.get_NumberOfVertices() - 1, num);
            polyline.AddVertexAt(polyline.get_NumberOfVertices(), point3d1, 0, 0, 0);
            point3d = point3d1;
        polyline.SetStartWidthAt(polyline.get_NumberOfVertices() - 1, num);
        polyline.SetEndWidthAt(polyline.get_NumberOfVertices() - 1, num);

        return polyline;

    @staticmethod
    def smethod_0(xmlFile_0, xmlNode_0, string_0):
        rnpArLeg = RnpArLegs()
        xmlNodes = xmlNode_0.SelectSingleNode(string_0)
        if (xmlNodes != None):
            xmlNodeLists = xmlNodes.SelectNodes("RnpArLeg")
            if (xmlNodeLists != None):
                for xmlNodes1 in xmlNodeLists:
                    rnpArLeg.Add(RnpArLeg(xmlFile_0, xmlNodes1))
        return rnpArLeg;

class RnpArCalculatedLeg :

    def __init__(self, rnpArDataGroup_0, rnpArSegmentType_0, rnpArLeg_0, rnpArLeg_1, rnpArLeg_2):
        point3dArray = []
        self.StartObj = None
        self.EndObj = None
        self.segment = rnpArSegmentType_0;
        self.moc30 = rnpArDataGroup_0.MOC_MA_30.Metres
        self.moc50 = rnpArDataGroup_0.MOC_MA_50.Metres
        self.courseChangeStart = 0.0
        self.courseChangeEnd = 0.0
        if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
            self.RnpPrevious = rnpArLeg_1.Rnp;
            self.RnpNext = rnpArLeg_2.Rnp if rnpArLeg_2 != None else rnpArLeg_1.Rnp
        else:
            self.RnpPrevious = rnpArLeg_0.Rnp if rnpArLeg_0 != None else rnpArLeg_1.Rnp
            self.RnpNext = rnpArLeg_1.Rnp;
        self.RnpPrevious = Unit.ConvertNMToMeter(self.RnpPrevious);
        self.RnpCurrent = Unit.ConvertNMToMeter(rnpArLeg_1.Rnp);
        self.RnpNext = Unit.ConvertNMToMeter(self.RnpNext)
        if (rnpArLeg_1.Type != RnpArLegType.RF):
            self.EndPoint = rnpArLeg_1.Position
            self.PrimaryPts = PolylineArea();
            self.NominalPts = PolylineArea();
            if (rnpArLeg_0 != None):
                self.StartPoint = rnpArLeg_0.Position
                self.track = MathHelper.getBearing(self.StartPoint, self.EndPoint);
                if (rnpArLeg_0.Type != RnpArLegType.RF):
                    self.Inbound = MathHelper.getBearing(rnpArLeg_0.Previous, rnpArLeg_0.Position)
                    lstTurnDirection = []
                    num1 = MathHelper.smethod_77(self.Inbound, self.track, AngleUnits.Radians, lstTurnDirection)
                    turnDirection = lstTurnDirection[0]
                    if (turnDirection == TurnDirection.Nothing or num1 < Unit.ConvertDegToRad(1)):
                        self.LegType = RnpArCalculatedLegType.STRAIGHT;
                        point3d43 = MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                        point3d44 = MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                        self.PrimaryPts.method_1(point3d44);
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d44, self.track + 3.14159265358979, self.RnpPrevious));
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d43, self.track + 3.14159265358979, self.RnpPrevious));
                        self.PrimaryPts.method_1(point3d43);
                        self.NominalPts.method_1(self.StartPoint);
                        self.StartObj = Polyline()
                        self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), MathHelper.distanceBearingPoint(point3d43, self.track + 3.14159265358979, self.RnpPrevious), 0, 0, 0);
                        self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), MathHelper.distanceBearingPoint(point3d44, self.track + 3.14159265358979, self.RnpPrevious), 0, 0, 0);
                    else:
                        self.courseChangeStart = Unit.smethod_1(num1)
                        self.LegType = RnpArCalculatedLegType.TF
                        naN = Speed.NaN()
                        altitude = Altitude.NaN()
                        wind = Speed.NaN()
                        if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
                            naN = rnpArLeg_1.method_3(rnpArDataGroup_0);
                            altitude = rnpArLeg_0.Altitude;
                            wind = rnpArLeg_0.Wind;
                            bank = rnpArLeg_0.Bank;
                        else:
                            naN = rnpArLeg_1.method_3(rnpArDataGroup_0);
                            altitude = rnpArLeg_1.Altitude;
                            wind = rnpArLeg_1.Wind;
                            bank = rnpArLeg_1.Bank;
                        speed = Speed.smethod_0(naN, rnpArDataGroup_0.ISA, altitude) + wind
                        distance = Distance.smethod_0(speed, bank);
                        metres = distance.Metres
                        #math.tan(num1 / 2);
                        if (turnDirection != TurnDirection.Left):
                            num2 = (3.14159265358979 - num1) / 2;
                            num3 = MathHelper.smethod_4(self.Inbound - num2);
                            point3d45 = MathHelper.distanceBearingPoint(self.StartPoint, num3, 2 * self.RnpCurrent);
                            MathHelper.distanceBearingPoint(self.StartPoint, num3, 2 * self.RnpPrevious);
                            point3d46 = MathHelper.distanceBearingPoint(self.StartPoint, num3 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num2));
                            point3d47 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 3.14159265358979, self.RnpPrevious);
                            point3d48 = MathHelper.distanceBearingPoint(point3d47, self.Inbound + 1.5707963267949, 2 * self.RnpPrevious);
                            point3d49 = MathHelper.distanceBearingPoint(point3d47, self.Inbound - 1.5707963267949, 2 * self.RnpPrevious);
                            point3d50 = MathHelper.distanceBearingPoint(point3d46, self.Inbound + 3.14159265358979, self.RnpPrevious / math.cos(num1 / 2));
                            point3d51 = MathHelper.distanceBearingPoint(point3d50, num3, 4 * self.RnpCurrent / math.sin(num2));
                            point3d47 = MathHelper.distanceBearingPoint(self.StartPoint, num3 + 3.14159265358979, 2 * self.RnpPrevious / math.sin(num2));
                            point3d52 = MathHelper.distanceBearingPoint(point3d47, self.Inbound + 3.14159265358979, self.RnpPrevious / math.cos(num1 / 2));
                            point3d53 = MathHelper.distanceBearingPoint(point3d52, num3, 4 * self.RnpPrevious / math.sin(num2));
                            point3d54 = MathHelper.distanceBearingPoint(point3d46, self.track, (metres + self.RnpCurrent) * math.tan(num1 / 2));
                            point3d55 = MathHelper.distanceBearingPoint(point3d46, self.Inbound + 3.14159265358979, (metres + self.RnpCurrent) * math.tan(num1 / 2));
                            MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpPrevious);
                            point3d56 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound - 1.5707963267949, 2 * self.RnpPrevious);
                            point3d57 = MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                            point3d58 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound - 1.5707963267949, 2 * self.RnpCurrent);
                            point3d14 = MathHelper.getIntersectionPoint(point3d48, point3d49, point3d52, point3d53);
                            point3d59 = MathHelper.distanceBearingPoint(point3d55, self.Inbound + 1.5707963267949, metres + self.RnpCurrent);
                            point3d60 = MathHelper.distanceBearingPoint(point3d59, num3, metres + self.RnpCurrent);
                            if not MathHelper.smethod_115(point3d55, point3d50, point3d51):
                                self.PrimaryPts.method_3(point3d54, MathHelper.smethod_60(point3d54, point3d60, point3d55));
                                polylineArea = self.PrimaryPts
                                point3dArray = [point3d55, point3d50]
                                polylineArea.method_7(point3dArray);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d50, point3d51, point3d59, metres + self.RnpCurrent, lstPoint3D2)
                                point3d15 = lstPoint3D2[0]
                                point3d16 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d54, MathHelper.smethod_60(point3d54, point3d60, point3d16));
                                self.PrimaryPts.method_1(point3d16);
                            if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
                                if (self.RnpPrevious >= self.RnpCurrent):
                                    point3d47 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 3.14159265358979, self.RnpPrevious);
                                    point3d49 = MathHelper.distanceBearingPoint(point3d47, self.Inbound - 1.5707963267949, 2 * self.RnpCurrent);
                                    polylineArea1 = self.PrimaryPts;
                                    point3dArray = [point3d14, point3d49]
                                    polylineArea1.method_7(point3dArray);
                                    self.PrimaryPts.method_3(point3d58, MathHelper.smethod_60(point3d58, point3d45, point3d57));
                                    self.PrimaryPts.method_1(point3d57);
                                else:
                                    polylineArea2 = self.PrimaryPts;
                                    point3dArray = [point3d14, point3d49]
                                    polylineArea2.method_7(point3dArray);
                                    if (not MathHelper.smethod_115(point3d56, point3d52, point3d53)):
                                        self.PrimaryPts.method_1(point3d53);
                                    else:
                                        lstPoint3D2 = []
                                        MathHelper.smethod_34(point3d52, point3d53, self.StartPoint, 2 * self.RnpPrevious, lstPoint3D2)
                                        point3d17 = lstPoint3D2[0]
                                        point3d18 = lstPoint3D2[1]
                                        self.PrimaryPts.method_3(point3d56, MathHelper.smethod_59(self.Inbound, point3d56, point3d18));
                                        self.PrimaryPts.method_1(point3d18);
                                    if (not MathHelper.smethod_115(point3d58, point3d50, point3d51)):
                                        self.PrimaryPts.method_1(point3d51);
                                        self.PrimaryPts.method_3(point3d58, MathHelper.smethod_60(point3d58, point3d45, point3d57));
                                        self.PrimaryPts.method_1(point3d57);
                                    else:
                                        lstPoint3D2 = []
                                        MathHelper.smethod_34(point3d50, point3d51, self.StartPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                        point3d19 = lstPoint3D2[0]
                                        point3d20 = lstPoint3D2[1]
                                        self.PrimaryPts.method_3(point3d20, MathHelper.smethod_60(point3d20, point3d45, point3d57));
                                        self.PrimaryPts.method_1(point3d57);

                            elif (not MathHelper.smethod_115(point3d58, point3d50, point3d51)):
                                self.PrimaryPts.method_1(point3d51);
                                self.PrimaryPts.method_3(point3d58, MathHelper.smethod_60(point3d58, point3d45, point3d57));
                                self.PrimaryPts.method_1(point3d57);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d50, point3d51, self.StartPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d21 = lstPoint3D2[0]
                                point3d22 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d22, MathHelper.smethod_60(point3d22, point3d45, point3d57));
                                self.PrimaryPts.method_1(point3d57);
                            point3d61 = MathHelper.distanceBearingPoint(self.StartPoint, self.track, metres * math.tan(num1 / 2));
                            point3d62 = MathHelper.distanceBearingPoint(point3d61, self.track + 1.5707963267949, metres);
                            point3d63 = MathHelper.distanceBearingPoint(point3d62, num3, metres);
                            self.NominalPts.method_3(point3d63, MathHelper.smethod_57(TurnDirection.Right, point3d63, point3d61, point3d62));
                            self.NominalPts.method_1(point3d61);
                            point3d46 = MathHelper.distanceBearingPoint(self.StartPoint, num3 + 3.14159265358979, 2 * self.RnpPrevious / math.sin(num2));
                            point3d55 = MathHelper.distanceBearingPoint(point3d46, self.Inbound + 3.14159265358979, (metres + self.RnpPrevious) * math.tan(num1 / 2));
                            self.StartObj = Polyline()
                            self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), point3d55, 0, 0, 0);
                            self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), MathHelper.distanceBearingPoint(point3d55, self.Inbound - 1.5707963267949, 4 * self.RnpPrevious), 0, 0, 0);
                        else:
                            num4 = (3.14159265358979 - num1) / 2;
                            num5 = MathHelper.smethod_4(self.Inbound + num4);
                            point3d64 = MathHelper.distanceBearingPoint(self.StartPoint, num5, 2 * self.RnpCurrent);
                            MathHelper.distanceBearingPoint(self.StartPoint, num5, 2 * self.RnpPrevious);
                            point3d65 = MathHelper.distanceBearingPoint(self.StartPoint, num5 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num4));
                            point3d66 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 3.14159265358979, self.RnpPrevious);
                            point3d67 = MathHelper.distanceBearingPoint(point3d66, self.Inbound - 1.5707963267949, 2 * self.RnpPrevious);
                            point3d68 = MathHelper.distanceBearingPoint(point3d66, self.Inbound + 1.5707963267949, 2 * self.RnpPrevious);
                            point3d69 = MathHelper.distanceBearingPoint(point3d65, self.Inbound + 3.14159265358979, self.RnpPrevious / math.cos(num1 / 2));
                            point3d70 = MathHelper.distanceBearingPoint(point3d69, num5, 4 * self.RnpCurrent / math.sin(num4));
                            point3d66 = MathHelper.distanceBearingPoint(self.StartPoint, num5 + 3.14159265358979, 2 * self.RnpPrevious / math.sin(num4));
                            point3d71 = MathHelper.distanceBearingPoint(point3d66, self.Inbound + 3.14159265358979, self.RnpPrevious / math.cos(num1 / 2));
                            point3d72 = MathHelper.distanceBearingPoint(point3d71, num5, 4 * self.RnpPrevious / math.sin(num4));
                            point3d73 = MathHelper.distanceBearingPoint(point3d65, self.track, (metres + self.RnpCurrent) * math.tan(num1 / 2));
                            point3d74 = MathHelper.distanceBearingPoint(point3d65, self.Inbound + 3.14159265358979, (metres + self.RnpCurrent) * math.tan(num1 / 2));
                            MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpPrevious);
                            point3d75 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 1.5707963267949, 2 * self.RnpPrevious);
                            point3d76 = MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                            point3d77 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 1.5707963267949, 2 * self.RnpCurrent);
                            point3d5 = MathHelper.getIntersectionPoint(point3d67, point3d68, point3d71, point3d72);
                            point3d78 = MathHelper.distanceBearingPoint(point3d74, self.Inbound - 1.5707963267949, metres + self.RnpCurrent);
                            point3d79 = MathHelper.distanceBearingPoint(point3d78, num5, metres + self.RnpCurrent);
                            if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
                                if (self.RnpPrevious >= self.RnpCurrent):
                                    point3d66 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 3.14159265358979, self.RnpPrevious);
                                    point3d68 = MathHelper.distanceBearingPoint(point3d66, self.Inbound + 1.5707963267949, 2 * self.RnpCurrent);
                                    self.PrimaryPts.method_3(point3d76, MathHelper.smethod_60(point3d76, point3d64, point3d77));
                                    polylineArea3 = self.PrimaryPts;
                                    point3dArray = [point3d77, point3d70, point3d68, point3d5]
                                    polylineArea3.method_7(point3dArray);
                                else:
                                    if (not MathHelper.smethod_115(point3d77, point3d70, point3d69)):
                                        self.PrimaryPts.method_3(point3d76, MathHelper.smethod_60(point3d76, point3d64, point3d77));
                                        polylineArea4 = self.PrimaryPts;
                                        point3dArray = [point3d77, point3d70]
                                        polylineArea4.method_7(point3dArray)
                                    else:
                                        lstPoint3D2 = []
                                        MathHelper.smethod_34(point3d69, point3d70, self.StartPoint, 2 * self.RnpCurrent, lstPoint3D2);
                                        point3d6 = lstPoint3D2[0]
                                        point3d7 = lstPoint3D2[1]
                                        self.PrimaryPts.method_3(point3d76, MathHelper.smethod_60(point3d76, point3d64, point3d7));
                                        self.PrimaryPts.method_1(point3d7);
                                    if (not MathHelper.smethod_115(point3d75, point3d72, point3d71)):
                                        polylineArea5 = self.PrimaryPts;
                                        point3dArray = [point3d72, point3d68, point3d5]
                                        polylineArea5.method_7(point3dArray)
                                    else:
                                        lstPoint3D2 = []
                                        MathHelper.smethod_34(point3d71, point3d72, self.StartPoint, 2 * self.RnpPrevious, lstPoint3D2)
                                        point3d8 = lstPoint3D2[0]
                                        point3d9 = lstPoint3D2[1]
                                        self.PrimaryPts.method_3(point3d9, MathHelper.smethod_59(MathHelper.getBearing(self.StartPoint, point3d9) + 1.5707963267949, point3d9, point3d75));
                                        polylineArea6 = self.PrimaryPts;
                                        point3dArray = [point3d75, point3d68, point3d5]
                                        polylineArea6.method_7(point3dArray)

                            elif (not MathHelper.smethod_115(point3d77, point3d70, point3d69)):
                                self.PrimaryPts.method_3(point3d76, MathHelper.smethod_60(point3d76, point3d64, point3d77));
                                polylineArea7 = self.PrimaryPts;
                                point3dArray = [point3d77, point3d70]
                                polylineArea7.method_7(point3dArray)
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d69, point3d70, self.StartPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d10 = lstPoint3D2[0]
                                point3d11 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d76, MathHelper.smethod_60(point3d76, point3d64, point3d11));
                                self.PrimaryPts.method_1(point3d11);
                            if (not MathHelper.smethod_115(point3d74, point3d70, point3d69)):
                                self.PrimaryPts.method_1(point3d69);
                                self.PrimaryPts.method_3(point3d74, MathHelper.smethod_60(point3d74, point3d79, point3d73));
                                self.PrimaryPts.method_1(point3d73);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d69, point3d70, point3d78, metres + self.RnpCurrent, lstPoint3D2)
                                point3d12 = lstPoint3D2[0]
                                point3d13 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d13, MathHelper.smethod_60(point3d13, point3d79, point3d73));
                                self.PrimaryPts.method_1(point3d73);

                            point3d80 = MathHelper.distanceBearingPoint(self.StartPoint, self.track, metres * math.tan(num1 / 2));
                            point3d81 = MathHelper.distanceBearingPoint(point3d80, self.track - 1.5707963267949, metres);
                            point3d82 = MathHelper.distanceBearingPoint(point3d81, num5, metres);
                            self.NominalPts.method_3(point3d82, MathHelper.smethod_57(TurnDirection.Left, point3d82, point3d80, point3d81));
                            self.NominalPts.method_1(point3d80);
                            point3d65 = MathHelper.distanceBearingPoint(self.StartPoint, num5 + 3.14159265358979, 2 * self.RnpPrevious / math.sin(num4));
                            point3d74 = MathHelper.distanceBearingPoint(point3d65, self.Inbound + 3.14159265358979, (metres + self.RnpPrevious) * math.tan(num1 / 2));
                            self.StartObj = Polyline()
                            self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), point3d74, 0, 0, 0)
                            self.StartObj.AddVertexAt(self.StartObj.Length, MathHelper.distanceBearingPoint(point3d74, self.Inbound + 1.5707963267949, 4 * self.RnpPrevious), 0, 0, 0)

                else:
                    self.LegType = RnpArCalculatedLegType.STRAIGHT;
                    point3d3 = MathHelper.smethod_75(rnpArLeg_0.Inbound, rnpArLeg_0.Previous, self.StartPoint);
                    self.Inbound = rnpArLeg_0.Inbound;
                    point3d83 = MathHelper.distanceBearingPoint(self.StartPoint, self.track + 3.14159265358979, self.RnpPrevious);
                    point3d84 = MathHelper.distanceBearingPoint(point3d83, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                    point3d85 = MathHelper.distanceBearingPoint(point3d83, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                    point3d86 = MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                    point3d87 = MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                    point3d88 = MathHelper.distanceBearingPoint(point3d84, MathHelper.getBearing(point3d84, point3d86), MathHelper.calcDistance(point3d84, point3d86) / 2);
                    point3d89 = MathHelper.distanceBearingPoint(point3d85, MathHelper.getBearing(point3d85, point3d87), MathHelper.calcDistance(point3d85, point3d87) / 2);
                    num6 = MathHelper.calcDistance(point3d3, self.StartPoint);
                    if (MathHelper.calcDistance(point3d3, point3d84) >= MathHelper.calcDistance(point3d3, point3d85)):
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d85, point3d84, point3d3, num6 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d4 = lstPoint3D2[0]
                            point3d85 = lstPoint3D2[1]
                            lstPoint3D2 = []
                            if MathHelper.smethod_34(point3d89, point3d88, point3d3, num6 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                                point3d4 = lstPoint3D2[0]
                                point3d89 = lstPoint3D2[1]
#                         else:
                            
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d85, point3d84, point3d3, num6 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d4 = lstPoint3D2[0]
                            point3d84 = lstPoint3D2[1]
                            lstPoint3D2 = []
                            if MathHelper.smethod_34(point3d89, point3d88, point3d3, num6 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                                point3d4 = lstPoint3D2[0]
                                point3d88 = lstPoint3D2[1]
                    else:
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d84, point3d85, point3d3, num6 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d4 = lstPoint3D2[0]
                            point3d84 = lstPoint3D2[1]
                            lstPoint3D2 = []
                            if MathHelper.smethod_34(point3d88, point3d89, point3d3, num6 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                                point3d4 = lstPoint3D2[0]
                                point3d88 = lstPoint3D2[1]
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d84, point3d85, point3d3, num6 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d4 = lstPoint3D2[0]
                            point3d85 = lstPoint3D2[1]
                            lstPoint3D2 = []
                            if MathHelper.smethod_34(point3d88, point3d89, point3d3, num6 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                                point3d4 = lstPoint3D2[0]
                                point3d89 = lstPoint3D2[1]

                    self.PrimaryPts.method_3(point3d87, MathHelper.smethod_60(point3d87, point3d89, point3d85));
                    self.PrimaryPts.method_1(point3d85);
                    self.PrimaryPts.method_3(point3d84, MathHelper.smethod_60(point3d84, point3d88, point3d86));
                    self.PrimaryPts.method_1(point3d86);
                    self.NominalPts.method_1(self.StartPoint);
                    self.StartObj = Polyline()
                    self.StartObj.append(PolylinePoint(point3d85))
                    self.StartObj.append(PolylinePoint(point3d84))

            else:
                self.LegType = RnpArCalculatedLegType.STRAIGHT;
                if (rnpArSegmentType_0 != RnpArSegmentType.Final):
                    if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
                        raise UserWarning, "Missing a starting point for self type of segment"
                    self.StartPoint = rnpArDataGroup_0.Smas;
                    self.track = MathHelper.getBearing(self.StartPoint, self.EndPoint);
                    self.Inbound = self.track;
                    num7 = Unit.ConvertNMToMeter(rnpArDataGroup_0.Legs_FA[0].Rnp);
                    if (num7 >= self.RnpCurrent):
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent));
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent));
                    else:
                        point3d90 = MathHelper.distanceBearingPoint(self.StartPoint, self.track, (2 * self.RnpCurrent - 2 * num7) / math.tan(Unit.ConvertDegToRad(15)));
                        if (MathHelper.calcDistance(self.StartPoint, point3d90) > MathHelper.calcDistance(self.StartPoint, self.EndPoint)):
                            raise UserWarning, "Insufficient distance to fit the 15° missed approach splay. Please make sure the first missed approach leg is long enough to accomodate the required splay."
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d90, self.track + 1.5707963267949, 2 * self.RnpCurrent));
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * num7));
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * num7));
                        self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d90, self.track - 1.5707963267949, 2 * self.RnpCurrent));

                    self.StartObj = Polyline()
                    self.StartObj.append(PolylinePoint(MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent)))
                    self.StartObj.append(PolylinePoint(MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent)))
                else:
                    self.StartPoint = rnpArDataGroup_0.LTP
                    self.track = MathHelper.getBearing(self.StartPoint, self.EndPoint);
                    self.Inbound = self.track;
                    self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent));
                    self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(self.StartPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent));

            if (rnpArLeg_2 == None):
                self.Outbound = self.track;
                point3d91 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                point3d92 = MathHelper.distanceBearingPoint(self.EndPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                self.PrimaryPts.method_1(point3d92);
                self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d92, self.track, self.RnpNext));
                self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d91, self.track, self.RnpNext));
                self.PrimaryPts.method_1(point3d91);
                self.NominalPts.method_1(self.EndPoint);
            elif (rnpArLeg_2.Type != RnpArLegType.RF):
                self.Outbound = MathHelper.getBearing(self.EndPoint, rnpArLeg_2.Position);
                lstTurn = []
                num8 = MathHelper.smethod_77(self.track, self.Outbound, AngleUnits.Radians, lstTurn)
                turnDirection1 = lstTurn[0]
                if (turnDirection1 == TurnDirection.Nothing or num8 < Unit.ConvertDegToRad(1)):
                    point3d93 = MathHelper.distanceBearingPoint(self.EndPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                    point3d94 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                    self.PrimaryPts.method_1(point3d93);
                    self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d93, self.track, self.RnpNext));
                    self.PrimaryPts.method_1(MathHelper.distanceBearingPoint(point3d94, self.track, self.RnpNext));
                    self.PrimaryPts.method_1(point3d94);
                    self.NominalPts.method_1(self.EndPoint);
                    self.EndObj = Polyline()
                    self.EndObj.Add(MathHelper.distanceBearingPoint(point3d93, self.track + 3.14159265358979, self.RnpNext))
                    self.EndObj.Add(MathHelper.distanceBearingPoint(point3d94, self.track + 3.14159265358979, self.RnpNext))
                else:
                    self.courseChangeEnd = Unit.smethod_1(num8);
                    naN1 = Speed.NaN()
                    altitude1 = Altitude.NaN()
                    wind1 = Speed.NaN()
                    if (rnpArSegmentType_0 != RnpArSegmentType.Missed):
                        naN1 = rnpArLeg_2.method_3(rnpArDataGroup_0);
                        altitude1 = rnpArLeg_1.Altitude;
                        wind1 = rnpArLeg_1.Wind;
                        num = rnpArLeg_1.Bank;
                    else:
                        naN1 = rnpArLeg_1.method_3(rnpArDataGroup_0);
                        altitude1 = rnpArLeg_2.Altitude;
                        wind1 = rnpArLeg_2.Wind;
                        num = rnpArLeg_2.Bank;
                    speed1 = Speed.smethod_0(naN1, rnpArDataGroup_0.ISA, altitude1) + wind1;
                    distance = Distance.smethod_0(speed1, num);
                    metres1 = distance.Metres;
                    math.tan(num8 / 2);
                    if (turnDirection1 != TurnDirection.Left):
                        num9 = (3.14159265358979 - num8) / 2;
                        num10 = MathHelper.smethod_4(self.track - num9);
                        point3d95 = MathHelper.distanceBearingPoint(self.EndPoint, num10, 2 * self.RnpCurrent);
                        MathHelper.distanceBearingPoint(self.EndPoint, num10, 2 * self.RnpNext);
                        point3d96 = MathHelper.distanceBearingPoint(self.EndPoint, num10 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num9));
                        point3d97 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound, self.RnpNext);
                        point3d98 = MathHelper.distanceBearingPoint(point3d97, self.Outbound + 1.5707963267949, 2 * self.RnpNext);
                        point3d99 = MathHelper.distanceBearingPoint(point3d97, self.Outbound - 1.5707963267949, 2 * self.RnpNext);
                        point3d100 = MathHelper.distanceBearingPoint(point3d96, self.Outbound, self.RnpNext / math.cos(num8 / 2));
                        point3d101 = MathHelper.distanceBearingPoint(point3d100, num10, 4 * self.RnpCurrent / math.sin(num9));
                        point3d97 = MathHelper.distanceBearingPoint(self.EndPoint, num10 + 3.14159265358979, 2 * self.RnpNext / math.sin(num9));
                        point3d102 = MathHelper.distanceBearingPoint(point3d97, self.Outbound, self.RnpNext / math.cos(num8 / 2));
                        point3d103 = MathHelper.distanceBearingPoint(point3d102, num10, 4 * self.RnpNext / math.sin(num9));
                        point3d104 = MathHelper.distanceBearingPoint(point3d96, self.track + 3.14159265358979, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        point3d105 = MathHelper.distanceBearingPoint(point3d96, self.Outbound, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        MathHelper.distanceBearingPoint(self.EndPoint, self.track - 1.5707963267949, 2 * self.RnpNext);
                        point3d106 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound - 1.5707963267949, 2 * self.RnpNext);
                        point3d107 = MathHelper.distanceBearingPoint(self.EndPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                        point3d108 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound - 1.5707963267949, 2 * self.RnpCurrent);
                        point3d34 = MathHelper.getIntersectionPoint(point3d98, point3d99, point3d102, point3d103);
                        point3d109 = MathHelper.distanceBearingPoint(point3d105, self.Outbound + 1.5707963267949, metres1 + self.RnpCurrent);
                        point3d110 = MathHelper.distanceBearingPoint(point3d109, num10, metres1 + self.RnpCurrent);
                        if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
                            if (not MathHelper.smethod_119(point3d108, point3d100, point3d101)):
                                self.PrimaryPts.method_3(point3d107, MathHelper.smethod_60(point3d107, point3d95, point3d108));
                                polylineArea8 = self.PrimaryPts;
                                point3dArray = [point3d108, point3d101]
                                polylineArea8.method_7(point3dArray)
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d100, point3d101, self.EndPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d35 = lstPoint3D2[0]
                                point3d36 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d107, MathHelper.smethod_60(point3d107, point3d95, point3d36));
                                self.PrimaryPts.method_1(point3d36);
                        elif (self.RnpNext >= self.RnpCurrent):
                            point3d97 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound, self.RnpNext);
                            point3d99 = MathHelper.distanceBearingPoint(point3d97, self.Outbound - 1.5707963267949, 2 * self.RnpCurrent);
                            self.PrimaryPts.method_3(point3d107, MathHelper.smethod_60(point3d107, point3d95, point3d108));
                            polylineArea9 = self.PrimaryPts;
                            point3dArray = [point3d108, point3d99, point3d34]
                            polylineArea9.method_7(point3dArray);
                        else:
                            if (not MathHelper.smethod_119(point3d108, point3d100, point3d101)):
                                self.PrimaryPts.method_3(point3d107, MathHelper.smethod_60(point3d107, point3d95, point3d108));
                                polylineArea10 = self.PrimaryPts;
                                point3dArray = [point3d108, point3d101]
                                polylineArea10.method_7(point3dArray);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d100, point3d101, self.EndPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d37 = lstPoint3D2[0]
                                point3d38 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d107, MathHelper.smethod_60(point3d107, point3d95, point3d38));
                                self.PrimaryPts.method_1(point3d38);
                            if (not MathHelper.smethod_119(point3d106, point3d102, point3d103)):
                                polylineArea11 = self.PrimaryPts;
                                point3dArray = [point3d103, point3d99, point3d34]
                                polylineArea11.method_7(point3dArray);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d102, point3d103, self.EndPoint, 2 * self.RnpNext, lstPoint3D2)
                                point3d39 = lstPoint3D2[0]
                                point3d40 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d40, MathHelper.smethod_59(MathHelper.getBearing(self.EndPoint, point3d40) + 1.5707963267949, point3d40, point3d106));
                                polylineArea12 = self.PrimaryPts;
                                point3dArray = [point3d106, point3d99, point3d34]
                                polylineArea12.method_7(point3dArray);

                        if (not MathHelper.smethod_119(point3d105, point3d100, point3d101)):
                            self.PrimaryPts.method_1(point3d100);
                            self.PrimaryPts.method_3(point3d105, MathHelper.smethod_60(point3d105, point3d110, point3d104));
                            self.PrimaryPts.method_1(point3d104);
                        else:
                            lstPoint3D2 = []
                            MathHelper.smethod_34(point3d100, point3d101, point3d109, metres1 + self.RnpCurrent, lstPoint3D2)
                            point3d41 = lstPoint3D2[0]
                            point3d42 = lstPoint3D2[1]
                            self.PrimaryPts.method_3(point3d42, MathHelper.smethod_60(point3d42, point3d110, point3d104));
                            self.PrimaryPts.method_1(point3d104);

                        point3d111 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 3.14159265358979, metres1 * math.tan(num8 / 2));
                        point3d112 = MathHelper.distanceBearingPoint(point3d111, self.track + 1.5707963267949, metres1);
                        point3d113 = MathHelper.distanceBearingPoint(point3d112, num10, metres1);
                        self.NominalPts.method_3(point3d111, MathHelper.smethod_59(self.track, point3d111, point3d113));
                        self.NominalPts.method_1(point3d113);
                        point3d96 = MathHelper.distanceBearingPoint(self.EndPoint, num10 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num9));
                        point3d104 = MathHelper.distanceBearingPoint(point3d96, self.track + 3.14159265358979, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        self.EndObj = Polyline()
                        self.EndObj.Add(point3d104)
                        self.EndObj.Add(MathHelper.distanceBearingPoint(point3d104, self.track - 1.5707963267949, 4 * self.RnpNext))
                    else:
                        num11 = (3.14159265358979 - num8) / 2;
                        num12 = MathHelper.smethod_4(self.track + num11);
                        point3d114 = MathHelper.distanceBearingPoint(self.EndPoint, num12, 2 * self.RnpCurrent);
                        MathHelper.distanceBearingPoint(self.EndPoint, num12, 2 * self.RnpNext);
                        point3d115 = MathHelper.distanceBearingPoint(self.EndPoint, num12 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num11));
                        point3d116 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound, self.RnpNext);
                        point3d117 = MathHelper.distanceBearingPoint(point3d116, self.Outbound - 1.5707963267949, 2 * self.RnpNext);
                        point3d118 = MathHelper.distanceBearingPoint(point3d116, self.Outbound + 1.5707963267949, 2 * self.RnpNext);
                        point3d119 = MathHelper.distanceBearingPoint(point3d115, self.Outbound, self.RnpNext / math.cos(num8 / 2));
                        point3d120 = MathHelper.distanceBearingPoint(point3d119, num12, 4 * self.RnpCurrent / math.sin(num11));
                        point3d116 = MathHelper.distanceBearingPoint(self.EndPoint, num12 + 3.14159265358979, 2 * self.RnpNext / math.sin(num11));
                        point3d121 = MathHelper.distanceBearingPoint(point3d116, self.Outbound, self.RnpNext / math.cos(num8 / 2));
                        point3d122 = MathHelper.distanceBearingPoint(point3d121, num12, 4 * self.RnpNext / math.sin(num11));
                        point3d123 = MathHelper.distanceBearingPoint(point3d115, self.track + 3.14159265358979, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        point3d124 = MathHelper.distanceBearingPoint(point3d115, self.Outbound, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        MathHelper.distanceBearingPoint(self.EndPoint, self.track + 1.5707963267949, 2 * self.RnpNext);
                        point3d125 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound + 1.5707963267949, 2 * self.RnpNext);
                        point3d126 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                        point3d127 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound + 1.5707963267949, 2 * self.RnpCurrent);
                        point3d25 = MathHelper.getIntersectionPoint(point3d117, point3d118, point3d121, point3d122);
                        point3d128 = MathHelper.distanceBearingPoint(point3d124, self.Outbound - 1.5707963267949, metres1 + self.RnpCurrent);
                        point3d129 = MathHelper.distanceBearingPoint(point3d128, num12, metres1 + self.RnpCurrent);
                        if (not MathHelper.smethod_119(point3d124, point3d120, point3d119)):
                            self.PrimaryPts.method_3(point3d123, MathHelper.smethod_60(point3d123, point3d129, point3d124));
                            polylineArea13 = self.PrimaryPts;
                            point3dArray = [point3d124, point3d119]
                            polylineArea13.method_7(point3dArray);
                        else:
                            lstPoint3D2 = []
                            MathHelper.smethod_34(point3d119, point3d120, point3d128, metres1 + self.RnpCurrent, lstPoint3D2)
                            point3d26 = lstPoint3D2[0]
                            point3d27 = lstPoint3D2[1]
                            self.PrimaryPts.method_3(point3d123, MathHelper.smethod_60(point3d123, point3d129, point3d27));
                            self.PrimaryPts.method_1(point3d27);
                        if (rnpArSegmentType_0 == RnpArSegmentType.Missed):
                            if (not MathHelper.smethod_119(point3d127, point3d120, point3d119)):
                                self.PrimaryPts.method_1(point3d120);
                                self.PrimaryPts.method_3(point3d127, MathHelper.smethod_60(point3d127, point3d114, point3d126));
                                self.PrimaryPts.method_1(point3d126);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d119, point3d120, self.EndPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d28 = lstPoint3D2[0]
                                point3d29 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d29, MathHelper.smethod_60(point3d29, point3d114, point3d126));
                                self.PrimaryPts.method_1(point3d126);

                        elif (self.RnpNext >= self.RnpCurrent):
                            point3d116 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound, self.RnpNext);
                            point3d118 = MathHelper.distanceBearingPoint(point3d116, self.Outbound + 1.5707963267949, 2 * self.RnpCurrent);
                            polylineArea14 = self.PrimaryPts;
                            point3dArray = [point3d25, point3d118]
                            polylineArea14.method_7(point3dArray);
                            self.PrimaryPts.method_3(point3d127, MathHelper.smethod_60(point3d127, point3d114, point3d126));
                            self.PrimaryPts.method_1(point3d126);
                        else:
                            polylineArea15 = self.PrimaryPts;
                            point3dArray = [point3d25, point3d118]
                            polylineArea15.method_7(point3dArray);
                            if (not MathHelper.smethod_119(point3d125, point3d122, point3d121)):
                                self.PrimaryPts.method_1(point3d122);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d121, point3d122, self.EndPoint, 2 * self.RnpNext, lstPoint3D2)
                                point3d30 = lstPoint3D2[0]
                                point3d31 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d125, MathHelper.smethod_59(MathHelper.getBearing(self.EndPoint, point3d125) + 1.5707963267949, point3d125, point3d31));
                                self.PrimaryPts.method_1(point3d31);
                            if (not MathHelper.smethod_119(point3d127, point3d120, point3d119)):
                                self.PrimaryPts.method_1(point3d120);
                                self.PrimaryPts.method_3(point3d127, MathHelper.smethod_60(point3d127, point3d114, point3d126));
                                self.PrimaryPts.method_1(point3d126);
                            else:
                                lstPoint3D2 = []
                                MathHelper.smethod_34(point3d119, point3d120, self.EndPoint, 2 * self.RnpCurrent, lstPoint3D2)
                                point3d32 = lstPoint3D2[0]
                                point3d33 = lstPoint3D2[1]
                                self.PrimaryPts.method_3(point3d33, MathHelper.smethod_60(point3d33, point3d114, point3d126));
                                self.PrimaryPts.method_1(point3d126);

                        point3d130 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 3.14159265358979, metres1 * math.tan(num8 / 2));
                        point3d131 = MathHelper.distanceBearingPoint(point3d130, self.track - 1.5707963267949, metres1);
                        point3d132 = MathHelper.distanceBearingPoint(point3d131, num12, metres1);
                        self.NominalPts.method_3(point3d130, MathHelper.smethod_59(self.track, point3d130, point3d132));
                        self.NominalPts.method_1(point3d132);
                        point3d115 = MathHelper.distanceBearingPoint(self.EndPoint, num12 + 3.14159265358979, 2 * self.RnpCurrent / math.sin(num11));
                        point3d123 = MathHelper.distanceBearingPoint(point3d115, self.track + 3.14159265358979, (metres1 + self.RnpCurrent) * math.tan(num8 / 2));
                        self.EndObj = Polyline()
                        self.EndObj.Add(point3d123)
                        self.EndObj.Add(MathHelper.distanceBearingPoint(point3d123, self.track + 1.5707963267949, 4 * self.RnpNext))

            else:
                point3d23 = MathHelper.smethod_75(rnpArLeg_2.Inbound, self.EndPoint, rnpArLeg_2.Position)
                self.Outbound = rnpArLeg_2.Inbound
                point3d133 = MathHelper.distanceBearingPoint(self.EndPoint, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                point3d134 = MathHelper.distanceBearingPoint(self.EndPoint, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                point3d135 = MathHelper.distanceBearingPoint(self.EndPoint, self.track, self.RnpNext);
                point3d136 = MathHelper.distanceBearingPoint(point3d135, self.track - 1.5707963267949, 2 * self.RnpCurrent);
                point3d137 = MathHelper.distanceBearingPoint(point3d135, self.track + 1.5707963267949, 2 * self.RnpCurrent);
                point3d138 = MathHelper.distanceBearingPoint(point3d136, MathHelper.getBearing(point3d136, point3d133), MathHelper.calcDistance(point3d136, point3d133) / 2);
                point3d139 = MathHelper.distanceBearingPoint(point3d137, MathHelper.getBearing(point3d137, point3d134), MathHelper.calcDistance(point3d137, point3d134) / 2);
                num13 = MathHelper.calcDistance(point3d23, self.EndPoint);
                if (MathHelper.calcDistance(point3d23, point3d136) >= MathHelper.calcDistance(point3d23, point3d137)):
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d137, point3d136, point3d23, num13 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d24 = lstPoint3D2[0]
                        point3d137 = lstPoint3D2[1]
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d139, point3d138, point3d23, num13 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d24 = lstPoint3D2[0]
                            point3d139 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d137, point3d136, point3d23, num13 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d24 = lstPoint3D2[0]
                        point3d136 = lstPoint3D2[1]
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d139, point3d138, point3d23, num13 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d24 = lstPoint3D2[0]
                            point3d138 = lstPoint3D2[1]
                else:
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d136, point3d137, point3d23, num13 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d24 = lstPoint3D2[0]
                        point3d136 = lstPoint3D2[1]
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d138, point3d139, point3d23, num13 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d24 = lstPoint3D2[0]
                            point3d138 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d136, point3d137, point3d23, num13 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d24 = lstPoint3D2[0]
                        point3d137 = lstPoint3D2[1]
                        lstPoint3D2 = []
                        if MathHelper.smethod_34(point3d138, point3d139, point3d23, num13 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                            point3d24 = lstPoint3D2[0]
                            point3d139 = lstPoint3D2[1]

                self.PrimaryPts.method_3(point3d133, MathHelper.smethod_60(point3d133, point3d138, point3d136));
                self.PrimaryPts.method_1(point3d136);
                self.PrimaryPts.method_3(point3d137, MathHelper.smethod_60(point3d137, point3d139, point3d134));
                self.PrimaryPts.method_1(point3d134);
                self.NominalPts.method_1(self.EndPoint);
                point3d140 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound + 3.14159265358979, self.RnpNext);
                point3d141 = MathHelper.distanceBearingPoint(point3d140, self.Outbound - 1.5707963267949, 2 * self.RnpNext);
                point3d142 = MathHelper.distanceBearingPoint(point3d140, self.Outbound + 1.5707963267949, 2 * self.RnpNext);
                self.EndObj = Polyline()
                self.EndObj.Add(point3d141)
                self.EndObj.Add(point3d142)

            if (self.StartObj != None and self.EndObj != None):
                num14 = MathHelper.calcDistance(self.StartObj.GetClosestPointTo(self.EndObj.GetPoint3dAt(0), False), self.EndObj.GetPoint3dAt(0));
                num15 = MathHelper.calcDistance(self.StartObj.GetClosestPointTo(self.EndObj.GetPoint3dAt(1), False), self.EndObj.GetPoint3dAt(1));
                self.SegmentLength = min([num14, num15])
            else:
                self.SegmentLength = MathHelper.calcDistance(self.StartPoint, self.EndPoint)

        else:
            self.LegType = RnpArCalculatedLegType.RF
            self.StartPoint = rnpArLeg_0.Position
            self.EndPoint = rnpArLeg_1.Position
            self.Inbound = self.method_1(rnpArLeg_0, rnpArLeg_1);
            self.Outbound = self.method_2(rnpArLeg_0, rnpArLeg_1);
            self.Radius = rnpArLeg_1.Radius;
            point3d143 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 3.14159265358979, self.RnpPrevious);
            point3d144 = MathHelper.distanceBearingPoint(point3d143, self.Inbound - 1.5707963267949, 2 * self.RnpCurrent);
            point3d145 = MathHelper.distanceBearingPoint(point3d143, self.Inbound + 1.5707963267949, 2 * self.RnpCurrent);
            point3d146 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound - 1.5707963267949, 2 * self.RnpCurrent);
            point3d147 = MathHelper.distanceBearingPoint(self.StartPoint, self.Inbound + 1.5707963267949, 2 * self.RnpCurrent);
            point3d148 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound - 1.5707963267949, 2 * self.RnpCurrent);
            point3d149 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound + 1.5707963267949, 2 * self.RnpCurrent);
            point3d150 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound, self.RnpNext);
            point3d151 = MathHelper.distanceBearingPoint(point3d150, self.Outbound - 1.5707963267949, 2 * self.RnpCurrent);
            point3d152 = MathHelper.distanceBearingPoint(point3d150, self.Outbound + 1.5707963267949, 2 * self.RnpCurrent);
            point3d = MathHelper.smethod_75(self.Inbound, self.StartPoint, self.EndPoint);
            point3d153 = MathHelper.distanceBearingPoint(self.EndPoint, self.Outbound + 3.14159265358979, self.RnpNext);
            point3d154 = MathHelper.distanceBearingPoint(point3d153, self.Outbound - 1.5707963267949, 2 * self.RnpNext);
            point3d155 = MathHelper.distanceBearingPoint(point3d153, self.Outbound + 1.5707963267949, 2 * self.RnpNext);
            num16 = 0;
            num17 = 0;
            num18 = 0;
            if (rnpArLeg_0 != None and rnpArLeg_0.Type == RnpArLegType.RF):
                point3d = MathHelper.smethod_75(rnpArLeg_0.Inbound, rnpArLeg_0.Previous, self.StartPoint);
                point3d156 = MathHelper.distanceBearingPoint(point3d144, MathHelper.getBearing(point3d144, point3d146), MathHelper.calcDistance(point3d144, point3d146) / 2);
                point3d157 = MathHelper.distanceBearingPoint(point3d143, MathHelper.getBearing(point3d143, self.StartPoint), MathHelper.calcDistance(point3d143, self.StartPoint) / 2);
                point3d158 = MathHelper.distanceBearingPoint(point3d145, MathHelper.getBearing(point3d145, point3d147), MathHelper.calcDistance(point3d145, point3d147) / 2);
                num19 = MathHelper.calcDistance(point3d, self.StartPoint);
                if (MathHelper.calcDistance(point3d, point3d144) >= MathHelper.calcDistance(point3d, point3d145)):
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d145, point3d144, point3d, num19 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d145 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d158, point3d156, point3d, num19 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d158 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d145, point3d144, point3d, num19 + 2 * self.RnpCurrent, lstPoint3D2) != "None":#out point3d1, out point3d144)
                        point3d1 = lstPoint3D2[0]
                        point3d144 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d158, point3d156, point3d, num19 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d156 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d145, point3d144, point3d, num19, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d143 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d158, point3d156, point3d, num19, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d157 = lstPoint3D2[1]
                else:
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d144, point3d145, point3d, num19 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d144 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d156, point3d158, point3d, num19 - 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d156 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d144, point3d145, point3d, num19 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d24 = lstPoint3D2[0]
                        point3d138 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d156, point3d158, point3d, num19 + 2 * self.RnpCurrent, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d158 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d144, point3d145, point3d, num19, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d143 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    if MathHelper.smethod_34(point3d156, point3d158, point3d, num19, lstPoint3D2) != "None":
                        point3d1 = lstPoint3D2[0]
                        point3d157 = lstPoint3D2[1]
                    
                num16 = MathHelper.smethod_60(point3d144, point3d156, point3d146);
                num17 = MathHelper.smethod_60(point3d147, point3d158, point3d145);
                num18 = MathHelper.smethod_60(point3d143, point3d157, self.StartPoint);

            num20 = 0;
            num21 = 0;
            num22 = 0;
            if (rnpArLeg_2 != None and rnpArLeg_2.Type == RnpArLegType.RF):
                point3d = MathHelper.smethod_75(rnpArLeg_2.Inbound, self.EndPoint, rnpArLeg_2.Position);
                point3d159 = MathHelper.distanceBearingPoint(point3d151, MathHelper.getBearing(point3d151, point3d148), MathHelper.calcDistance(point3d151, point3d148) / 2);
                point3d160 = MathHelper.distanceBearingPoint(point3d150, MathHelper.getBearing(point3d150, self.EndPoint), MathHelper.calcDistance(point3d150, self.EndPoint) / 2);
                point3d161 = MathHelper.distanceBearingPoint(point3d152, MathHelper.getBearing(point3d152, point3d149), MathHelper.calcDistance(point3d152, point3d149) / 2);
                num23 = MathHelper.calcDistance(point3d, self.EndPoint);
                if (MathHelper.calcDistance(point3d, point3d151) >= MathHelper.calcDistance(point3d, point3d152)):
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d152, point3d151, point3d, num23 - 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d152);
                    point3d2 = lstPoint3D2[0]
                    point3d152 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d161, point3d159, point3d, num23 - 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d161);
                    point3d2 = lstPoint3D2[0]
                    point3d161 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d152, point3d151, point3d, num23 + 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d151);
                    point3d2 = lstPoint3D2[0]
                    point3d151 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d161, point3d159, point3d, num23 + 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d159);
                    point3d2 = lstPoint3D2[0]
                    point3d159 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d152, point3d151, point3d, num23, lstPoint3D2)#out point3d2, out point3d150);
                    point3d2 = lstPoint3D2[0]
                    point3d150 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d161, point3d159, point3d, num23, lstPoint3D2)#out point3d2, out point3d160);
                    point3d2 = lstPoint3D2[0]
                    point3d160 = lstPoint3D2[1]
                else:
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d151, point3d152, point3d, num23 - 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d151);
                    point3d2 = lstPoint3D2[0]
                    point3d151 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d159, point3d161, point3d, num23 - 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d159);
                    point3d2 = lstPoint3D2[0]
                    point3d159 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d151, point3d152, point3d, num23 + 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d152);
                    point3d2 = lstPoint3D2[0]
                    point3d152 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d159, point3d161, point3d, num23 + 2 * self.RnpCurrent, lstPoint3D2)#out point3d2, out point3d161);
                    point3d2 = lstPoint3D2[0]
                    point3d161 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d151, point3d152, point3d, num23, lstPoint3D2)#out point3d2, out point3d150);
                    point3d2 = lstPoint3D2[0]
                    point3d150 = lstPoint3D2[1]
                    lstPoint3D2 = []
                    MathHelper.smethod_34(point3d159, point3d161, point3d, num23, lstPoint3D2)#out point3d2, out point3d160);
                    point3d2 = lstPoint3D2[0]
                    point3d160 = lstPoint3D2[1]

                num20 = MathHelper.smethod_60(point3d148, point3d159, point3d151);
                num21 = MathHelper.smethod_60(point3d152, point3d161, point3d149);
                num22 = MathHelper.smethod_60(self.EndPoint, point3d160, point3d150);

            self.PrimaryPts = PolylineArea()
            self.PrimaryPts.method_3(point3d144, num16);
            self.PrimaryPts.method_3(point3d146, MathHelper.smethod_59(self.Inbound, point3d146, point3d148));
            self.PrimaryPts.method_3(point3d148, num20);
            self.PrimaryPts.method_1(point3d151);
            self.PrimaryPts.method_3(point3d152, num21);
            self.PrimaryPts.method_3(point3d149, MathHelper.smethod_59(self.Outbound + 3.14159265358979, point3d149, point3d147));
            self.PrimaryPts.method_3(point3d147, num17);
            self.PrimaryPts.method_1(point3d145);
            self.NominalPts = PolylineArea();
            self.NominalPts.method_3(self.StartPoint, MathHelper.smethod_59(self.Inbound, self.StartPoint, self.EndPoint));
            self.NominalPts.method_1(self.EndPoint);
            self.StartObj = Polyline();
            self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), point3d145, 0, 0, 0);
            self.StartObj.AddVertexAt(self.StartObj.get_NumberOfVertices(), point3d144, 0, 0, 0);
            self.EndObj = Polyline();
            self.EndObj.AddVertexAt(self.EndObj.get_NumberOfVertices(), point3d154, 0, 0, 0);
            self.EndObj.AddVertexAt(self.EndObj.get_NumberOfVertices(), point3d155, 0, 0, 0);
            self.MeasureObj = Polyline();
            self.MeasureObj.AddVertexAt(self.MeasureObj.get_NumberOfVertices(), point3d143, num18, 0, 0);
            self.MeasureObj.AddVertexAt(self.MeasureObj.get_NumberOfVertices(), self.StartPoint, MathHelper.smethod_59(self.Inbound, self.StartPoint, self.EndPoint), 0, 0);
            self.MeasureObj.AddVertexAt(self.MeasureObj.get_NumberOfVertices(), self.EndPoint, num22, 0, 0);
            self.MeasureObj.AddVertexAt(self.MeasureObj.get_NumberOfVertices(), point3d150, 0, 0, 0);
            point3dCollection = []
            self.MeasureObj.IntersectWith(self.EndObj, 0, point3dCollection);
            self.SegmentLength = self.method_3(point3dCollection[0]);

        self.PrimaryPts.method_16();
        self.PrimaryArea = PrimaryObstacleArea(self.PrimaryPts);
        
    def method_0(self, point3d_0):# double double_0)
        if (self.LegType == RnpArCalculatedLegType.RF):
            double_0 = 0;
            return max([self.method_3(self.MeasureObj.GetClosestPointTo(point3d_0, False)), 0]), double_0

        num = MathHelper.calcDistance(self.StartObj.GetClosestPointTo(point3d_0, False), point3d_0)
        if (MathHelper.smethod_99(self.courseChangeStart, 0, 0.1) and num > self.SegmentLength and self.EndObj != None):
            num = self.SegmentLength + MathHelper.calcDistance(self.EndObj.GetClosestPointTo(point3d_0, False), point3d_0);
        if (max([self.courseChangeStart, self.courseChangeEnd]) > 15):
            double_0 = self.moc50;
        elif (max([self.courseChangeStart, self.courseChangeEnd]) <= 0.1):
            double_0 = 0;
        else:
            double_0 = self.moc30;
        return num, double_0

    def method_1(self, rnpArLeg_0, rnpArLeg_1):
        return rnpArLeg_1.Inbound;

    def method_2(self, rnpArLeg_0, rnpArLeg_1):
        point3d1 = rnpArLeg_0.Position
        point3d2 = rnpArLeg_1.Position
        point3d = MathHelper.smethod_75(rnpArLeg_1.Inbound, point3d1, point3d2)
        if (MathHelper.smethod_66(MathHelper.smethod_59(rnpArLeg_1.Inbound, point3d1, point3d2)) == TurnDirection.Left):
            return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) - 1.5707963267949)
        return MathHelper.smethod_4(MathHelper.getBearing(point3d, point3d2) + 1.5707963267949)

    def method_3(self, point3d_0):
        metres = 0;
        distAtPoint = self.MeasureObj.GetDistAtPoint(point3d_0)#.smethod_167(self.MeasureObj.get_Elevation()));
        num = 1;
        while (True):
            if (num < self.MeasureObj.get_NumberOfVertices()):
                point3dAt = self.MeasureObj.GetPoint3dAt(num - 1);
                point3dAt1 = self.MeasureObj.GetPoint3dAt(num);
                distAtPoint1 = self.MeasureObj.GetDistAtPoint(point3dAt);
                num1 = self.MeasureObj.GetDistAtPoint(point3dAt1);
                if (distAtPoint <= num1):
                    bulgeAt = self.MeasureObj.GetBulgeAt(num - 1);
                    if (bulgeAt != 0):
                        point3d = MathHelper.smethod_71(point3dAt, point3dAt1, bulgeAt);
                        turnDirection = MathHelper.smethod_66(bulgeAt)
                        num2 = MathHelper.getBearing(point3d, point3dAt) if turnDirection == TurnDirection.Right else MathHelper.getBearing(point3d, point3d_0)
                        num3 = MathHelper.smethod_53(num2, MathHelper.getBearing(point3d, point3d_0) if turnDirection == TurnDirection.Right else MathHelper.getBearing(point3d, point3dAt))
                        metres = metres + (self.Radius.Metres - self.RnpCurrent) * num3
                        break;
                    else:
                        metres = metres + (distAtPoint - distAtPoint1);
                        break;
                else:
                    bulgeAt1 = self.MeasureObj.GetBulgeAt(num - 1);
                    if (bulgeAt1 != 0):
                        num4 = 4 * math.atan(bulgeAt1);
                        metres = metres + (self.Radius.Metres - self.RnpCurrent) * num4;
                    else:
                        metres = metres + (num1 - distAtPoint1);
                    num += 1
            else:
                break;
        return metres;

class RnpArCalculatedSegment(list) : #List<RnpAR.RnpArCalculatedLeg>

    def __init__(self):
        list.__init__(self)
        self.Type = RnpArSegmentType.Intermediate

    def get_count(self):
        return len(self)

    def del_count(self):
        del self.__Count


    def Construct(self, layer):
        pass

    def method_0(self):
        pass
    
    def Add(self, el):
        self.append(el)
        
    Count = property(get_count, None, del_count, "self is count of elements.")
#         for rnpArCalculatedLeg in self:
#             rnpArCalculatedLeg.Dispose();

class RnpArCalculatedSegments(list) : #List<RnpAR.RnpArCalculatedSegment>

    def __init__(self):
        list.__init__(self)
        
    def get_Count(self):
        return len(self)
    Count = property(get_Count, None, None, None)
    
    def method_0(self):
        pass
#         foreach (RnpAR.RnpArCalculatedSegment rnpArCalculatedSegment in self)
#         {
#             rnpArCalculatedSegment.method_0();
#         }

    def method_1(self, string_0, layersList):
        for rnpArCalculatedSegment in self:
            rnpArCalculatedSegment.Construct(string_0, layersList)

    def method_2(self, string_0, point3d_0, layersList):
        polylineArea = PolylineArea([point3d_0])
        polylineArea1 = PolylineArea([point3d_0])
        for rnpArCalculatedSegment in self:
            if (not isinstance(rnpArCalculatedSegment, RnpArMissedApproachSegment)):
                for rnpArCalculatedLeg in rnpArCalculatedSegment:
                    if (rnpArCalculatedLeg.NominalPts == None):
                        continue;
                    for nominalPt in rnpArCalculatedLeg.NominalPts:
                        polylineArea.Add(nominalPt)
            
            else:
                for rnpArCalculatedLeg1 in rnpArCalculatedSegment:
                    if (rnpArCalculatedLeg1.NominalPts == None):
                        continue;
                    for polylineAreaPoint in rnpArCalculatedLeg1.NominalPts:
                        polylineArea1.Add(polylineAreaPoint);

        polylineArea.method_16();
        polylineArea1.method_16();
        layerName = "Nominal Track"
        resultLayer = AcadHelper.createVectorLayer(layerName)
        if (polylineArea1.Count > 1):
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, polylineArea1)
        if (polylineArea.Count > 1):
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, polylineArea)
        layersList.append(resultLayer)
        
        WPTLayerName = string_0 + "_WPT"
        lstWPT = []
        for rnpArCalculatedSegment1 in self:
            if not isinstance(rnpArCalculatedSegment1, RnpArFinalApproachSegment):
                for rnpArCalculatedLeg2 in rnpArCalculatedSegment1:
                    lstWPT.append((rnpArCalculatedLeg2.EndPoint, "FlyBy"))
            else:
                for i in range(rnpArCalculatedSegment1.Count):
                    item = rnpArCalculatedSegment1[i]
                    if (i == rnpArCalculatedSegment1.Count - 1):
                        lstWPT.append((item.EndPoint, Captions.FAP))
                    else:
                        lstWPT.append((item.EndPoint, "FlyBy"))
        wptLayer = AcadHelper.createWPTPointLayer(WPTLayerName, lstWPT)
        layersList.append(wptLayer)

    def method_3(self, point3d_0):
        polylineArea = PolylineArea([point3d_0])
        #List<RnpAR.RnpArCalculatedSegment>.Enumerator enumerator = self.GetEnumerator();
        for current in self:
            if isinstance(current, RnpArFinalApproachSegment):
                for rnpArCalculatedLeg in current:
                    if (rnpArCalculatedLeg.NominalPts == None):
                        continue;
                    for nominalPt in rnpArCalculatedLeg.NominalPts:
                        polylineArea.Add(nominalPt);
            elif isinstance(current, RnpArIntermediateApproachSegment):
                for current1 in current[0].NominalPts:
                    polylineArea.Add(current1)
                break
        return self.asPolyline(polylineArea)
    def asPolyline(self, polylineArea):
        polyline = Polyline()
        if (not polylineArea.isCircle):
            for item in polylineArea:
                position = item.Position;
                polyline.AddVertexAt(polyline.Length, position, item.Bulge, 0, 0)
        else:
            point3d = MathHelper.distanceBearingPoint(polylineArea.CenterPoint, 0, polylineArea.Radius);
            point3d1 = MathHelper.distanceBearingPoint(polylineArea.CenterPoint, 1.5707963267949, polylineArea.Radius);
            point3d2 = MathHelper.distanceBearingPoint(polylineArea.CenterPoint, 3.14159265358979, polylineArea.Radius);
            point3d3 = MathHelper.distanceBearingPoint(polylineArea.CenterPoint, 4.71238898038469, polylineArea.Radius);
            polyline.AddVertexAt(0, point3d, MathHelper.smethod_60(point3d, point3d1, point3d2), 0, 0);
            polyline.AddVertexAt(1, point3d2, MathHelper.smethod_60(point3d2, point3d3, point3d), 0, 0);
            polyline.AddVertexAt(2, point3d, 0, 0, 0);
        return polyline;

class RnpArFinalApproachSegment(RnpArCalculatedSegment):
#     private RnpArVebComponents veb;
# 
#     private RnpArTemperatureComponents tc;
# 
#     private Distance dFrop150;
# 
#     private Distance dFrop15s;
# 
#     private Distance dFrop50s;

    def __init__(self, rnpArDataGroup_0):
        RnpArCalculatedSegment.__init__(self)
        self.Type = RnpArSegmentType.Final
        count = rnpArDataGroup_0.Legs_FA.Count - 1
        for i in range(rnpArDataGroup_0.Legs_FA.Count):
            if (i == 0):
                item = None;
            else:
                item = rnpArDataGroup_0.Legs_FA[i - 1];
            rnpArLeg1 = item;
            if (i == count):
                rnpArLeg = None;
            else:
                rnpArLeg = rnpArDataGroup_0.Legs_FA[i + 1];
            rnpArLeg2 = rnpArLeg;
            if (rnpArLeg2 == None):
                if (rnpArDataGroup_0.Legs_I.Count > 0):
                    item1 = rnpArDataGroup_0.Legs_I[0];
                else:
                    item1 = None;
                rnpArLeg2 = item1;
            self.append(RnpArCalculatedLeg(rnpArDataGroup_0, RnpArSegmentType.Final, rnpArLeg1, rnpArDataGroup_0.Legs_FA[i], rnpArLeg2))

        self.tc = rnpArDataGroup_0.TemperatureComponents;
        self.veb = RnpArVebComponents(self.tc.ISA_low, rnpArDataGroup_0.MaxFinalRnp, rnpArDataGroup_0.MaxFinalBankRF, rnpArDataGroup_0.VPA, rnpArDataGroup_0.FAP, Altitude(rnpArDataGroup_0.LTP.z()), rnpArDataGroup_0.RDH);
        self.dFrop150 = rnpArDataGroup_0.Frop150;
        self.dFrop15s = rnpArDataGroup_0.Frop15s;
        self.dFrop50s = rnpArDataGroup_0.Frop50s;

    def Construct(self, layerName, layersList):
        resultLayer = AcadHelper.createVectorLayer(RnpArSegmentType.Final)
        linesList = []
        for rnpArCalculatedLeg in self:
            if (rnpArCalculatedLeg.PrimaryPts == None):
                continue;
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, rnpArCalculatedLeg.PrimaryPts, True)
            linesList.append((rnpArCalculatedLeg.PrimaryPts.method_14_closed(), []))
        
        startPoint = self[0].StartPoint
        num = MathHelper.getBearing(self[0].StartPoint, self[0].EndPoint)



        if self[len(self) - 1].LegType != RnpArLegType.RF:
            oASoriginTF = self.veb.OASorigin_TF
            oASoriginTFPoint = MathHelper.distanceBearingPoint(startPoint, num, oASoriginTF.Metres)
            oASoriginTFLine = [MathHelper.distanceBearingPoint(oASoriginTFPoint, num - math.pi / 2.0, 50),
                               MathHelper.distanceBearingPoint(oASoriginTFPoint, num + math.pi / 2.0, 50)]
            oASoriginTFAttr = [("Caption", "OAS ORIGIN (TF)")]
            linesList.append((oASoriginTFLine, oASoriginTFAttr))
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, oASoriginTFLine, False, {"Caption": "OAS ORIGIN (TF)"})
        else:
            oASoriginRF = self.veb.OASorigin_RF;
            oASoriginRFPoint = MathHelper.distanceBearingPoint(startPoint, num, oASoriginRF.Metres)
            oASoriginRFLine = [MathHelper.distanceBearingPoint(oASoriginRFPoint, num - math.pi / 2.0, 50),
                               MathHelper.distanceBearingPoint(oASoriginRFPoint, num + math.pi / 2.0, 50)]
            oASoriginRFAttr = [("Caption", "OAS ORIGIN (RF)")]
            linesList.append((oASoriginRFLine, oASoriginRFAttr))
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, oASoriginRFLine, False, {"Caption": "OAS ORIGIN (RF)"})
        if (self.dFrop150.IsValid()):
            dFrop150Point = MathHelper.distanceBearingPoint(startPoint, num, self.dFrop150.Metres)
            dFrop150Line = [MathHelper.distanceBearingPoint(dFrop150Point, num - math.pi / 2.0, 50),
                               MathHelper.distanceBearingPoint(dFrop150Point, num + math.pi / 2.0, 50)]
            dFrop150Attr = [("Caption", "FROP 150 m")]
            linesList.append((dFrop150Line, dFrop150Attr))
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, dFrop150Line, False, {"Caption": "FROP 150 m"})
        if (self.dFrop15s.IsValid()):
            dFrop15sPoint = MathHelper.distanceBearingPoint(startPoint, num, self.dFrop15s.Metres)
            dFrop15sLine = [MathHelper.distanceBearingPoint(dFrop15sPoint, num - math.pi / 2.0, 50),
                               MathHelper.distanceBearingPoint(dFrop15sPoint, num + math.pi / 2.0, 50)]
            dFrop15sAttr = [("Caption", "FROP OCH (15 s)")]
            linesList.append((dFrop15sLine, dFrop15sAttr))
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, dFrop15sLine, False, {"Caption": "FROP OCH (15 s)"})
        if (self.dFrop50s.IsValid()):
            dFrop50sPoint = MathHelper.distanceBearingPoint(startPoint, num, self.dFrop50s.Metres)
            dFrop50sLine = [MathHelper.distanceBearingPoint(dFrop50sPoint, num - math.pi / 2.0, 50),
                               MathHelper.distanceBearingPoint(dFrop50sPoint, num + math.pi / 2.0, 50)]
            dFrop50sAttr = [("Caption", "FROP OCH (50 s)")]
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, dFrop50sLine, False, {"Caption": "FROP OCH (50 s)"})
            linesList.append((dFrop50sLine, dFrop50sAttr))
        # resultLayer = QgisHelper.createPolylineLayer(RnpArSegmentType.Final, linesList, [QgsField("Caption", QVariant.String)])
        QgisHelper.setLabelSettingToPolyline(resultLayer, "Caption")
        layersList.append(resultLayer)

    def method_1(self, rnpArDataGroup_0, int_0):
        fAP = None
        polyline = Polyline()
        point3d = rnpArDataGroup_0.LTP
        polyline.AddVertexAt(0, point3d, 0, 0, 0);
        try:
            # re = 6367435.67964 # radius of the Earth (Metre)
            # metres = re * math.log1p((re + fAP.Altitude.Metres)/(re + fAP.Previous.get_Z() + rnpArDataGroup_0.RDH.Metres) - 1)/ rnpArDataGroup_0.VPA.Percent
            metres = rnpArDataGroup_0.FAPtoLTP.Metres
            num = 0
            while (num < self.Count):
                if (self[num].LegType != RnpArCalculatedLegType.TF):
                    if (self[num].LegType != RnpArCalculatedLegType.RF):
                        polyline.AddVertexAt(polyline.get_NumberOfVertices(), self[num].StartPoint, 0, 0, 0);
                        polyline.AddVertexAt(polyline.get_NumberOfVertices(), self[num].EndPoint, 0, 0, 0);
                    else:
                        for nominalPt in self[num].NominalPts:
                            polyline.AddVertexAt(polyline.get_NumberOfVertices(), nominalPt.Position, nominalPt.Bulge, 0, 0);
                    if (round(polyline.get_Length(), 4) >= round(metres, 4)):
                        int_0 = num;
                        if self[num].LegType != RnpArCalculatedLegType.RF :
                            fAP = RnpArLeg(RnpArLegType.TF)
                            fAP.Bank = 18
                        else:
                            fAP = RnpArLeg(RnpArLegType.RF)
                            fAP.Radius = self[num].Radius

                        fAP.Altitude = rnpArDataGroup_0.FAP;
                        fAP.Inbound = self[num].Inbound;
                        fAP.IsFAP = True;
                        fAP.Previous = Point3D(point3d.x(), point3d.y());
                        # re = 6367435.67964 # radius of the Earth (Metre)
                        # metres = re * math.log((re + fAP.Altitude.Metres)/(re + fAP.Previous.get_Z() + rnpArDataGroup_0.RDH.Metres))/ (rnpArDataGroup_0.VPA.Percent / 100)

                        pointAtDist = polyline.GetPointAtDist(metres);
                        if pointAtDist == None:
                            pointAtDist = polyline[len(polyline) - 1].point3d
                        fAP.Position = Point3D(pointAtDist.x(), pointAtDist.y(), fAP.Altitude.Metres);
                        fAP.Rnp = round(Unit.ConvertMeterToNM(self[num].RnpCurrent), 3);
                        fAP.Segment = RnpArSegmentType.Final;
                        rnpArLeg = fAP;
                        return rnpArLeg, int_0
                    else:
                        point3d = polyline.GetPoint3dAt(polyline.get_NumberOfVertices() - 1);
                        num += 1
                else:
                    int_0 = num;
                    fAP = RnpArLeg(RnpArLegType.TF)
                    fAP.Altitude = rnpArDataGroup_0.FAP
                    fAP.Bank = 18
                    fAP.Inbound = self[num].Inbound
                    fAP.IsFAP = True
                    fAP.Previous = Point3D(point3d.x(), point3d.y())
                    # re = 6367435.67964 # radius of the Earth (Metre)
                    # d = re * math.log1p((re + fAP.Altitude.Metres)/(re + fAP.Previous.get_Z() + rnpArDataGroup_0.RDH.Metres) - 1)/ (rnpArDataGroup_0.VPA.Percent / 100)
                    point3d1 = MathHelper.distanceBearingPoint(point3d, self[0].Inbound, metres - polyline.get_Length());
                    fAP.Position = Point3D(point3d1.x(), point3d1.y(), fAP.Altitude.Metres);
                    fAP.Rnp = round(Unit.ConvertMeterToNM(self[num].RnpPrevious), 1);
                    fAP.Segment = RnpArSegmentType.Final;
                    rnpArLeg = fAP;
                    return rnpArLeg, int_0

            if (polyline.get_Length() >= metres):
                item = rnpArDataGroup_0.Legs_FA[rnpArDataGroup_0.Legs_FA.Count - 1]
                int_0 = rnpArDataGroup_0.Legs_FA.Count - 1
                fAP = RnpArLeg(item.Type)
                fAP.Altitude = rnpArDataGroup_0.FAP
                fAP.Bank = item.Bank
                fAP.Inbound = item.Inbound
                fAP.IsFAP = True
                fAP.Previous = item.Previous
                fAP.Position = Point3D(item.Position.x(), item.Position.y(), fAP.Altitude.Metres)
                fAP.Rnp = item.Rnp
                fAP.Segment = RnpArSegmentType.Final
            else:
                fAP = RnpArLeg(RnpArLegType.TF)
                fAP.Altitude = rnpArDataGroup_0.FAP
                fAP.Bank = 18
                fAP.Inbound = self[self.Count - 1].Outbound
                fAP.IsFAP = True
                fAP.Previous = Point3D(point3d.x(), point3d.y())
                re = 6367435.67964 # radius of the Earth (Metre)
                # m = math.log1p(1)
                # d = re * math.log1p((re + fAP.Altitude.Metres)/(re + rnpArDataGroup_0.LTP.get_Z() + rnpArDataGroup_0.RDH.Metres) - 1)/ (rnpArDataGroup_0.VPA.Percent/100)

                point3d2 = MathHelper.distanceBearingPoint(point3d, fAP.Inbound, metres - polyline.get_Length());
                fAP.Position = Point3D(point3d2.x(), point3d2.y(), fAP.Altitude.Metres);
                fAP.Rnp = round(Unit.ConvertMeterToNM(self[self.Count - 1].RnpNext), 3);
                fAP.Segment = RnpArSegmentType.Final;
            rnpArLeg = fAP;
        finally:
            pass
            #AcadHelper.smethod_24(polyline);
        return rnpArLeg, int_0

class RnpArInitialApproachSegment(RnpArCalculatedSegment):
    def __init__(self, rnpArDataGroup_0):
        RnpArCalculatedSegment.__init__(self)
        self.Type = RnpArSegmentType.Initial
        count = rnpArDataGroup_0.Legs_IA.Count - 1
        for i in range(rnpArDataGroup_0.Legs_IA.Count):
            if (i == 0):
                item = None
            else:
                item = rnpArDataGroup_0.Legs_IA[i - 1]
            item1 = item if item != None else rnpArDataGroup_0.Legs_I[rnpArDataGroup_0.Legs_I.Count - 1]
            if (i == count):
                rnpArLeg = None
            else:
                rnpArLeg = rnpArDataGroup_0.Legs_IA[i + 1]
            rnpArLeg1 = rnpArLeg
            self.Add(RnpArCalculatedLeg(rnpArDataGroup_0, RnpArSegmentType.Initial, item1, rnpArDataGroup_0.Legs_IA[i], rnpArLeg1))

    def Construct(self, layerName, layersList):
        resultLayer = AcadHelper.createVectorLayer(RnpArSegmentType.Initial)
        for rnpArCalculatedLeg in self:
            if (rnpArCalculatedLeg.PrimaryPts == None):
                continue;
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, rnpArCalculatedLeg.PrimaryPts, True)
        layersList.append(resultLayer)

class RnpArIntermediateApproachSegment(RnpArCalculatedSegment):

    def __init__(self, rnpArDataGroup_0):
        RnpArCalculatedSegment.__init__(self)
        self.Type = RnpArSegmentType.Intermediate
        count = rnpArDataGroup_0.Legs_I.Count - 1;
        for i in range(rnpArDataGroup_0.Legs_I.Count):
            if (i == 0):
                item = None;
            else:
                item = rnpArDataGroup_0.Legs_I[i - 1];
            rnpArLeg1 = item if item != None else rnpArDataGroup_0.Legs_FA[rnpArDataGroup_0.Legs_FA.Count - 1]
            
            if (i == count):
                rnpArLeg = None;
            else:
                rnpArLeg = rnpArDataGroup_0.Legs_I[i + 1];

            rnpArLeg2 = rnpArLeg;
            if (rnpArLeg2 == None):
                if (rnpArDataGroup_0.Legs_IA.Count > 0):
                    item1 = rnpArDataGroup_0.Legs_IA[0];
                else:
                    item1 = None;
                rnpArLeg2 = item1;

            self.Add(RnpArCalculatedLeg(rnpArDataGroup_0, RnpArSegmentType.Intermediate, rnpArLeg1, rnpArDataGroup_0.Legs_I[i], rnpArLeg2))

    def Construct(self, layerName, layersList):
        resultLayer = AcadHelper.createVectorLayer(RnpArSegmentType.Intermediate)
        for rnpArCalculatedLeg in self:
            if (rnpArCalculatedLeg.PrimaryPts == None):
                continue;
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, rnpArCalculatedLeg.PrimaryPts, True)

        layersList.append(resultLayer)

class RnpArMissedApproachSegment(RnpArCalculatedSegment):

    def __init__(self, rnpArDataGroup_0):
        RnpArCalculatedSegment.__init__(self)
        self.Type = RnpArSegmentType.Missed
        count = rnpArDataGroup_0.Legs_MA.Count - 1;
        for i in range(rnpArDataGroup_0.Legs_MA.Count):
            if (i == 0):
                item = None;
            else:
                item = rnpArDataGroup_0.Legs_MA[i - 1];
            rnpArLeg1 = item;
            if (i == count):
                rnpArLeg = None;
            else:
                rnpArLeg = rnpArDataGroup_0.Legs_MA[i + 1];
            rnpArLeg2 = rnpArLeg
            self.Add(RnpArCalculatedLeg(rnpArDataGroup_0, RnpArSegmentType.Missed, rnpArLeg1, rnpArDataGroup_0.Legs_MA[i], rnpArLeg2));

        self.soc = rnpArDataGroup_0.SOC;
        self.socAlt = rnpArDataGroup_0.SOCaltitude;
        self.ltp = rnpArDataGroup_0.LTP;
        self.Outbound = MathHelper.getBearing(self[0].EndPoint, self[0].StartPoint);
        self.Xz = rnpArDataGroup_0.Xz.Metres
        self.Xmas = rnpArDataGroup_0.Xmas.Metres

    def Construct(self, layerName, layersList):
        resultLayer = AcadHelper.createVectorLayer(RnpArSegmentType.Missed)
        linesList = []
        for rnpArCalculatedLeg in self:
            if (rnpArCalculatedLeg.PrimaryPts == None):
                continue;
            AcadHelper.setGeometryAndAttributesInLayer(resultLayer, rnpArCalculatedLeg.PrimaryPts, True)

            linesList.append((rnpArCalculatedLeg.PrimaryPts.method_14_closed(), []))
        
        socLine = [MathHelper.distanceBearingPoint(self.soc, self.Outbound + math.pi / 2.0, 50),
                   MathHelper.distanceBearingPoint(self.soc, self.Outbound - math.pi / 2.0, 50)]
        socAttr = [("Caption", "SOC, ALTITUDE = " + str(round(self.socAlt.Metres)))]
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, socLine, False, {"Caption":"SOC, ALTITUDE = " + str(round(self.socAlt.Metres))})
        linesList.append((socLine, socAttr))

        zsufPoint = MathHelper.distanceBearingPoint(self.ltp, self.Outbound, self.Xz)
        zsufLine = [MathHelper.distanceBearingPoint(zsufPoint, self.Outbound + math.pi / 2.0, 50),
                   MathHelper.distanceBearingPoint(zsufPoint, self.Outbound - math.pi / 2.0, 50)]
        zsufAttr = [("Caption", "X (Z SURFACE)")]
        linesList.append((zsufLine, zsufAttr))
        AcadHelper.setGeometryAndAttributesInLayer(resultLayer, zsufLine, False, {"Caption":"X (Z SURFACE)"})

        
        # resultLayer = QgisHelper.createPolylineLayer(RnpArSegmentType.Missed, linesList, [QgsField("Caption", QVariant.String)])
        QgisHelper.setLabelSettingToPolyline(resultLayer, "Caption")
        layersList.append(resultLayer)
        
class RnpArVebComponents:

    def __init__(self, double_0, double_1, double_2, angleGradientSlope_0, altitude_0, altitude_1, altitude_2):
        self.vpa = angleGradientSlope_0
        self.ltp = altitude_1
        self.rdh = altitude_2
        self.__fte = 23
        self.__atis = 6
        self.__anpe = 1.225 * Unit.ConvertNMToMeter(double_1) * math.tan(angleGradientSlope_0.Radians);
        self.__wpr = 18 * math.tan(angleGradientSlope_0.Radians);
        self.__ase75 = -2.887E-07 * math.pow(altitude_1.Metres + 75, 2) + 0.0065 * (altitude_1.Metres + 75) + 15;
        self.__aseFAP = -2.887E-07 * math.pow(altitude_0.Metres, 2) + 0.0065 * altitude_0.Metres + 15;
        self.__vae75 = 75 / math.tan(angleGradientSlope_0.Radians) * (math.tan(angleGradientSlope_0.Radians) - math.tan(Unit.ConvertDegToRad(angleGradientSlope_0.Degrees - 0.01)));
        self.__vaeFAP = (altitude_0.Metres - altitude_1.Metres) / math.tan(angleGradientSlope_0.Radians) * (math.tan(angleGradientSlope_0.Radians) - math.tan(Unit.ConvertDegToRad(angleGradientSlope_0.Degrees - 0.01)));
        self.__isad75 = 75 * double_0 / (288 + double_0 - 0.00325 * (altitude_1.Metres + 75));
        self.__isadFAP = (altitude_0.Metres - altitude_1.Metres) * double_0 / (288 + double_0 - 0.00325 * altitude_0.Metres);
        self.__bg_tf = 7.6;
        self.__bg_rf = max([40 * math.sin(Unit.ConvertDegToRad(double_2)), self.__bg_tf])
        self.__moc75_tf = self.__bg_tf - self.__isad75 + 1.33333333333333 * math.sqrt(self.__anpe * self.__anpe + self.__wpr * self.__wpr + self.__fte * self.__fte + self.__ase75 * self.__ase75 + self.__vae75 * self.__vae75 + self.__atis * self.__atis);
        self.__moc75_rf = self.__bg_rf - self.__isad75 + 1.33333333333333 * math.sqrt(self.__anpe * self.__anpe + self.__wpr * self.__wpr + self.__fte * self.__fte + self.__ase75 * self.__ase75 + self.__vae75 * self.__vae75 + self.__atis * self.__atis);
        self.__mocFAP_tf = self.__bg_tf - self.__isadFAP + 1.33333333333333 * math.sqrt(self.__anpe * self.__anpe + self.__wpr * self.__wpr + self.__fte * self.__fte + self.__aseFAP * self.__aseFAP + self.__vaeFAP * self.__vaeFAP + self.__atis * self.__atis);
        self.__mocFAP_rf = self.__bg_rf - self.__isadFAP + 1.33333333333333 * math.sqrt(self.__anpe * self.__anpe + self.__wpr * self.__wpr + self.__fte * self.__fte + self.__aseFAP * self.__aseFAP + self.__vaeFAP * self.__vaeFAP + self.__atis * self.__atis);
        self.__OASgradient_tf = (altitude_0.Metres - altitude_1.Metres - self.__mocFAP_tf - (75 - self.__moc75_tf)) / ((altitude_0.Metres - altitude_1.Metres - 75) / math.tan(angleGradientSlope_0.Radians));
        self.__OASgradient_rf = (altitude_0.Metres - altitude_1.Metres - self.__mocFAP_rf - (75 - self.__moc75_rf)) / ((altitude_0.Metres - altitude_1.Metres - 75) / math.tan(angleGradientSlope_0.Radians));
        self.__OASorigin_tf = (75 - altitude_2.Metres) / math.tan(angleGradientSlope_0.Radians) - (75 - self.__moc75_tf) / self.__OASgradient_tf;
        self.__OASorigin_rf = (75 - altitude_2.Metres) / math.tan(angleGradientSlope_0.Radians) - (75 - self.__moc75_rf) / self.__OASgradient_rf;

    def get_fte(self):
        return Distance(self.__fte)


    def get_atis(self):
        return Distance(self.__atis)


    def get_anpe(self):
        return Distance(self.__anpe)


    def get_wpr(self):
        return Distance(self.__wpr)


    def get_ase_75(self):
        return Distance(self.__ase75)


    def get_ase_fap(self):
        return Distance(self.__aseFAP)


    def get_vae_75(self):
        return Distance(self.__vae75)


    def get_vae_fap(self):
        return Distance(self.__vaeFAP)


    def get_isad_75(self):
        return Distance(self.__isad75)


    def get_isad_fap(self):
        return Distance(self.__isadFAP)


    def get_bg_tf(self):
        return Distance(self.__bg_tf)


    def get_bg_rf(self):
        return Distance(self.__bg_rf)


    def get_moc_75_tf(self):
        return Altitude(self.__moc75_tf)


    def get_moc_75_rf(self):
        return Altitude(self.__moc75_rf)


    def get_moc_fap_tf(self):
        return Altitude(self.__mocFAP_tf)


    def get_moc_fap_rf(self):
        return Altitude(self.__mocFAP_rf)


    def get_oasgradient_tf(self):
        return AngleGradientSlope(self.__OASgradient_tf * 100, AngleGradientSlopeUnits.Percent)


    def get_oasgradient_rf(self):
        return AngleGradientSlope(self.__OASgradient_rf * 100, AngleGradientSlopeUnits.Percent)


    def get_oasorigin_tf(self):
        return Distance(self.__OASorigin_tf)


    def get_oasorigin_rf(self):
        return Distance(self.__OASorigin_rf)


    def method_0(self, double_0):
        num = math.tan(self.vpa.Radians);
        metres = (6367435.67964 + self.ltp.Metres + self.rdh.Metres) * math.exp(double_0 / (6367435.67964 / num)) - 6367435.67964 - self.ltp.Metres;
        metres1 = (6367435.67964 + self.ltp.Metres) * math.exp((double_0 - self._OASorigin_tf) / (6367435.67964 / self._OASgradient_tf)) - 6367435.67964 - self.ltp.Metres;
        return metres - metres1;

    def method_1(self, double_0):
        num = math.tan(self.vpa.Radians);
        metres = (6367435.67964 + self.ltp.Metres + self.rdh.Metres) * math.exp(double_0 / (6367435.67964 / num)) - 6367435.67964 - self.ltp.Metres;
        metres1 = (6367435.67964 + self.ltp.Metres) * math.exp((double_0 - self.__OASorigin_rf) / (6367435.67964 / self.__OASgradient_rf)) - 6367435.67964 - self.ltp.Metres;
        return metres - metres1;

    def method_2(self, double_0):
        metres = (6367435.67964 + self.ltp.Metres) * math.exp((double_0 - self.__OASorigin_tf) / (6367435.67964 / self.__OASgradient_tf)) - 6367435.67964 - self.ltp.Metres;
        return math.floor(metres);

    def method_3(self, double_0):
        metres = (6367435.67964 + self.ltp.Metres) * math.exp((double_0 - self.__OASorigin_rf) / (6367435.67964 / self.__OASgradient_rf)) - 6367435.67964 - self.ltp.Metres;
        return math.floor(metres);
    fte = property(get_fte, None, None, None)
    atis = property(get_atis, None, None, None)
    anpe = property(get_anpe, None, None, None)
    wpr = property(get_wpr, None, None, None)
    ase75 = property(get_ase_75, None, None, None)
    aseFAP = property(get_ase_fap, None, None, None)
    vae75 = property(get_vae_75, None, None, None)
    vaeFAP = property(get_vae_fap, None, None, None)
    isad75 = property(get_isad_75, None, None, None)
    isadFAP = property(get_isad_fap, None, None, None)
    bg_TF = property(get_bg_tf, None, None, None)
    bg_RF = property(get_bg_rf, None, None, None)
    moc75_TF = property(get_moc_75_tf, None, None, None)
    moc75_RF = property(get_moc_75_rf, None, None, None)
    mocFAP_TF = property(get_moc_fap_tf, None, None, None)
    mocFAP_RF = property(get_moc_fap_rf, None, None, None)
    OASgradient_TF = property(get_oasgradient_tf, None, None, None)
    OASgradient_RF = property(get_oasgradient_rf, None, None, None)
    OASorigin_TF = property(get_oasorigin_tf, None, None, None)
    OASorigin_RF = property(get_oasorigin_rf, None, None, None)

class RnpArTemperatureComponents:

    def __init__(self, speed_0, angleGradientSlope_0, double_0, double_1, altitude_0, altitude_1, altitude_2, aircraftSpeedCategory_0):
        self.ISA_airport = 15 - 0.00198 * altitude_0.Feet
        self.ISA_low = -(self.ISA_airport - double_1)
        feet = altitude_1.Feet - altitude_2.Feet;
        isaLow = self.ISA_low * (0.19 + 0.0038 * feet) + 0.032 * feet + 4.9;
        num = feet / math.tan(angleGradientSlope_0.Radians)
        self.VPA_min = AngleGradientSlope(Unit.smethod_1(math.atan((feet + isaLow) / num)))
        self.NA_below = self.ISA_airport + self.ISA_low
        if (self.VPA_min.Degrees < 2.5):
            num1 = num * math.tan(Unit.ConvertDegToRad(2.5)) + altitude_2.Feet
            feet1 = altitude_1.Feet - num1
            self.ISA_low_25 = (-feet1 - 0.032 * feet - 4.9) / (0.19 + 0.0038 * feet)
            self.NA_below_25 = self.ISA_airport + self.ISA_low_25
        if aircraftSpeedCategory_0 == AircraftSpeedCategory.A:
            if (speed_0.Knots < 80 or speed_0.Knots >= 90):
                self.VPA_max = AngleGradientSlope(7.232)
            else:
                self.VPA_max = AngleGradientSlope(6.441)
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.B:
            self.VPA_max = AngleGradientSlope(4.746);
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.C:
            self.VPA_max = AngleGradientSlope(4.068);
        elif aircraftSpeedCategory_0 == AircraftSpeedCategory.D:
            self.VPA_max = AngleGradientSlope(3.503);
        else:
            self.VPA_max = AngleGradientSlope(4.068)
            
        num2 = num * math.tan(self.VPA_max.Radians) + altitude_2.Feet
        feet2 = num2 - altitude_1.Feet
        self.ISA_high = (feet2 - 0.032 * feet - 4.9) / (0.19 + 0.0038 * feet)
        self.NA_above = self.ISA_airport + self.ISA_high

class RnpArSegmentObstacles(ObstacleTable):
    resultOCA = None
    resultOCH = None
    def __init__(self, rnpArDataGroup_0, rnpArCalculatedSegments_0):
        '''
        Constructor
        '''
        ObstacleTable.__init__(self, rnpArCalculatedSegments_0)
        self.surfaceType = SurfaceTypes.RnpAR
        self.group = rnpArDataGroup_0
        self.fas = None
        self.mas = None
        self.ins = None
        self.ias = None
        
        if not isinstance(rnpArCalculatedSegments_0[0] ,RnpArMissedApproachSegment):
            self.fas = rnpArCalculatedSegments_0[0]
            if (rnpArCalculatedSegments_0.Count > 1):
                self.ins = rnpArCalculatedSegments_0[1]
            if (rnpArCalculatedSegments_0.Count > 2):
                self.ias = rnpArCalculatedSegments_0[2]
        else:
            self.xmas = rnpArDataGroup_0.Xmas.Metres
            self.tanZ = math.tan(rnpArDataGroup_0.MACG.Radians)
            self.cotZ = 1 / self.tanZ
            vPA = rnpArDataGroup_0.VPA
            self.cotVPA = 1 / math.tan(vPA.Radians)
            self.mas = rnpArCalculatedSegments_0[0]
            self.fas = rnpArCalculatedSegments_0[1]
            if (rnpArCalculatedSegments_0.Count > 2):
                self.ins = rnpArCalculatedSegments_0[2]
            if (rnpArCalculatedSegments_0.Count > 3):
                self.ias = rnpArCalculatedSegments_0[3]

        self.ltpAlt = rnpArDataGroup_0.LTP.z()
        self.nominal = rnpArCalculatedSegments_0.method_3(rnpArDataGroup_0.LTP)
        RnpArSegmentObstacles.resultOCA = Altitude(rnpArDataGroup_0.LTP.z()) + rnpArDataGroup_0.HL
        RnpArSegmentObstacles.resultOCH = rnpArDataGroup_0.HL
        temperatureComponents = rnpArDataGroup_0.TemperatureComponents
        self.veb = RnpArVebComponents(temperatureComponents.ISA_low, rnpArDataGroup_0.MaxFinalRnp, rnpArDataGroup_0.MaxFinalBankRF, rnpArDataGroup_0.VPA, rnpArDataGroup_0.FAP, Altitude(rnpArDataGroup_0.LTP.z()), rnpArDataGroup_0.RDH)
        if (rnpArDataGroup_0.Legs_FA[rnpArDataGroup_0.Legs_FA.Count - 1].Type != RnpArLegType.RF):
            self.mocFAP = self.veb.mocFAP_TF.Metres
        else:
            self.mocFAP = self.veb.mocFAP_RF.Metres
        self.xVeb = self.veb.OASorigin_TF.Metres
        if (rnpArDataGroup_0.Legs_MA.Count > 0):
            rnp = rnpArDataGroup_0.Legs_MA[0].Rnp
        else:
            num = rnpArDataGroup_0.Legs_FA[0].Rnp
        self.xZ = rnpArDataGroup_0.Xz.Metres
                
    def addObstacleToModel(self, obstacle, checkResult):
        ObstacleTable.addObstacleToModel(self, obstacle, checkResult)
        row = self.source.rowCount() - 1
#         colCount = self.source.columnCount()
         
        item = QStandardItem(str(checkResult[0]))
        item.setData(checkResult[0])
        self.source.setItem(row, self.IndexMocAppliedM, item)
         
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[0])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[0]))
        self.source.setItem(row, self.IndexMocAppliedFt, item)
         
        item = QStandardItem(str(checkResult[1]))
        item.setData(checkResult[1])
        self.source.setItem(row, self.IndexDxM, item)
         
        item = QStandardItem(str(checkResult[2]))
        item.setData(checkResult[2])
        self.source.setItem(row, self.IndexEqAltM, item)
         
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[2])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[2]))
        self.source.setItem(row, self.IndexEqAltFt, item)
         
        item = QStandardItem(str(checkResult[3]))
        item.setData(checkResult[3])
        self.source.setItem(row, self.IndexSurfAltM, item)
         
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[3])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[3]))
        self.source.setItem(row, self.IndexSurfAltFt, item)
         
        item = QStandardItem(str(checkResult[4]))
        item.setData(checkResult[4])
        self.source.setItem(row, self.IndexDifferenceM, item)
         
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[4])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[4]))
        self.source.setItem(row, self.IndexDifferenceFt, item)
         
        item = QStandardItem(str(checkResult[5]))
        item.setData(checkResult[5])
        self.source.setItem(row, self.IndexOcaM, item)
         
        item = QStandardItem(str(Unit.ConvertMeterToFeet(checkResult[5])))
        item.setData(Unit.ConvertMeterToFeet(checkResult[5]))
        self.source.setItem(row, self.IndexOcaFt, item)
 
        item = QStandardItem(str(checkResult[6]))
        item.setData(checkResult[6])
        self.source.setItem(row, self.IndexCritical, item)
 
        item = QStandardItem(str(checkResult[7]))
        item.setData(checkResult[7])
        self.source.setItem(row, self.IndexSurface, item)
        
    def setHeaderLabels(self):
        ObstacleTable.setHeaderLabels(self)
        fixedColumnCount = len(self.fixedColumnLabels)
        self.IndexMocAppliedM = fixedColumnCount
        self.IndexMocAppliedFt = fixedColumnCount + 1
        self.IndexMocMultiplier = fixedColumnCount + 2
        self.IndexDxM = fixedColumnCount + 3
        self.IndexEqAltM = fixedColumnCount + 4
        self.IndexEqAltFt = fixedColumnCount + 5
        self.IndexSurfAltM = fixedColumnCount + 6
        self.IndexSurfAltFt = fixedColumnCount + 7
        self.IndexDifferenceM = fixedColumnCount + 8
        self.IndexDifferenceFt = fixedColumnCount + 9
        self.IndexOcaM = fixedColumnCount + 10
        self.IndexOcaFt = fixedColumnCount + 11
        self.IndexCritical = fixedColumnCount + 12
        self.IndexSurface = fixedColumnCount + 13
        
        self.fixedColumnLabels.extend([
                ObstacleTableColumnType.MocAppliedM,
                ObstacleTableColumnType.MocAppliedFt,
                ObstacleTableColumnType.MocMultiplier,
                ObstacleTableColumnType.DxM,
                ObstacleTableColumnType.EqAltM,
                ObstacleTableColumnType.EqAltFt,
                ObstacleTableColumnType.SurfAltM,
                ObstacleTableColumnType.SurfAltFt,
                ObstacleTableColumnType.DifferenceM,
                ObstacleTableColumnType.DifferenceFt,
                ObstacleTableColumnType.OcaM,
                ObstacleTableColumnType.OcaFt,
                ObstacleTableColumnType.Critical,
                ObstacleTableColumnType.Surface
                ])
        self.source.setHorizontalHeaderLabels(self.fixedColumnLabels)

    def checkObstacle(self, obstacle_0):
        if define._units == QGis.Meters:
            position = obstacle_0.position
        else:
            position = obstacle_0.positionDegree
            
        tolerance = obstacle_0.tolerance
        trees = obstacle_0.trees
        z = position.get_Z() + trees
        for fa in self.fas:
            if (not fa.PrimaryArea.pointInPolygon(position, tolerance)):
                continue
            closestPointTo = self.nominal.GetClosestPointTo(position, False)
            num = max([self.nominal.GetDistAtPoint(closestPointTo) - tolerance, 0])
            num1 = 0
            if (fa.LegType == RnpArCalculatedLegType.RF):
                if (num > self.veb.OASorigin_RF.Metres):
                    num1 = self.veb.method_3(num)
            elif (num > self.veb.OASorigin_TF.Metres):
                num1 = self.veb.method_2(num)
            num2 = self.ltpAlt + num1
            z1 = None
            criticalObstacleType = CriticalObstacleType.No
            if (z > num2):
                criticalObstacleType = CriticalObstacleType.Yes
                hL = self.group.HL
                z1 = position.get_Z() + trees + hL.Metres
                if (z1 > RnpArSegmentObstacles.resultOCA.Metres):
                    RnpArSegmentObstacles.resultOCA = Altitude(z1)
                    RnpArSegmentObstacles.resultOCH = Altitude(z1 - self.ltpAlt)
            
            calcResult = [None, num, None, num2, z - num2, z1, criticalObstacleType, RnpArSegmentType.Final]
            self.addObstacleToModel(obstacle_0, calcResult)
            metres = self.group.MOC_I.Metres * obstacle_0.MocMultiplier
            if (num2 <= self.group.FAP.Metres - metres):
                continue
            z1 = position.get_Z() + trees + metres
            criticalObstacleType = CriticalObstacleType.Yes if z1 > self.group.FAP.Metres else CriticalObstacleType.No
            self.addObstacleToModel(obstacle_0, [metres, None, None, None, None, z1, criticalObstacleType, RnpArSegmentType.Intermediate])

        if (self.mas != None):
            segmentLength = 0
            for ma in self.mas:
                if (ma.PrimaryArea.pointInPolygon(position, tolerance)):
                    distance, mocMultiplier = ma.method_0(position)
                    num3 = self.xmas - (segmentLength + distance)
                    if (num3 - tolerance > self.xVeb):
                        point3d = self.nominal.GetClosestPointTo(position, False);
                        num3 = max([self.nominal.GetDistAtPoint(point3d) - tolerance, 0])
                        num4 = 0
                        if (num3 > self.veb.OASorigin_TF.Metres):
                            num4 = self.veb.method_2(num3)
                        num5 = self.ltpAlt + num4
                        z2 = None
                        criticalObstacleType1 = CriticalObstacleType.No
                        if (z > num5):
                            criticalObstacleType1 = CriticalObstacleType.Yes
                            altitude = self.group.HL
                            z2 = position.get_Z() + trees + altitude.Metres
                            if (z2 > RnpArSegmentObstacles.resultOCA.Metres):
                                RnpArSegmentObstacles.resultOCA = Altitude(z2)
                                RnpArSegmentObstacles.resultOCH = Altitude(z2 - self.ltpAlt)
                        self.addObstacleToModel(obstacle_0, [None, num3, None, num5, z - num5, z2, criticalObstacleType1, RnpArSegmentType.Final])

                    elif (num3 + tolerance <= self.xZ):
                        num3 = num3 + tolerance
                        mocMultiplier = mocMultiplier * obstacle_0.MocMultiplier
                        num6 = z + mocMultiplier;
                        num7 = num6 - self.ltpAlt;
                        num8 = self.ltpAlt + self.tanZ * (math.fabs(num3) + self.xZ);
                        num9 = None;
                        metres1 = None;
                        criticalObstacleType2 = CriticalObstacleType.No
                        if (num6 > num8):
                            criticalObstacleType2 = CriticalObstacleType.Yes
                            num10 = (num7 * self.cotZ - self.xZ + (num3 + tolerance)) / (self.cotVPA + self.cotZ)
                            num9 = self.ltpAlt + num10
                            metres1 = num9 + self.group.HL.Metres
                            if (metres1 > RnpArSegmentObstacles.resultOCA.Metres):
                                RnpArSegmentObstacles.resultOCA = Altitude(metres1)
                                RnpArSegmentObstacles.resultOCH = Altitude(metres1 - self.ltpAlt)

                        self.addObstacleToModel(obstacle_0, [mocMultiplier, num3, num9, num8, num6 - num8, metres1, criticalObstacleType2, RnpArSegmentType.Missed])
                    else:
                        num11 = self.ltpAlt
                        z3 = None
                        criticalObstacleType3 = CriticalObstacleType.No
                        if (z > num11):
                            criticalObstacleType3 = CriticalObstacleType.Yes
                            hL1 = self.group.HL
                            z3 = position.get_Z() + trees + hL1.Metres
                            if (z3 > RnpArSegmentObstacles.resultOCA.Metres):
                                RnpArSegmentObstacles.resultOCA = Altitude(z3)
                                RnpArSegmentObstacles.resultOCH = Altitude(z3 - self.ltpAlt)

                        self.addObstacleToModel(obstacle_0, [None, num3 + tolerance, None, num11, z - num11, z3, criticalObstacleType3, RnpArSegmentType.Missed])

                segmentLength = segmentLength + ma.SegmentLength

        if (self.ins != None):
            mOCI = self.group.MOC_I
            num12 = max([mOCI.Metres * obstacle_0.MocMultiplier, self.mocFAP])
            
            for current in self.ins:
                if (current.PrimaryArea.pointInPolygon(position, tolerance)):
                    z4 = position.get_Z() + trees + num12;
                    criticalObstacleType4 = CriticalObstacleType.Yes if z4 > self.group.FAP.Metres else CriticalObstacleType.No
                    self.addObstacleToModel(obstacle_0, [num12, None, None, None, None, z4, criticalObstacleType4, RnpArSegmentType.Intermediate])

        if (self.ias != None):
            metres2 = self.group.MOC_IA.Metres * obstacle_0.MocMultiplier
            
            for current in self.ias:
                if current.PrimaryArea.pointInPolygon(position, tolerance):
                    z5 = position.get_Z() + trees + metres2
                    self.addObstacleToModel(obstacle_0, [metres2, None, None, None, None, z5, CriticalObstacleType.No, RnpArSegmentType.Initial])

        return ObstacleTable.checkObstacle(self, obstacle_0)