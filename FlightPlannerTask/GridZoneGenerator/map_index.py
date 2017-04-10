# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LoadByClass
                                 A QGIS plugin
 Load database classes.
                             -------------------
        begin                : 2014-12-18
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
        mod history          : 2014-12-17 by Leonardo Lourenço - Computing Engineer @ Brazilian Army
        mod history          : 2014-12-17 by Maurício de Paulo - Cartographic Engineer @ Brazilian Army
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot, QVariant
from qgis.core import QgsPoint, QgsGeometry, QgsFeature, QgsVectorLayer, QgsField, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.core import QgsMapLayerRegistry, QgsVectorFileWriter
import string, os

from Type.String import String

class Aux(QObject):
    rangeCalculated = pyqtSignal(int)
    processFinished = pyqtSignal()
    stepProcessed = pyqtSignal()
    errorOccurred = pyqtSignal(str)
    userCanceled = pyqtSignal()

    def __init__(self, thread):
        super(Aux, self).__init__()

        self.thread = thread
        
    def getMemoryLayerErrorMessage(self):
        return self.tr('Problem loading memory layer!')

    def getIndexFieldName(self):
        return self.tr('map_index')

    @pyqtSlot()
    def cancel(self):
        self.thread.stop()

class UtmGrid(QObject):#(QRunnable):
    def __init__(self):
        """Constructor."""
        # super(UtmGrid, self).__init__()
        
        self.scales = [1000,500,250,100,50,25,10,5,2,1]
        nomen1000 = ['Nao Recorta']
        nomen500 = [['V','X'],['Y','Z']]
        nomen250 = [['A','B'],['C','D']]
        nomen100 = [['I','II','III'],['IV','V','VI']]
        nomen50 = [['1','2'],['3','4']]
        nomen25 = [['NO','NE'],['SO','SE']]
        nomen10 = [['A','B'],['C','D'],['E','F']]
        nomen5 = [['I','II'],['III','IV']]
        nomen2 = [['1', '2', '3'], ['4', '5', '6']]
        nomen1 = [['A','B'],['C','D']]
        self.scaleText = [nomen1000,nomen500,nomen250,nomen100,nomen50,nomen25,nomen10,nomen5,nomen2,nomen1]
        self.matrizRecorte = []
        self.spacingX = []
        self.spacingY = []
        self.stepsDone = 0
        self.stepsTotal = 0
        self.featureBuffer = []
        self.MIdict = []
        self.MIRdict = []
        
        self.aux = Aux(self)

        self.stopped = False

    def stop(self):
        self.stopped = True
    
    def findScaleText(self, scaleText, scaleId):
        """Get the scale matrix for the given scaleText and scaleId
        """
        j = -1
        for j, row in enumerate(self.scaleText[scaleId]):
            if scaleText in row:
                i=row.index(scaleText)
                break
        return (i, len(self.scaleText[scaleId])-j-1)
        
    def getScale(self, inomen):
        """Get scale for the given map index
        """
        return self.scales[ self.getScaleIdFromiNomen(inomen) ]
    
    def getScaleIdFromiNomen(self, inomen):
        """Get scale index in self.scales object for the given map index
        """
        id = len(inomen.split('-')) - 2
        return id
     
    def getScaleIdFromScale(self, scale):
        """Get scale if for the given scale (e.g. 1, 2, 25, 250)
        """
        return self.scales.index(scale)

    def getSpacingX(self, scale):
        """Get X spacing fot the given scale
        """
        scaleId = self.scales.index(scale)
        if scaleId < 0: return 0
        if len(self.spacingX) == 0:
            dx = 6
            self.spacingX = [dx]
            for i in range(1, len(self.scaleText)):
                subdivisions = len(self.scaleText[i][0])
                dx /= float(subdivisions)
                self.spacingX.append(dx)
        return self.spacingX[scaleId]
    
    def getSpacingY(self, scale):
        """Get Y spacing fot the given scale
        """
        scaleId = self.scales.index(scale)
        if scaleId < 0: return 0
        if len(self.spacingY) == 0:
            dy = 4
            self.spacingY = [dy]
            for i in range(1, len(self.scaleText)):
                subdivisions = len(self.scaleText[i])
                dy /= float(subdivisions)
                self.spacingY.append(dy)
        return self.spacingY[scaleId]
    
    def makeQgsPolygon(self, xmin, ymin, xmax, ymax):
        """Creating a polygon for the given coordinates
        """
        dx = (xmax - xmin)/3
        dy = (ymax - ymin)/3
        
        polyline = []

        point = QgsPoint(xmin, ymin)
        polyline.append(point)
        point = QgsPoint(xmin+dx, ymin)
        polyline.append(point)
        point = QgsPoint(xmax-dx, ymin) 
        polyline.append(point)
        point = QgsPoint(xmax, ymin)
        polyline.append(point)
        point = QgsPoint(xmax, ymin+dy)
        polyline.append(point)
        point = QgsPoint(xmax, ymax-dy)
        polyline.append(point)
        point = QgsPoint(xmax, ymax)
        polyline.append(point)
        point = QgsPoint(xmax-dx, ymax)
        polyline.append(point)
        point = QgsPoint(xmin+dx, ymax)
        polyline.append(point)
        point = QgsPoint(xmin, ymax)
        polyline.append(point)
        point = QgsPoint(xmin, ymax-dy)
        polyline.append(point)
        point = QgsPoint(xmin, ymin+dy)
        polyline.append(point)
        point = QgsPoint(xmin, ymin)
        polyline.append(point)

        qgsPolygon = QgsGeometry.fromMultiPolygon([[polyline]])
        return qgsPolygon
        
    def getHemisphereMultiplier(self,inomen):
        """Check the hemisphere
        """
        inomen = String.QString2Str(inomen)
        if len(inomen) > 1:
            h = inomen[0].upper()
            if h == 'S':
                return -1
            else:
                return 1

    def getLLCornerLatitude1kk(self,inomen):
        """Get lower left Latitude for 1:1.000.000 scale
        """
        inomen = String.QString2Str(inomen)
        l = inomen[1].upper()
        y = 0.0;
        operator = self.getHemisphereMultiplier(inomen)
        verticalPosition = string.uppercase.index(l)
        y = (y+4*verticalPosition)*operator
        if (operator<0): y-=4
        return y

    def getLLCornerLongitude1kk(self,inomen):
        """Get lower left Longitude for 1:1.000.000 scale
        """
        inomen = String.QString2Str(inomen)
        fuso = int(inomen[3:5])
        x = 0
        if((fuso > 0) and (fuso <= 60)):
            x = (((fuso - 30)*6.0)-6.0)
        return x
    
    def getLLCorner(self,inomen):
        """Get lower left coordinates for scale determined by the given map index
        """
        inomen = String.QString2Str(inomen)
        x = self.getLLCornerLongitude1kk(inomen)
        y = self.getLLCornerLatitude1kk(inomen)
        inomenParts = inomen.upper().split('-')
        #Escala de 500.00
        for partId in range(2,len(inomenParts)):
            scaleId = partId-1
            dx = self.getSpacingX(self.scales[scaleId])
            dy = self.getSpacingY(self.scales[scaleId])
            scaleText = inomenParts[partId]
            i,j = self.findScaleText(scaleText, partId-1)
            x += i*dx
            y += j*dy
        return (x,y)
    
    def computeNumberOfSteps(self,startScaleId,stopScaleId):
        """Compute the number of steps to build a progress
        """
        steps=1
        for i in range(startScaleId+1,stopScaleId+1):
            steps *= len(self.scaleText[i])*len(self.scaleText[i][0])
        return steps

    def getQgsPolygonFrame(self, map_index):
        """Particular case used to create frame polygon for the given
        map_index
        """
        scale = self.getScale(map_index)
        (x, y) = self.getLLCorner(map_index)
        dx = self.getSpacingX(scale)
        dy = self.getSpacingY(scale)
        poly = self.makeQgsPolygon(x, y, x + dx, y + dy)
        return poly
    
    def populateQgsLayer(self, iNomen, stopScale, layer, mi = ''):
        """Generic recursive method to create frame polygon for the given
        stopScale within the given map index (iNomen)
        """
        if self.stopped:
            del layer
            layer = None
            self.aux.userCanceled.emit()
            return

        scale = self.getScale(iNomen)            
        #first run
        if (self.stepsTotal==0):
            self.stepsTotal=self.computeNumberOfSteps(self.getScaleIdFromScale(scale), self.getScaleIdFromScale(stopScale))
            self.aux.rangeCalculated.emit(self.stepsTotal*2)
            self.stepsDone = 0
        if scale == stopScale:
            (x, y) = self.getLLCorner(iNomen)
            dx = self.getSpacingX(stopScale)
            dy = self.getSpacingY(stopScale)
            poly = self.makeQgsPolygon(x, y, x + dx, y + dy)
            
            self.insertFrameIntoQgsLayer(layer, poly, iNomen, mi)
            
            self.stepsDone += 1
            self.aux.stepProcessed.emit()
        else:
            scaleId = self.getScaleIdFromiNomen(iNomen)
            matrix = self.scaleText[ scaleId+1 ]
            
            for i in range(len(matrix)):
                line = matrix[i]
                for j in range(len(line)):
                    inomen2 = iNomen + '-' + line[j]
                    mi2 = mi + '-' + line[j]
                    self.populateQgsLayer(inomen2, stopScale, layer, mi2)
                    
    def insertFrameIntoQgsLayer(self, layer, poly, map_index, mi):
        """Inserts the poly into layer
        """
        provider = layer.dataProvider()

        #Creating the feature
        feature = QgsFeature()
        feature.setGeometry(poly)
        feature.setAttributes([map_index, mi])

        # Adding the feature into the file
        provider.addFeatures([feature])
    
    def getMIdict(self):
        if not self.MIdict:
            self.MIdict = self.getDict("MI100.csv")
        return self.MIdict
            
    def getMIRdict(self):
        if not self.MIRdict:
            self.MIRdict = self.getDict("MIR250.csv")
        return self.MIRdict    
    
    def getDict(self, file_name):    
        csvFile = open(os.path.join(os.path.dirname(__file__),file_name))
        data = csvFile.readlines()
        csvFile.close()
        l1 = map(lambda x: (x.strip()).split(';'),data)
        dicionario = dict((a[1].lstrip('0'),a[0]) for a in l1)
        return dicionario

    def getINomenFromMI(self,mi):
        return self.getINomen(self.getMIdict(), mi)

    def getINomenFromMIR(self,mir):
        return self.getINomen(self.getMIRdict(), mir)
        
    def getINomen(self, dict, index):
        key = index.split('-')[0]
        otherParts = index.split('-')[1:]
        if (dict.has_key(key)):
            return dict[key]+'-'+string.join(otherParts,'-')
        else:
            return ''

    def getMIFromINomen(self,inomen):
        return self.getMI(self.getMIdict(), inomen)

    def getMI(self, dict, inomen):
        if inomen in dict.values():
            return dict.keys()[dict.values().index(inomen)].lstrip('0')
        else:
            return ''
        
    def setParameters(self, index, stopScale, mi, crs, output, layer = None):
        self.index = index
        self.stopScale = stopScale
        self.mi = mi
        self.crs = crs
        self.output = output
        self.layer = layer

    def createGridLayer(self, name, layerType, crsAuthId):
        layer = QgsVectorLayer('%s?crs=%s'% (layerType, crsAuthId), name, 'memory')
        if not layer.isValid():
            self.aux.errorOccurred.emit(self.aux.getMemoryLayerErrorMessage())
            return
        provider = layer.dataProvider()
        provider.addAttributes([QgsField(self.aux.getIndexFieldName(), QVariant.String), QgsField('mi', QVariant.String)])
        layer.updateFields()
        return layer
    
    def run(self):
        tempLayer = self.createGridLayer('temp', 'Multipolygon', self.crs.geographicCRSAuthId())

        self.populateQgsLayer(self.index, self.stopScale, tempLayer, self.mi)
        
        useMemory = True
        if not self.layer:
            useMemory = False
            self.layer = self.createGridLayer('Grid Zones', 'Multipolygon', self.crs.authid())
        
        for feature in tempLayer.getFeatures():
            if self.stopped:
                del tempLayer
                tempLayer = None
                self.aux.userCanceled.emit()
                return

            geom = feature.geometry()
            reprojected = self.reprojectGridZone(geom)
            self.insertGridZoneIntoQgsLayer(self.layer, reprojected, feature.attributes())
            self.aux.stepProcessed.emit()

        del tempLayer
        tempLayer = None
        
        self.aux.stepProcessed.emit()

        if not useMemory:
            QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.output, "utf-8", None, "ESRI Shapefile")

        self.aux.processFinished.emit()

    def reprojectGridZone(self, multipoly):
        crsSrc = QgsCoordinateReferenceSystem(self.crs.geographicCRSAuthId())
        coordinateTransformer = QgsCoordinateTransform(crsSrc, self.crs)
        polyline = multipoly.asMultiPolygon()[0][0]
        newPolyline = []
        for point in polyline:
            newPolyline.append(coordinateTransformer.transform(point))
        qgsMultiPolygon = QgsGeometry.fromMultiPolygon([[newPolyline]])
        return qgsMultiPolygon

    def insertGridZoneIntoQgsLayer(self, layer, multipoly, attributes):
        """Inserts the poly into layer
        """
        provider = layer.dataProvider()

        #Creating the feature
        feature = QgsFeature()
        feature.setGeometry(multipoly)
        feature.setAttributes(attributes)

        # Adding the feature into the file
        provider.addFeatures([feature])
        