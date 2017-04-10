# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QAD Quantum Aided Design plugin

 Gestione dei colori dei grip di QAD
 
                              -------------------
        begin                : 2016-17-02
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
from qgis.core import QgsApplication
from qgis.utils import *
from qgis.gui import *


import qad_gripcolor_ui


from qad_variables import *
from qad_msg import QadMsg, qadShowPluginHelp
import qad_utils


#######################################################################################
# Classe che gestisce l'interfaccia grafica per i colori dei grip
class QadGripColorDialog(QDialog, QObject, qad_gripcolor_ui.Ui_GripColor_Dialog):
   def __init__(self, plugIn, parent, gripColor, gripHot, gripHover, gripContour):
      self.plugIn = plugIn
      self.iface = self.plugIn.iface#.mainWindow()

      QDialog.__init__(self, parent)

      self.gripColor   = gripColor
      self.gripHot     = gripHot
      self.gripHover   = gripHover
      self.gripContour = gripContour
      
      self.setupUi(self)
      
      # Inizializzazione dei colori
      self.init_colors()


   def setupUi(self, Dialog):
      qad_gripcolor_ui.Ui_GripColor_Dialog.setupUi(self, self)
      # aggiungo il bottone di qgis QgsColorButtonV2 chiamato unselectedGripColor 
      # che eredita la posizione di unselectedGripColorDummy (che viene nascosto)
      self.unselectedGripColorDummy.setHidden(True)
      self.unselectedGripColor = QgsColorButtonV2(self.unselectedGripColorDummy.parent())
      self.unselectedGripColor.setGeometry(self.unselectedGripColorDummy.geometry())
      self.unselectedGripColor.setObjectName("unselectedGripColor")
      # aggiungo il bottone di qgis QgsColorButtonV2 chiamato selectedGripColor 
      # che eredita la posizione di selectedGripColorDummy (che viene nascosto)
      self.selectedGripColorDummy.setHidden(True)
      self.selectedGripColor = QgsColorButtonV2(self.selectedGripColorDummy.parent())
      self.selectedGripColor.setGeometry(self.selectedGripColorDummy.geometry())
      self.selectedGripColor.setObjectName("selectedGripColor")
      # aggiungo il bottone di qgis QgsColorButtonV2 chiamato hoverGripColor 
      # che eredita la posizione di hoverGripColorDummy (che viene nascosto)
      self.hoverGripColorDummy.setHidden(True)
      self.hoverGripColor = QgsColorButtonV2(self.hoverGripColorDummy.parent())      
      self.hoverGripColor.setGeometry(self.hoverGripColorDummy.geometry())
      self.hoverGripColor.setObjectName("hoverGripColor")
      # aggiungo il bottone di qgis QgsColorButtonV2 chiamato contourGripColor 
      # che eredita la posizione di contourGripColorDummy (che viene nascosto)
      self.contourGripColorDummy.setHidden(True)
      self.contourGripColor = QgsColorButtonV2(self.contourGripColorDummy.parent())
      self.contourGripColor.setGeometry(self.contourGripColorDummy.geometry())
      self.contourGripColor.setObjectName("contourGripColor")


   #============================================================================
   # init_colors
   #============================================================================
   def init_colors(self):
      # Inizializzazione dei colori
      self.unselectedGripColor.setColor(QColor(self.gripColor))
      self.selectedGripColor.setColor(QColor(self.gripHot))
      self.hoverGripColor.setColor(QColor(self.gripHover))
      self.contourGripColor.setColor(QColor(self.gripContour))
  

   def ButtonBOX_Accepted(self):
      self.gripColor = self.unselectedGripColor.color().name()
      self.gripHot = self.selectedGripColor.color().name()
      self.gripHover = self.hoverGripColor.color().name()
      self.gripContour = self.contourGripColor.color().name()

      QDialog.accept(self)


   def ButtonHELP_Pressed(self):
      qadShowPluginHelp(QadMsg.translate("Help", ""))
