# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QAD Quantum Aided Design plugin

 classe per gestire il map tool in ambito del comando pline
 
                              -------------------
        begin                : 2016-04-07
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
import math


import qad_utils
from qad_snapper import *
from qad_variables import *
from qad_getpoint import *
from qad_rubberband import QadRubberBand


#===============================================================================
# Qad_pline_maptool_ModeEnum class.
#===============================================================================
class Qad_pline_maptool_ModeEnum():
   # non si richiede niente
   NONE = 0
   # si richiede il punto finale per ricalcare un oggetto esistente 
   ASK_FOR_TRACE_PT = 1
   # si deve tracciare una linea 
   DRAW_LINE = 2


#===============================================================================
# Qad_pline_maptool class
#===============================================================================
class Qad_pline_maptool(QadGetPoint):
    
   def __init__(self, plugIn, asToolForMPolygon = False):
      QadGetPoint.__init__(self, plugIn)

      self.firstPt = None
      self.mode = None

      self.asToolForMPolygon = asToolForMPolygon # se True significa che è usato per disegnare un poligono
      if self.asToolForMPolygon:
         self.__polygonRubberBand = QadRubberBand(self.plugIn.canvas, True)
         self.endVertex = None # punta al vertice iniziale e finale del poligono di QadPLINECommandClass

   def hidePointMapToolMarkers(self):
      QadGetPoint.hidePointMapToolMarkers(self)
      if self.asToolForMPolygon: self.__polygonRubberBand.hide()

   def showPointMapToolMarkers(self):
      QadGetPoint.showPointMapToolMarkers(self)
      if self.asToolForMPolygon: self.__polygonRubberBand.show()
                             
   def clear(self):
      QadGetPoint.clear(self)
      if self.asToolForMPolygon: self.__polygonRubberBand.reset()
      self.mode = None
   
   def canvasMoveEvent(self, event):
      QadGetPoint.canvasMoveEvent(self, event)

      if self.asToolForMPolygon == True: # se True significa che è usato per disegnare un poligono
         self.__polygonRubberBand.reset()
      
         startPoint = self.getStartPoint()
         if startPoint is None: return
         
         points = None           
          
         # si richiede il punto finale per ricalcare un oggetto esistente
         if self.mode == Qad_pline_maptool_ModeEnum.ASK_FOR_TRACE_PT:
            if self.tmpEntity.isInitialized():
               # trasformo la geometria nel crs del canvas per lavorare con coordinate piane xy
               geom = self.layerToMapCoordinates(self.tmpEntity.layer, self.tmpEntity.getGeometry())
               ptEnd = qad_utils.closestVertexPtWithContext(self.tmpPoint, geom)
               # leggo la parte di linea tra self.firstPt e ptEnd
               points = qad_utils.getLinePart(geom, startPoint, ptEnd)
         else:
            points = [startPoint, self.tmpPoint]
         
         if (points is not None) and (self.endVertex is not None) and (startPoint != self.endVertex):
            points.insert(0, self.endVertex)
            self.__polygonRubberBand.setPolygon(points)
         
         del startPoint

    
   def activate(self):
      QadGetPoint.activate(self)
      if self.asToolForMPolygon: self.__polygonRubberBand.show()

   def deactivate(self):
      try: # necessario perché se si chiude QGIS parte questo evento nonostante non ci sia più l'oggetto maptool !
         QadGetPoint.deactivate(self)
         if self.asToolForMPolygon: self.__polygonRubberBand.hide()
      except:
         pass

   def setMode(self, mode):
      self.mode = mode
            
      # si richiede il punto finale per ricalcare un oggetto esistente
      if self.mode == Qad_pline_maptool_ModeEnum.ASK_FOR_TRACE_PT:
         self.checkPointLayer = False # scarto la selezione di punti
         self.checkLineLayer = True
         self.checkPolygonLayer = True
         self.onlyEditableLayers = False
         self.forceSnapTypeOnce(QadSnapTypeEnum.END)

         self.setSelectionMode(QadGetPointSelectionModeEnum.ENTITY_SELECTION_DYNAMIC)
         self.setDrawMode(QadGetPointDrawModeEnum.NONE)
      # non si richiede niente
      elif self.mode == Qad_pline_maptool_ModeEnum.NONE:
         self.setSelectionMode(QadGetPointSelectionModeEnum.NONE)
         self.setDrawMode(QadGetPointDrawModeEnum.NONE)
      # si deve tracciare una linea
      elif self.mode == Qad_pline_maptool_ModeEnum.DRAW_LINE:
         self.setSelectionMode(QadGetPointSelectionModeEnum.POINT_SELECTION)
         self.setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE) # imposto la linea elastica
