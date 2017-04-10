
from qgis.core import QGis, QgsGeometry, QgsFeature, QGis, QgsField, QgsFields, QgsPoint
from PyQt4.QtCore import QVariant
from FlightPlanner.types import Point3D
from FlightPlanner.polylineArea import PolylineArea, PolylineAreaPoint



class DBText:
    def __init__(self):
        self.string = ""
        self.position = None
        self.height = 8
        self.verticalMode = None
        self.horizontalMode = None
        self.alignmentPoint = None
        self.rotation = 0.0

        self.point3d = None
        self.layerType = QGis.Line
        self.xData = None
    
    def set_LayerType(self, geometryType):
        self.layerType = geometryType
        
    def set_AlignmentPoint(self, val):
        self.alignmentPoint = val

    def set_HorizontalMode(self, hMode):
        self.horizontalMode = hMode

    def set_Rotation(self, rotationValue):
        self.rotation = rotationValue

    def set_VerticalMode(self, vMode):
        self.verticalMode = vMode

    def set_TextString(self, string):
        self.string = string

    def set_Position(self, point3d):
        self.position = point3d

        if self.layerType == QGis.Line:
            self.geometry = PolylineArea([point3d, Point3D(point3d.get_X() + 0.000000001, point3d.get_Y())])
        elif self.layerType == QGis.Point:
            self.geometry = point3d
        elif self.layerType == QGis.Polygon:
            self.geometry = PolylineArea([point3d, Point3D(point3d.get_X() + 0.000000001, point3d.get_Y()), Point3D(point3d.get_X() + 0.000000001, point3d.get_Y()+ 0.000000001), Point3D(point3d.get_X(), point3d.get_Y()+ 0.000000001), point3d])


    def set_Height(self, heightValue):
        self.height = heightValue
    def set_XData(self, xData):
        self.xData = xData

class Line(PolylineArea):
    def __init__(self, pointer1 = None, pointer2 = None):
        PolylineArea.__init__(self)
        if pointer1 != None:
            self.Add(PolylineAreaPoint(pointer1))
            self.Add(PolylineAreaPoint(pointer2))

        self.xData = dict()
        self.caption = ""
        self.type = "Line"
    def set_StartPoint(self, point3d):
        self.clear()
        self.Add(PolylineAreaPoint(point3d))
    def set_EndPoint(self, point3d):
        self.Add(PolylineAreaPoint(point3d))

    def set_XData(self, data):
        self.xData = data

    def get_StartPoint(self):
        return self[0].Position

    def get_EndPoint(self):
        return self[len(self) - 1].Position
class Feature(QgsFeature):
    def __init__(self, geom = None, attributes = None):
        QgsFeature.__init__(self)

        self.xData = dict()
        self.caption = ""
        self.type = "Line"

        fieldAltitude = "Altitude"
        fieldName = "Caption"
        fieldNameBulge = "Bulge"
        fieldNameGeometryType = "Type"
        fieldCategory = "CATEGORY"
        fieldXdataName = "XDataName"
        fieldXdataPoint = "XDataPoint"
        fieldXdataTolerence = "XDataTol"
        fieldCenterPoint = "CenterPt"
        fieldSurface = "Surface"

        fields = QgsFields()
        fields.append(QgsField(fieldAltitude, QVariant.String))
        fields.append(QgsField(fieldName, QVariant.String))
        fields.append(QgsField(fieldNameBulge, QVariant.String))
        fields.append(QgsField(fieldNameGeometryType, QVariant.String))
        fields.append(QgsField(fieldCategory, QVariant.String))
        fields.append(QgsField(fieldXdataName, QVariant.String))
        fields.append(QgsField(fieldXdataPoint, QVariant.String))
        fields.append(QgsField(fieldXdataTolerence, QVariant.String))
        fields.append(QgsField(fieldCenterPoint, QVariant.String))
        fields.append(QgsField(fieldSurface, QVariant.String))

        self.setFields(fields)

        if geom != None:
            self.setGeometry(geom)

            if geom.type() == QGis.Line:
                if len(geom.asPolyline()) == 2:
                    self.type = "Line"
                else:
                    self.type = "Polyline"
            elif geom.type() == QGis.Point:
                self.type = "Point"
            elif geom.type() == QGis.Polygon:
                self.type = "Polygon"
            self.setAttribute("Type", self.type)

        if attributes != None:
            attrItems = attributes.items()
            if len(attrItems) != 0:
                for attrList in attrItems:
                    if isinstance(attrList[1], Point3D):
                        attrStr = str(attrList[1].get_X()) + "," + str(attrList[1].get_Y()) + "," + str(attrList[1].get_Z())
                        self.setAttribute(attrList[0], attrStr)
                    elif isinstance(attrList[1], float) or isinstance(attrList[1], int):
                        self.setAttribute(attrList[0], str(attrList[1]))
                    else:
                        self.setAttribute(attrList[0], attrList[1])

    def setAttr(self, attributesDictionary):
        if len(attributesDictionary) == 0:
            return
        attrItems = attributesDictionary.items()
        if len(attrItems) != 0:
            for attrList in attrItems:
                if isinstance(attrList[1], Point3D):
                    attrStr = str(attrList[1].get_X()) + "," + str(attrList[1].get_Y()) + "," + str(attrList[1].get_Z())
                    self.setAttribute(attrList[0], attrStr)
                elif isinstance(attrList[1], float) or isinstance(attrList[1], int):
                    self.setAttribute(attrList[0], str(attrList[1]))
                else:
                    self.setAttribute(attrList[0], attrList[1])
    def setGeom(self, geom):
        if geom != None:
            if geom.type() == QGis.Line:
                self.setGeometry(geom)
                if geom.type() == QGis.Line:
                    if len(geom.asPolyline()) == 2:
                        self.type = "Line"
                    else:
                        self.type = "Polyline"
                elif geom.type() == QGis.Point:
                    self.type = "Point"
                elif geom.type() == QGis.Polygon:
                    self.type = "Polygon"
                self.setAttribute("Type", self.type)
            elif geom.type() == QGis.Point:
                self.setGeometry(geom)
                self.type = "Point"
                self.setAttribute("Type", self.type)
            elif geom.type() == QGis.Polygon:
                self.setGeometry(geom)
                self.type = "Polygon"
                self.setAttribute("Type", self.type)



