# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QAD Quantum Aided Design plugin

 classe per visualizzare i punti di snap
 
                              -------------------
        begin                : 2013-05-22
        copyright            : iiiii
        email                : hhhhh
        developers           : bbbbb aaaaa ggggg
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


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


from qad_snapper import *
from qad_vertexmarker import *
from qad_rubberband import createRubberBand
from qad_msg import QadMsg


class QadSnapPointsDisplayManager():
   """
   Classe che gestisce la visualizzazione dei punti di snap
   """

   
   #============================================================================
   # __init__
   #============================================================================
   def __init__(self, mapCanvas):
      self.__mapCanvas = mapCanvas
      self.__vertexMarkers = [] # lista dei marcatori puntuali visualizzati
      self.__startPoint = QgsPoint()  
      self.__iconSize = QadVariables.get(QadMsg.translate("Environment variables", "AUTOSNAPSIZE"))
      self.__color = QColor(255, 0, 0) # color of the marker
      self.__penWidth = 2 # pen width 
      self.__lineMarkers = [] # lista dei RubberBand visualizzati
   
   #============================================================================
   # __del__
   #============================================================================
   def __del__(self):
      self.removeItems()


   def removeItems(self):
      self.hide()
      
      # svuoto la lista dei marker rimuovendoli dal canvas
      for vertexMarker in self.__vertexMarkers:
         vertexMarker.removeItem()
      del self.__vertexMarkers[:]

      # svuoto la linea di estensione rimuovendoli dal canvas
      for lineMarker in self.__lineMarkers:
         self.__mapCanvas.scene().removeItem(lineMarker)
      del self.__lineMarkers[:]


   def setIconSize(self, iconSize):
      self.__iconSize = iconSize


   def setColor(self, color):
      self.__color = color


   def setPenWidth(self, width):
      self.__penWidth = width


   def setStartPoint(self, point):
      """
      Setta il punto di partenza per la modalità di snap PAR
      """
      self.__startPoint = point


   def __getIconType(self, snapType):     
      if snapType == QadSnapTypeEnum.END or snapType == QadSnapTypeEnum.END_PLINE:
         return QadVertexmarkerIconTypeEnum.BOX
      elif snapType == QadSnapTypeEnum.MID:
         return QadVertexmarkerIconTypeEnum.TRIANGLE
      elif snapType == QadSnapTypeEnum.CEN:
         return QadVertexmarkerIconTypeEnum.CIRCLE
      elif snapType == QadSnapTypeEnum.NOD:
         return QadVertexmarkerIconTypeEnum.CIRCLE_X
      elif snapType == QadSnapTypeEnum.QUA:
         return QadVertexmarkerIconTypeEnum.RHOMBUS
      elif snapType == QadSnapTypeEnum.INT:
         return QadVertexmarkerIconTypeEnum.X
      elif snapType == QadSnapTypeEnum.INS:
         return QadVertexmarkerIconTypeEnum.DOUBLE_BOX
      elif snapType == QadSnapTypeEnum.PER:
         return QadVertexmarkerIconTypeEnum.PERP
      elif snapType == QadSnapTypeEnum.TAN:
         return QadVertexmarkerIconTypeEnum.TANGENT
      elif snapType == QadSnapTypeEnum.NEA:
         return QadVertexmarkerIconTypeEnum.DOUBLE_TRIANGLE
      elif snapType == QadSnapTypeEnum.APP:
         return QadVertexmarkerIconTypeEnum.BOX_X
      elif snapType == QadSnapTypeEnum.EXT:
         return QadVertexmarkerIconTypeEnum.INFINITY_LINE
      elif snapType == QadSnapTypeEnum.PAR:
         return QadVertexmarkerIconTypeEnum.PARALLEL
      elif snapType == QadSnapTypeEnum.PR:
         return QadVertexmarkerIconTypeEnum.PROGRESS
      elif snapType == QadSnapTypeEnum.EXT_INT:
         return QadVertexmarkerIconTypeEnum.X_INFINITY_LINE
      elif snapType == QadSnapTypeEnum.PER_DEF:
         return QadVertexmarkerIconTypeEnum.PERP_DEFERRED
      elif snapType == QadSnapTypeEnum.TAN_DEF:
         return QadVertexmarkerIconTypeEnum.TANGENT_DEFERRED      
      else:
         return QadVertexmarkerIconTypeEnum.NONE      
      
      
   def hide(self):
      """
      Nasconde i marcatori precedentemente visualizzati
      """
      for vertexMarker in self.__vertexMarkers:
         vertexMarker.hide()
      
      for lineMarker in self.__lineMarkers:
         lineMarker.hide()

         
   def show(self, SnapPoints, \
            extLines = None, extArcs = None, \
            parLines = None, \
            intExtLine = None, intExtArc = None, \
            oSnapPointsForPolar = None, \
            oSnapLinesForPolar = None):
      """
      Visualizza i punti di snap, riceve un dizionario di liste di punti di snap
      suddivisi per tipi di snap (es. {END : [pt1 .. ptn] MID : [pt1 .. ptn]})
      e
      lista delle linee da estendere (ogni elemento é una lista di 2 punti = linea) per la modalità di snap EXT
      lista degli archi da estendere (ogni elemento é un arco) per la modalità di snap EXT
      lista delle linee per modo parallelo (ogni elemento é una lista di 2 punti = linea) per la modalità di snap PAR
      linea per intersezione su estensione (lista di 2 punti = linea) per la modalità di snap EXT_INT
      arco per intersezione su estensione per la modalità di snap EXT_INT
      """
      self.hide()

      # svuoto la lista dei marker
      for vertexMarker in self.__vertexMarkers:
         vertexMarker.removeItem()
      del self.__vertexMarkers[:]
      
      # svuoto la linea di estensione
      for lineMarker in self.__lineMarkers:
         self.__mapCanvas.scene().removeItem(lineMarker)
      del self.__lineMarkers[:]

      autoSnap = QadVariables.get(QadMsg.translate("Environment variables", "AUTOSNAP"))

      self.__mapCanvas.setToolTip("")
      
      # punti di snap
      for snapPoint in SnapPoints.items():
         snapType = snapPoint[0]
         i = -1
         for point in snapPoint[1]:
            i = i + 1
            
            if autoSnap & QadAUTOSNAPEnum.DISPLAY_MARK: # Turns on the AutoSnap mark
               # disegno il marcatore di snap
               self.__vertexMarkers.append(self.getVertexMarker(snapType, point))

            if autoSnap & QadAUTOSNAPEnum.DISPLAY_TOOLTIPS: # Turns on the AutoSnap tooltips
               # lo tengo perchè mi può servire
               # trasformo point da map coordinate in global coordinate
               # item = QadVertexMarker(self.__mapCanvas)
               # newPt = item.toCanvasCoordinates(point)
               # item.removeItem()
               # del item
               # pt = self.__mapCanvas.mapToGlobal(QPoint(newPt.x(), newPt.y()))
               # QToolTip.showText(pt, "testo di prova")
               self.__mapCanvas.setToolTip(snapTypeEnum2str(snapType))

            # linee di estensione
            if snapType == QadSnapTypeEnum.EXT and (extLines is not None):
               for extLine in extLines:
                  dummyPt = qad_utils.getPerpendicularPointOnInfinityLine(extLine[0], extLine[1], point)
                  # se dummyPt e point sono così vicini da essere considerati uguali
                  if qad_utils.ptNear(point, dummyPt):
                     # prendo il vertice più vicino a point
                     if qad_utils.getDistance(point, extLine[0]) < qad_utils.getDistance(point, extLine[1]):
                        dummyPt = extLine[0]
                     else:
                        dummyPt = extLine[1]
                                             
                     # per un baco non ancora capito: se la linea ha solo 2 vertici e 
                     # hanno la stessa x o y (linea orizzontale o verticale) 
                     # la linea non viene disegnata perciò sposto un pochino la x o la y         
                     dummyPt = qad_utils.getAdjustedRubberBandVertex(point, dummyPt)                     
                     # disegno la linea di estensione
                     self.__lineMarkers.append(self.getLineMarker(point, dummyPt))
                     
            # archi di estensione
            if snapType == QadSnapTypeEnum.EXT and (extArcs is not None):
               for extArc in extArcs:
                  angle = qad_utils.getAngleBy2Pts(extArc.center, point)
                  arc = QadArc(extArc)
                  
                  if qad_utils.getDistance(point, arc.getStartPt()) > \
                     qad_utils.getDistance(point, arc.getEndPt()):
                     arc.endAngle = angle
                  else:
                     arc.startAngle = angle
                        
                  # disegno l'arco di estensione
                  arcMarker = self.getArcMarker(arc)
                  if arcMarker is not None:
                     self.__lineMarkers.append(arcMarker)                     
            
            # linee di parallelismo
            if snapType == QadSnapTypeEnum.PAR and (self.__startPoint is not None):
               boundBox = self.__mapCanvas.extent()
               xMin = boundBox.xMinimum()
               yMin = boundBox.yMinimum()
               xMax = boundBox.xMaximum()
               yMax = boundBox.yMaximum()

               upperIntersX = qad_utils.getXOnInfinityLine(self.__startPoint, point, yMax)
               if upperIntersX > xMax or upperIntersX < xMin:
                  upperIntersX = None
                                                           
               lowerIntersX = qad_utils.getXOnInfinityLine(self.__startPoint, point, yMin)
               if lowerIntersX > xMax or lowerIntersX < xMin:
                  lowerIntersX = None
                  
               leftIntersY  = qad_utils.getYOnInfinityLine(self.__startPoint, point, xMin)
               if leftIntersY > yMax or leftIntersY < yMin:
                  leftIntersY = None

               rightIntersY = qad_utils.getYOnInfinityLine(self.__startPoint, point, xMax)
               if rightIntersY > yMax or rightIntersY < yMin:
                  rightIntersY = None

               p1 = None
               p2 = None
               
               if upperIntersX is not None:
                  p1 = QgsPoint(upperIntersX, yMax)
                  
               if leftIntersY is not None:
                  if leftIntersY != yMax:
                     if p1 is None:
                        p1 = QgsPoint(xMin, leftIntersY)
                     else:       
                        p2 = QgsPoint(xMin, leftIntersY)   
                                          
               if lowerIntersX is not None:
                  if lowerIntersX != xMin:
                     if p1 is None:
                        p1 = QgsPoint(lowerIntersX, yMin)
                     elif p2 is None:                  
                        p2 = QgsPoint(lowerIntersX, yMin)   

               if rightIntersY is not None:
                  if rightIntersY != yMin:
                     if p2 is None:
                        p2 = QgsPoint(xMax, rightIntersY)

               if (p1 is not None) and (p2 is not None):                    
                  # per un baco non ancora capito: se la linea ha solo 2 vertici e 
                  # hanno la stessa x o y (linea orizzontale o verticale) 
                  # la linea non viene disegnata perciò sposto un pochino la x o la y         
                  p2 = qad_utils.getAdjustedRubberBandVertex(p1, p2)                                          
                  # disegno la linea parallela
                  self.__lineMarkers.append(self.getLineMarker(p1, p2))                  

      # linee per il puntamento polare
      if oSnapLinesForPolar is not None:
         for line in oSnapLinesForPolar:
            lineMarker = self.getLineMarkerForPolar(line[0], line[1])
            if lineMarker is not None:
               # disegno la linea
               self.__lineMarkers.append(lineMarker)

      # punti medi delle linee marcate come da estendere
      if extLines is not None:
         for extLine in extLines:
            point = qad_utils.getMiddlePoint(extLine[0], extLine[1])
            # disegno il marcatore di estensionel            
            self.__vertexMarkers.append(self.getVertexMarker(QadSnapTypeEnum.EXT, point))

      # punti medi degli archi marcati come da estendere
      if extArcs is not None:
         for extArc in extArcs:
            point = extArc.getMiddlePt()
            # disegno il marcatore di estensione    
            self.__vertexMarkers.append(self.getVertexMarker(QadSnapTypeEnum.EXT, point))

      # punti medi delle linee marcate come parallele
      if parLines is not None:
         for parLine in parLines:
            point = qad_utils.getMiddlePoint(parLine[0], parLine[1])
            # disegno il marcatore di parallelo    
            self.__vertexMarkers.append(self.getVertexMarker(QadSnapTypeEnum.PAR, point))

      # punto medio della linea marcata come intersezione estesa
      if intExtLine is not None and len(intExtLine) > 1:
         point = qad_utils.getMiddlePoint(intExtLine[0], intExtLine[1])
         # disegno il marcatore
         self.__vertexMarkers.append(self.getVertexMarker(QadSnapTypeEnum.EXT_INT, point))
         
      # punto medio dell'arco marcato come intersezione estesa      
      if intExtArc is not None and len(intExtArc) == 1:
         point = intExtArc[0].getMiddlePt()
         # disegno il marcatore
         self.__vertexMarkers.append(self.getVertexMarker(QadSnapTypeEnum.EXT_INT, point))
      
      # punti di osnap usati per l'opzione polare
      if oSnapPointsForPolar is not None:
         for snapPoint in oSnapPointsForPolar.items():
            snapType = snapPoint[0]
            for item in snapPoint[1]:
               # disegno il marcatore di snap
               self.__vertexMarkers.append(self.getVertexMarker(snapType, item))

            
   def getVertexMarker(self, snapType, point):
      """
      Crea un marcatore puntuale
      """
      vertexMarker = QadVertexMarker(self.__mapCanvas)
      vertexMarker.setIconSize(self.__iconSize)
      vertexMarker.setColor(self.__color)
      vertexMarker.setPenWidth(self.__penWidth)              
      vertexMarker.setIconType(self.__getIconType(snapType))              
      vertexMarker.setCenter(point)
      return vertexMarker


   def getLineMarker(self, pt1, pt2):
      """
      Crea un marcatore lineare
      """
      lineMarker = createRubberBand(self.__mapCanvas, QGis.Line, True)
      lineMarker.setColor(self.__color)
      lineMarker.setLineStyle(Qt.DashLine)
      lineMarker.addPoint(pt1, False)
      lineMarker.addPoint(pt2, True)      
      return lineMarker


   def getLineMarkerForPolar(self, startPoint, point):
      """
      Crea un marcatore lineare per il puntamento polare
      """
      boundBox = self.__mapCanvas.extent()
      xMin = boundBox.xMinimum()
      yMin = boundBox.yMinimum()
      xMax = boundBox.xMaximum()
      yMax = boundBox.yMaximum()

      p1 = startPoint
      p2 = point
               
      x2 = None
      if p2.y() > p1.y(): # semiretta che va verso l'alto
         x2 = qad_utils.getXOnInfinityLine(p1, p2, yMax)
      elif p2.y() < p1.y(): # semiretta che va verso il basso
         x2 = qad_utils.getXOnInfinityLine(p1, p2, yMin)                  
      else: # semiretta retta orizzontale
         if p2.x() > p1.x(): # semiretta che va verso destra
            x2 = xMax
         elif p2.x() < p1.x(): # semiretta che va verso sinistra
            x2 = xMin

      y2 = None
      if p2.x() > p1.x(): # semiretta che va verso destra
         y2 = qad_utils.getYOnInfinityLine(p1, p2, xMax)
      elif p2.x() < p1.x(): # semiretta che va verso sinistra
         y2 = qad_utils.getYOnInfinityLine(p1, p2, xMin)                  
      else: # semiretta retta verticale
         if p2.y() > p1.y(): # semiretta che va verso l'alto
            y2 = yMax
         elif p2.y() < p1.y(): # semiretta che va verso il basso
            y2 = yMin

      if x2 is not None:
         if x2 > xMax:
            x2 = xMax
         elif x2 < xMin:
            x2 = xMin
      
      if y2 is not None:
         if y2 > yMax:
            y2 = yMax
         elif y2 < yMin:
            y2 = yMin
                                                                             
      if (x2 is not None) and (y2 is not None):
         p2 = QgsPoint(x2, y2)                     
         # per un baco non ancora capito: se la linea ha solo 2 vertici e 
         # hanno la stessa x o y (linea orizzontale o verticale) 
         # la linea non viene disegnata perciò sposto un pochino la x o la y         
         p2 = qad_utils.getAdjustedRubberBandVertex(p1, p2)                                          
         # disegno la linea
         return self.getLineMarker(p1, p2)
      else:
         return None


   def getArcMarker(self, arc):
      """
      Crea un marcatore lineare x arco
      """
      lineMarker = createRubberBand(self.__mapCanvas, QGis.Line, True)
      lineMarker.setColor(self.__color)
      lineMarker.setLineStyle(Qt.DotLine)
      points = arc.asPolyline()
      if points is None:
         return None
      tot = len(points)
      i = 0
      while i < (tot - 1):
         lineMarker.addPoint(points[i], False)
         i = i + 1
      lineMarker.addPoint(points[i], True)
      return lineMarker

      