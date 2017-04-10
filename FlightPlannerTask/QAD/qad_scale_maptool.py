# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QAD Quantum Aided Design plugin

 classe per gestire il map tool in ambito del comando scale
 
                              -------------------
        begin                : 2013-09-27
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
from qad_snappointsdisplaymanager import *
from qad_variables import *
from qad_getpoint import *
from qad_dim import *
from qad_highlight import QadHighlight


#===============================================================================
# Qad_scale_maptool_ModeEnum class.
#===============================================================================
class Qad_scale_maptool_ModeEnum():
   # noto niente si richiede il punto base
   NONE_KNOWN_ASK_FOR_BASE_PT = 1     
   # noto il punto base si richiede il secondo punto per la scala
   BASE_PT_KNOWN_ASK_FOR_SCALE_PT = 2
   # si richiede il primo punto per la lunghezza di riferimento
   ASK_FOR_FIRST_PT_REFERENCE_LEN = 3     
   # noto il primo punto si richiede il secondo punto per la lunghezza di riferimento
   FIRST_PT_KNOWN_ASK_FOR_SECOND_PT_REFERENCE_LEN = 4     
   # noto il punto base si richiede il secondo punto per la nuova lunghezza
   BASE_PT_KNOWN_ASK_FOR_NEW_LEN_PT = 5
   # si richiede il primo punto per la nuova lunghezza
   ASK_FOR_FIRST_NEW_LEN_PT = 6
   # noto il primo punto si richiede il secondo punto per la nuova lunghezza
   FIRST_PT_KNOWN_ASK_FOR_SECOND_NEW_LEN_PT = 7     

