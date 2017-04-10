# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QAD Quantum Aided Design plugin

 comando COPY per copiare oggetti
 
                              -------------------
        begin                : 2013-10-02
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


# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


from qad_copy_maptool import *
from qad_generic_cmd import QadCommandClass
from qad_msg import QadMsg
from qad_getpoint import *
from qad_textwindow import *
from qad_ssget_cmd import QadSSGetClass
from qad_entity import *
from qad_variables import *
import qad_utils
import qad_layer
from qad_dim import *


# Classe che gestisce il comando COPY
class QadCOPYCommandClass(QadCommandClass):

   def instantiateNewCmd(self):
      """ istanzia un nuovo comando dello stesso tipo """
      return QadCOPYCommandClass(self.plugIn)
   
   def getName(self):
      return QadMsg.translate("Command_list", "COPY")

   def getEnglishName(self):
      return "COPY"

   def connectQAction(self, action):
      QObject.connect(action, SIGNAL("triggered()"), self.plugIn.runCOPYCommand)

   def getIcon(self):
      return QIcon(":/plugins/qad/icons/copyEnt.png")

   def getNote(self):
      # impostare le note esplicative del comando
      return QadMsg.translate("Command_COPY", "Copies selected objects a specified distance in a specified direction.")
   
   def __init__(self, plugIn):
      QadCommandClass.__init__(self, plugIn)
      self.SSGetClass = QadSSGetClass(plugIn)
      self.SSGetClass.onlyEditableLayers = True
      self.entitySet = QadEntitySet()
      self.basePt = QgsPoint()
      self.series = False
      self.seriesLen = 2
      self.adjust = False
      self.copyMode = QadVariables.get(QadMsg.translate("Environment variables", "COPYMODE"))
      
      self.featureCache = [] # lista di (layer, feature)
      self.nOperationsToUndo = 0

   def __del__(self):
      QadCommandClass.__del__(self)
      del self.SSGetClass
      
   def getPointMapTool(self, drawMode = QadGetPointDrawModeEnum.NONE):
      if self.step == 0: # quando si é in fase di selezione entità
         return self.SSGetClass.getPointMapTool()
      else:
         if (self.plugIn is not None):
            if self.PointMapTool is None:
               self.PointMapTool = Qad_copy_maptool(self.plugIn)
            return self.PointMapTool
         else:
            return None


   #============================================================================
   # move
   #============================================================================
   def move(self, f, offSetX, offSetY, layerEntitySet, entitySet, dimEntity):
      if dimEntity is None:
         # sposto la feature e la rimuovo da entitySet (é la prima)
         f.setGeometry(qad_utils.moveQgsGeometry(f.geometry(), offSetX, offSetY))
         # plugIn, layer, feature, coordTransform, refresh, check_validity
         if qad_layer.addFeatureToLayer(self.plugIn, layerEntitySet.layer, f, None, False, False) == False:  
            return False
      else:
         newDimEntity = QadDimEntity(dimEntity) # la copio
         # sposto la quota
         newDimEntity.move(offSetX, offSetY)
         if newDimEntity.addToLayers(self.plugIn) == False:
            return False             
            
      return True


   #============================================================================
   # copyGeoms
   #============================================================================
   def copyGeoms(self, newPt):
      # copio entitySet
      entitySet = QadEntitySet(self.entitySet)
      
      self.plugIn.beginEditCommand("Feature copied", entitySet.getLayerList())

      for layerEntitySet in entitySet.layerEntitySetList:
         layer = layerEntitySet.layer
         
         transformedBasePt = self.mapToLayerCoordinates(layer, self.basePt)
         transformedNewPt = self.mapToLayerCoordinates(layer, newPt)
         offSetX = transformedNewPt.x() - transformedBasePt.x()
         offSetY = transformedNewPt.y() - transformedBasePt.y()
         
         while len(layerEntitySet.featureIds) > 0:
            featureId = layerEntitySet.featureIds[0]
            f = layerEntitySet.getFeature(featureId)
            if f is None:
               del layerEntitySet.featureIds[0]
               continue

            # verifico se l'entità appartiene ad uno stile di quotatura
            dimEntity = QadDimStyles.getDimEntity(layerEntitySet.layer, f.id())
            
            if self.series and self.seriesLen > 0: # devo fare una serie
               if self.adjust == True:
                  offSetX = offSetX / (self.seriesLen - 1)
                  offSetY = offSetY / (self.seriesLen - 1)
   
               deltaX = offSetX
               deltaY = offSetY
                              
               for i in xrange(1, self.seriesLen, 1):
                  if self.move(f, deltaX, deltaY, layerEntitySet, entitySet, dimEntity) == False:
                     self.plugIn.destroyEditCommand()
                     return
                  deltaX = deltaX + offSetX
                  deltaY = deltaY + offSetY
            else:
               if self.move(f, offSetX, offSetY, layerEntitySet, entitySet, dimEntity) == False:
                  self.plugIn.destroyEditCommand()
                  return
               
            # la rimuovo da entitySet
            if dimEntity is None:
               del layerEntitySet.featureIds[0]
            else:
               dimEntitySet = dimEntity.getEntitySet()
               entitySet.subtract(dimEntitySet)
               
      self.plugIn.endEditCommand()
      self.nOperationsToUndo = self.nOperationsToUndo + 1


   #============================================================================
   # waitForBasePt
   #============================================================================
   def waitForBasePt(self):
      # imposto il map tool
      self.getPointMapTool().setMode(Qad_copy_maptool_ModeEnum.NONE_KNOWN_ASK_FOR_BASE_PT)                                

      if self.copyMode == 0: # Imposta il comando COPIA in modo che venga ripetuto automaticamente
         keyWords = QadMsg.translate("Command_COPY", "Displacement") + "/" + \
                    QadMsg.translate("Command_COPY", "mOde")
         englishKeyWords = "Displacement" + "/" + "mOde"
                    
      else:
         # l'opzione Multiple viene tradotta in italiano in "MUltiplo" nel contesto "waitForBasePt"
         # l'opzione Multiple viene tradotta in italiano in "Multipla" nel contesto "waitForMode"
         # e "Multipla" nel caso di modalità di copia
         keyWords = QadMsg.translate("Command_COPY", "Displacement") + "/" + \
                    QadMsg.translate("Command_COPY", "mOde") + "/" + \
                    QadMsg.translate("Command_COPY", "Multiple", "waitForBasePt")
         englishKeyWords = "Displacement" + "/" + "mOde" + "/" + "Multiple"

      default = QadMsg.translate("Command_COPY", "Displacement")                   
      prompt = QadMsg.translate("Command_COPY", "Specify base point or [{0}] <{1}>: ").format(keyWords, default)
      
      keyWords += "_" + englishKeyWords
      # si appresta ad attendere un punto o enter o una parola chiave         
      # msg, inputType, default, keyWords, nessun controllo
      self.waitFor(prompt, \
                   QadInputTypeEnum.POINT2D | QadInputTypeEnum.KEYWORDS, \
                   default, \
                   keyWords, QadInputModeEnum.NONE)      
      self.step = 2      
   
   #============================================================================
   # waitForSeries
   #============================================================================
   def waitForSeries(self):
      # si appresta ad attendere un numero intero
      msg = QadMsg.translate("Command_COPY", "Number of Items to Array <{0}>: ")
      # msg, inputType, default, keyWords, valori positivi
      self.waitFor(msg.format(str(self.seriesLen)), \
                   QadInputTypeEnum.INT, \
                   self.seriesLen, \
                   "", \
                   QadInputModeEnum.NOT_ZERO | QadInputModeEnum.NOT_NEGATIVE)                                      
      self.step = 6        
      
   #============================================================================
   # waitForSecondPt
   #============================================================================
   def waitForSecondPt(self):
      self.series = False
      self.adjust = False
      self.getPointMapTool().seriesLen = 0
      self.getPointMapTool().setMode(Qad_copy_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_COPY_PT)
                                      
      if len(self.featureCache) > 0:
         keyWords = QadMsg.translate("Command_COPY", "Array") + "/" + \
                    QadMsg.translate("Command_COPY", "Exit") + "/" + \
                    QadMsg.translate("Command_COPY", "Undo")
         default = QadMsg.translate("Command_COPY", "Exit")
         prompt = QadMsg.translate("Command_COPY", "Specify second point or [{0}] <{1}>: ").format(keyWords, default)
   
         englishKeyWords = "Array" + "/" + "Exit" + "/" + "Undo" + "/" + "Exit"
         keyWords += "_" + englishKeyWords
         # si appresta ad attendere un punto o enter o una parola chiave         
         # msg, inputType, default, keyWords, nessun controllo
         self.waitFor(prompt, \
                      QadInputTypeEnum.POINT2D | QadInputTypeEnum.KEYWORDS, \
                      default, \
                      keyWords, QadInputModeEnum.NONE)
      else:
         keyWords = QadMsg.translate("Command_COPY", "Array")
         prompt = QadMsg.translate("Command_COPY", "Specify second point or [{0}] <use first point as displacement from origin point 0,0>: ").format(keyWords)
                   
         englishKeyWords = "Array"
         keyWords += "_" + englishKeyWords
         # si appresta ad attendere un punto o enter o una parola chiave         
         # msg, inputType, default, keyWords, nessun controllo
         self.waitFor(prompt, \
                      QadInputTypeEnum.POINT2D | QadInputTypeEnum.KEYWORDS, \
                      None, \
                      keyWords, QadInputModeEnum.NONE)      
            
      self.step = 3           

   #============================================================================
   # waitForSecondPtBySeries
   #============================================================================
   def waitForSecondPtBySeries(self):
      if self.adjust == False:
         keyWords = QadMsg.translate("Command_COPY", "Fit")
         englishKeyWords = "Fit"        
      else:
         keyWords = QadMsg.translate("Command_COPY", "Array")
         englishKeyWords = "Array"        
      prompt = QadMsg.translate("Command_COPY", "Specify second point or [{0}]: ").format(keyWords)

      keyWords += "_" + englishKeyWords
      # si appresta ad attendere un punto o enter o una parola chiave         
      # msg, inputType, default, keyWords, valore nullo non permesso
      self.waitFor(prompt, \
                   QadInputTypeEnum.POINT2D | QadInputTypeEnum.KEYWORDS, \
                   "", \
                   keyWords, QadInputModeEnum.NOT_NULL)      
      self.step = 7

   #============================================================================
   # run
   #============================================================================
   def run(self, msgMapTool = False, msg = None):
      if self.plugIn.canvas.mapSettings().destinationCrs().geographicFlag():
         self.showMsg(QadMsg.translate("QAD", "\nThe coordinate reference system of the project must be a projected coordinate system.\n"))
         return True # fine comando
            
      #=========================================================================
      # RICHIESTA SELEZIONE OGGETTI
      if self.step == 0: # inizio del comando
         if self.SSGetClass.run(msgMapTool, msg) == True:
            # selezione terminata
            self.step = 1
            return self.run(msgMapTool, msg)
      
      #=========================================================================
      # COPIA OGGETTI
      elif self.step == 1:
         self.entitySet.set(self.SSGetClass.entitySet)
         
         if self.entitySet.count() == 0:
            return True # fine comando

         CurrSettingsMsg = QadMsg.translate("QAD", "\nCurrent settings: ")
         if self.copyMode == 0: # 0 = multipla 
            CurrSettingsMsg = CurrSettingsMsg + QadMsg.translate("Command_COPY", "Copy mode = Multiple")         
         else: # 1 = singola
            CurrSettingsMsg = CurrSettingsMsg + QadMsg.translate("Command_COPY", "Copy mode = Single")         
         self.showMsg(CurrSettingsMsg)         

         self.getPointMapTool().entitySet.set(self.entitySet)
         self.waitForBasePt()
         self.getPointMapTool().refreshSnapType() # riagggiorno lo snapType che può essere variato dal maptool di selezione entità                    
         return False
         
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA PUNTO BASE (da step = 1)
      elif self.step == 2: # dopo aver atteso un punto o un numero reale si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  pass # opzione di default "spostamento"
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if value is None:
            value = QadMsg.translate("Command_COPY", "Displacement")

         if type(value) == unicode:
            if value == QadMsg.translate("Command_COPY", "Displacement") or value == "Displacement":
               self.basePt.set(0, 0)
               self.getPointMapTool().basePt = self.basePt
               self.getPointMapTool().setMode(Qad_copy_maptool_ModeEnum.BASE_PT_KNOWN_ASK_FOR_COPY_PT)                                
               # si appresta ad attendere un punto
               msg = QadMsg.translate("Command_COPY", "Specify the displacement from the origin point 0,0 <{0}, {1}>: ")
               # msg, inputType, default, keyWords, nessun controllo
               self.waitFor(msg.format(str(self.plugIn.lastOffsetPt.x()), str(self.plugIn.lastOffsetPt.y())), \
                            QadInputTypeEnum.POINT2D, \
                            self.plugIn.lastOffsetPt, \
                            "", QadInputModeEnum.NONE)                                      
               self.step = 4
            elif value == QadMsg.translate("Command_COPY", "mOde") or value == "mOde":
               # l'opzione Multiple viene tradotta in italiano in "Multipla" nel contesto "waitForMode"
               keyWords = QadMsg.translate("Command_COPY", "Single") + "/" + \
                          QadMsg.translate("Command_COPY", "Multiple", "waitForMode")
               englishKeyWords = "Single" + "/" + "Multiple"
                          
               if self.copyMode == 0: # Imposta il comando COPIA in modo che venga ripetuto automaticamente
                  # l'opzione Multiple viene tradotta in italiano in "Multipla" nel contesto "waitForMode"
                  default = QadMsg.translate("Command_COPY", "Multiple", "waitForMode")
               else:
                  default = QadMsg.translate("Command_COPY", "Single")               
               prompt = QadMsg.translate("Command_COPY", "Enter a copy mode option [{0}] <{1}>: ").format(keyWords, default)

               keyWords += "_" + englishKeyWords
               # si appresta ad attendere enter o una parola chiave         
               # msg, inputType, default, keyWords, nessun controllo
               self.waitFor(prompt, \
                            QadInputTypeEnum.KEYWORDS, \
                            default, \
                            keyWords, QadInputModeEnum.NONE)
               self.step = 5
            # l'opzione Multiple viene tradotta in italiano in "MUltiplo" nel contesto "waitForBasePt"
            elif value == QadMsg.translate("Command_COPY", "Multiple", "waitForBasePt") or value == "Multiple":
               self.copyMode = 0 # Imposta il comando COPIA in modo che venga ripetuto automaticamente
               self.waitForBasePt()                         
         elif type(value) == QgsPoint: # se é stato inserito il punto base
            self.basePt.set(value.x(), value.y())

            # imposto il map tool
            self.getPointMapTool().basePt = self.basePt           
            self.waitForSecondPt()
         
         return False 
         
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA SECONDO PUNTO PER COPIA (da step = 2)
      elif self.step == 3: # dopo aver atteso un punto o un numero reale si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  if len(self.featureCache) > 0:
                     value = QadMsg.translate("Command_COPY", "Exit")
                  else:
                     value = None
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False
            else:
               value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if value is None:
            if len(self.featureCache) > 0:
               value = QadMsg.translate("Command_COPY", "Exit")
            else:               
               # utilizzare il primo punto come spostamento
               value = QgsPoint(self.basePt)
               self.basePt.set(0, 0)
               self.copyGeoms(value)
               return True # fine comando
         
         if type(value) == unicode:
            if value == QadMsg.translate("Command_COPY", "Array") or value == "Array":
               self.waitForSeries()               
            elif value == QadMsg.translate("Command_COPY", "Exit") or value == "Exit":
               return True # fine comando
            elif value == QadMsg.translate("Command_COPY", "Undo") or value == "Undo":
               if self.nOperationsToUndo > 0: 
                  self.nOperationsToUndo = self.nOperationsToUndo - 1
                  self.plugIn.undoEditCommand()
               else:
                  self.showMsg(QadMsg.translate("QAD", "\nThe command has been canceled."))                  
               self.waitForSecondPt()
         elif type(value) == QgsPoint: # se é stato inserito lo spostamento con un punto
            self.copyGeoms(value)
            if self.copyMode == 1: # "Singola" 
               return True # fine comando
            self.waitForSecondPt()
         
         return False
               
      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DEL PUNTO DI SPOSTAMENTO (da step = 2)
      elif self.step == 4: # dopo aver atteso un punto o un numero reale si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         self.plugIn.setLastOffsetPt(value)
         self.copyGeoms(value)
         return True # fine comando


      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DELLA MODALITA' (SINGOLA / MULTIPLA) (da step = 2)
      elif self.step == 5: # dopo aver atteso un punto o un numero reale si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # la parola chiave arriva come parametro della funzione
            value = msg

         if type(value) == unicode:
            if value == QadMsg.translate("Command_COPY", "Single") or value == "Single":
               self.copyMode = 1
               QadVariables.set(QadMsg.translate("Environment variables", "COPYMODE"), 1)
               QadVariables.save()
            # l'opzione Multiple viene tradotta in italiano in "Multipla" nel contesto "waitForMode"
            elif value == QadMsg.translate("Command_COPY", "Multiple", "waitForMode") or value == "Multiple":
               self.copyMode = 0
               QadVariables.set(QadMsg.translate("Environment variables", "COPYMODE"), 0)
               QadVariables.save()
            
         self.waitForBasePt()
         return False

      #=========================================================================
      # RISPOSTA ALLA RICHIESTA DELLA SERIE (da step = 3)
      elif self.step == 6: # dopo aver atteso un numero intero si riavvia il comando
         if msgMapTool == True: # il punto arriva da una selezione grafica
            if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
               value = self.seriesLen
            else:
               value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if value < 2:
            self.showMsg(QadMsg.translate("Command_COPY", "\nThe value must be between 2 and 32767."))
            self.waitForSeries()
         else:
            self.series = True
            self.seriesLen = value
            self.getPointMapTool().seriesLen = self.seriesLen

            self.waitForSecondPtBySeries()
            
         return False

      #=========================================================================
      # RISPOSTA ALLA RICHIESTA SECONDO PUNTO PER COPIA DA SERIE (da step = 6)
      elif self.step == 7: # dopo aver atteso un punto o una parola chiave
         if msgMapTool == True: # il punto arriva da una selezione grafica
            # la condizione seguente si verifica se durante la selezione di un punto
            # é stato attivato un altro plugin che ha disattivato Qad
            # quindi stato riattivato il comando che torna qui senza che il maptool
            # abbia selezionato un punto            
            if self.getPointMapTool().point is None: # il maptool é stato attivato senza un punto
               if self.getPointMapTool().rightButton == True: # se usato il tasto destro del mouse
                  return True # fine comando
               else:
                  self.setMapTool(self.getPointMapTool()) # riattivo il maptool
                  return False

            value = self.getPointMapTool().point
         else: # il punto arriva come parametro della funzione
            value = msg

         if type(value) == unicode:
            if value == QadMsg.translate("Command_COPY", "Array") or value == "Array":
               self.adjust = False
               self.getPointMapTool().adjust = self.adjust
               self.waitForSecondPtBySeries()
            elif value == QadMsg.translate("Command_COPY", "Fit") or value == "Fit":
               self.adjust = True
               self.getPointMapTool().adjust = self.adjust
               self.waitForSecondPtBySeries()
         elif type(value) == QgsPoint: # se é stato inserito lo spostamento con un punto
            self.copyGeoms(value)
            if self.copyMode == 1: # "Singola" 
               return True # fine comando            
            self.waitForSecondPt()
          
         return False