#===============================================================================
# Qad_scale_maptool class
#===============================================================================
class Qad_scale_maptool(QadGetPoint):
    
   def __init__(self, plugIn):
      QadGetPoint.__init__(self, plugIn)
                        
      self.basePt = None
      self.Pt1ReferenceLen = None
      self.ReferenceLen = 0
      self.Pt1NewLen = None
      self.entitySet = QadEntitySet()
      self.__highlight = QadHighlight(self.canvas)

   def hidePointMapToolMarkers(self):
      QadGetPoint.hidePointMapToolMarkers(self)
      self.__highlight.hide()

   def showPointMapToolMarkers(self):
      QadGetPoint.showPointMapToolMarkers(self)
      self.__highlight.show()
                             
   def clear(self):
      QadGetPoint.clear(self)
      self.__highlight.reset()
      self.mode = None    


   #============================================================================
   # scale
   #============================================================================
   def scale(self, f, basePt, scale, layerEntitySet, entitySet):
      # verifico se l'entità appartiene ad uno stile di quotatura
      dimEntity = QadDimStyles.getDimEntity(layerEntitySet.layer, f.id())
           
      if dimEntity is None:
         # scalo la feature e la rimuovo da entitySet (é la prima)
         f.setGeometry(qad_utils.scaleQgsGeometry(f.geometry(), basePt, scale))
         self.__highlight.addGeometry(f.geometry(), layerEntitySet.layer)
         del layerEntitySet.featureIds[0]
      else:
         # scalo la quota e la rimuovo da entitySet
         dimEntitySet = dimEntity.getEntitySet()
         dimEntity.scale(basePt, scale)
         self.__highlight.addGeometry(dimEntity.textualFeature.geometry(), dimEntity.getTextualLayer())
         self.__highlight.addGeometries(dimEntity.getLinearGeometryCollection(), dimEntity.getLinearLayer())
         self.__highlight.addGeometries(dimEntity.getSymbolGeometryCollection(), dimEntity.getSymbolLayer())
         entitySet.subtract(dimEntitySet)

   
   #============================================================================
   # addScaledGeometries
   #============================================================================
   def addScaledGeometries(self, scale):
      self.__highlight.reset()
      
      # copio entitySet
      entitySet = QadEntitySet(self.entitySet)
      
      if scale <= 0:
         return
      
      for layerEntitySet in entitySet.layerEntitySetList:
         layer = layerEntitySet.layer

         transformedBasePt = self.canvas.mapSettings().mapToLayerCoordinates(layer, self.basePt)

         while len(layerEntitySet.featureIds) > 0:
            featureId = layerEntitySet.featureIds[0]
            f = layerEntitySet.getFeature(featureId)        
            self.scale(f, transformedBasePt, scale, layerEntitySet, entitySet)
            
      
   def canvasMoveEvent(self, event):
      QadGetPoint.canvasMoveEvent(self, event)
                     
      # noto il punto base si richiede il secondo punto per la scala
      if self.mode == Qad_scale_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_SCALE_PT:
         scale = qad_utils.getDistance(self.basePt, self.tmpPoint)
         self.addScaledGeometries(scale)                           
      # noto il primo punto si richiede il secondo punto per la lunghezza di riferimento
      elif self.mode == Qad_scale_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_NEW_LEN_PT:
         len = qad_utils.getDistance(self.basePt, self.tmpPoint)
         scale = len / self.ReferenceLen
         self.addScaledGeometries(scale)                           
      # noto il primo punto si richiede il secondo punto per la nuova lunghezza
      elif self.mode == Qad_scale_maptool_ModeEnum.FIRST_PT_KNOWN_ASK_FOR_SECOND_NEW_LEN_PT:
         len = qad_utils.getDistance(self.Pt1NewLen, self.tmpPoint)
         scale = len / self.ReferenceLen
         self.addScaledGeometries(scale)                           
         
    
   def activate(self):
      QadGetPoint.activate(self)            
      self.__highlight.show()          

   def deactivate(self):
      try: # necessario perché se si chiude QGIS parte questo evento nonostante non ci sia più l'oggetto maptool !
         QadGetPoint.deactivate(self)
         self.__highlight.hide()
      except:
         pass

   def setMode(self, mode):
      self.mode = mode
      # noto niente si richiede il punto base
      if self.mode == Qad_scale_maptool_ModeEnum.NONE_KNOWN_ASK_FOR_BASE_PT:
         self.clear()
         self.setDrawMode(QadGetPointDrawModeEnum.NONE)
         self.__highlight.reset()
      # noto il punto base si richiede il secondo punto per la scala
      elif self.mode == Qad_scale_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_SCALE_PT:
         self.setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
         self.setStartPoint(self.basePt)
      # si richiede il primo punto per la lunghezza di riferimento
      elif self.mode == Qad_scale_maptool_ModeEnum.ASK_FOR_FIRST_PT_REFERENCE_LEN:
         self.setDrawMode(QadGetPointDrawModeEnum.NONE)
         self.__highlight.reset()
      # noto il primo punto si richiede il secondo punto per la lunghezza di riferimento
      elif self.mode == Qad_scale_maptool_ModeEnum.FIRST_PT_KNOWN_ASK_FOR_SECOND_PT_REFERENCE_LEN:
         self.setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
         self.setStartPoint(self.Pt1ReferenceLen)
      # noto il punto base si richiede il secondo punto per la nuova lunghezza
      elif self.mode == Qad_scale_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_NEW_LEN_PT:
         self.setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
         self.setStartPoint(self.basePt)
      # si richiede il primo punto per la nuova lunghezza
      elif self.mode == Qad_scale_maptool_ModeEnum.ASK_FOR_FIRST_NEW_LEN_PT:
         self.setDrawMode(QadGetPointDrawModeEnum.NONE)
         self.__highlight.reset()
      # noto il primo punto si richiede il secondo punto per la nuova lunghezza
      elif self.mode == Qad_scale_maptool_ModeEnum.FIRST_PT_KNOWN_ASK_FOR_SECOND_NEW_LEN_PT:
         self.setDrawMode(QadGetPointDrawModeEnum.ELASTIC_LINE)
         self.setStartPoint(self.Pt1NewLen)
