# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GridZoneGeneratorDialog
                                 A QGIS plugin
 This plugin creates UTM grid zones for a specific scaie
                             -------------------
        begin                : 2015-06-09
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

import os
from map_index import UtmGrid

from qgis.core import *
from qgis.gui import QgsGenericProjectionSelector
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, QThreadPool, Qt
from PyQt4.QtGui import QMessageBox, QFileDialog
from FlightPlanner.QgisHelper import QgisHelper
import define
print "FORM_CLASS"
# print os.path.join(os.path.dirname(__file__), 'grid_zone_generator_dialog_base.ui')
FORM_CLASS, _ = uic.loadUiType(define.appPath + "/grid_zone_generator_dialog_base.ui")

print "FORM_CLASS End"
class GridZoneGeneratorDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(GridZoneGeneratorDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface

        self.crsLineEdit.setReadOnly(True)
        
        self.utmgrid = UtmGrid()

        self.setValidCharacters()

        self.setMask()

        self.threadpool = QThreadPool()

    def setValidCharacters(self):
        self.chars = []

        chars = 'NS'
        self.chars.append(chars)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVZ'
        self.chars.append(chars)
        chars = ['01','02','03','04','05','06','07','08','09','10',
                   '11','12','13','14','15','16','17','18','19','20',
                   '21','22','23','24','25','26','27','28','29','30',
                   '31','32','33','34','35','36','37','38','39','40',
                   '41','42','43','44','45','46','47','48','49','50',
                   '51','52','53','54','55','56','57','58','59','60']
        self.chars.append(chars)
        chars = 'VXYZ'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
        chars = ['I','II','III','IV','V','VI']
        self.chars.append(chars)
        chars = '1234'
        self.chars.append(chars)
        chars = ['NO','NE','SO','SE']
        self.chars.append(chars)
        chars = 'ABCDEF'
        self.chars.append(chars)
        chars = ['I','II','III','IV']
        self.chars.append(chars)
        chars = '123456'
        self.chars.append(chars)
        chars = 'ABCD'
        self.chars.append(chars)
        
    def setMask(self):
        if self.scaleCombo.currentText() == '1000k':
            self.indexLineEdit.setInputMask('NN-NN')
        elif self.scaleCombo.currentText() == '500k':
            self.indexLineEdit.setInputMask('NN-NN-N')
        elif self.scaleCombo.currentText() == '250k':
            self.indexLineEdit.setInputMask('NN-NN-N-N')
        elif self.scaleCombo.currentText() == '100k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn')
        elif self.scaleCombo.currentText() == '50k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0')
        elif self.scaleCombo.currentText() == '25k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN')
        elif self.scaleCombo.currentText() == '10k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N')
        elif self.scaleCombo.currentText() == '5k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn')
        elif self.scaleCombo.currentText() == '2k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn-0')
        elif self.scaleCombo.currentText() == '1k':
            self.indexLineEdit.setInputMask('NN-NN-N-N-Nnn-0-NN-N-Nnn-0-N')
            
    def validateMI(self):
        mi = self.indexLineEdit.text()
        split = mi.split('-')
        for i in range(len(split)):
            word = str(split[i])
            if len(word) == 0:
                return False
            if i == 0:
                if word[0] not in self.chars[0]:
                    print word
                    return False
                if word[1] not in self.chars[1]:
                    print word
                    return False
            elif i == 1:
                if word not in self.chars[2]:
                    print word
                    return False
            elif i == 2:
                if word not in self.chars[3]:
                    print word
                    return False
            elif i == 3:
                if word not in self.chars[4]:
                    print word
                    return False
            elif i == 4:
                if word not in self.chars[5]:
                    print word
                    return False
            elif i == 5:
                if word not in self.chars[6]:
                    print word
                    return False
            elif i == 6:
                if word not in self.chars[7]:
                    print word
                    return False
            elif i == 7:
                if word not in self.chars[8]:
                    print word
                    return False
            elif i == 8:
                if word not in self.chars[9]:
                    print word
                    return False
            elif i == 9:
                if word not in self.chars[10]:
                    print word
                    return False
            elif i == 10:
                if word not in self.chars[11]:
                    print word
                    return False
        return True
    
    def disableAll(self):
        self.mirLineEdit.setEnabled(False)
        self.miLineEdit.setEnabled(False)
        self.indexLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_crsButton_clicked(self):
        projSelector = QgsGenericProjectionSelector()
        message = 'Select the Spatial Reference System!'
        projSelector.setMessage(theMessage=message)
        projSelector.exec_()
        try:
            epsg = int(projSelector.selectedAuthId().split(':')[-1])
            self.crs = QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.crs:
                self.crsLineEdit.setText(self.crs.description())
        except:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr(message))

    @pyqtSlot(str)
    def on_indexLineEdit_textEdited(self,s):
        if (s!=''):
            mi = self.utmgrid.getMIFromINomen(str(s))
            self.miLineEdit.setText(mi)

    @pyqtSlot(str)
    def on_miLineEdit_textEdited(self,s):
        if (s!=''):
            self.index = self.utmgrid.getINomenFromMI(str(s))
            self.indexLineEdit.setText(self.index)

    @pyqtSlot(str)
    def on_mirLineEdit_textEdited(self,s):
        if (s!=''):
            self.index = self.utmgrid.getINomenFromMIR(str(s))
            self.indexLineEdit.setText(self.index)

    @pyqtSlot(int)
    def on_scaleCombo_currentIndexChanged(self):
        self.setMask()

    @pyqtSlot(bool)
    def on_mirRadioButton_toggled(self, toggled):
        if toggled:
            self.mirLineEdit.setEnabled(True)
        else:
            self.mirLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_miRadioButton_toggled(self, toggled):
        if toggled:
            self.miLineEdit.setEnabled(True)
        else:
            self.miLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_indexRadioButton_toggled(self, toggled):
        if toggled:
            self.indexLineEdit.setEnabled(True)
        else:
            self.indexLineEdit.setEnabled(False)

    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        fileName = QFileDialog.getSaveFileName(parent=self, caption=self.tr('Save Output File'), filter='Shapefile (*.shp)')
        self.saveEdit.setText(fileName)
      
    @pyqtSlot()        
    def on_button_box_accepted(self):
        stopScale = int(self.stopScaleCombo.currentText().replace('k','')) 
        scale = int(self.scaleCombo.currentText().replace('k',''))
    
        if stopScale > scale:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('The stop scale denominator should not be bigger than \
                                                                    the scale denominator!'))
            return
        if self.createShapeBox.isChecked() and not self.saveEdit.text():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('A output file must be specified!'))
            return
        if not self.crsLineEdit.text():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('A CRS must be specified!'))
            return
        if not self.validateMI():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Invalid Map Index!'))            
            return
        
        # Initiating processing
        gridThread = UtmGrid()
        
        if self.createShapeBox.isChecked():
            self.layer = None
        else:
            self.layer = gridThread.createGridLayer(self.tr('Grid Zones'), 'Multipolygon', self.crs.authid())
            
        gridThread.setParameters(self.indexLineEdit.text(), stopScale, self.miLineEdit.text(), self.crs, self.saveEdit.text(), self.layer)
        # Connecting end signal
        gridThread.aux.processFinished.connect(self.finishProcess)
        gridThread.aux.rangeCalculated.connect(self.setRange)
        gridThread.aux.errorOccurred.connect(self.showError)
        gridThread.aux.stepProcessed.connect(self.updateProgress)
        # Setting the progress bar
        self.progressMessageBar = define._messagBar.createMessage(self.tr('Generating grid, please wait...'))
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.progressMessageBar.layout().addWidget(self.progressBar)
        define._messagBar.pushWidget(self.progressMessageBar, define._messagBar.INFO)
        self.progressBar.setRange(0, 0)
        self.progressMessageBar.destroyed.connect(gridThread.aux.cancel)
        # Starting process
        # self.threadpool.start(gridThread)
        gridThread.run()
        
    def setRange(self, maximum):
        self.progressBar.setRange(0, maximum)
        
    def showError(self, msg):
        QMessageBox.warning(self, self.tr('Warning!'), msg)
        
    def updateProgress(self):
        self.progressBar.setValue(self.progressBar.value() + 1)
        
    def finishProcess(self):
        self.progressBar.setValue(self.progressBar.maximum())
        
        if self.createShapeBox.isChecked():
            shpPath = ""
            if define.obstaclePath != None:
                shpPath = define.obstaclePath
            elif define.xmlPath != None:
                shpPath = define.xmlPath
            else:
                shpPath = define.appPath
            er = QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.saveEdit.text() + "/" + self.tr('Grid Zones') + ".shp", "utf-8", define._canvas.mapSettings().destinationCrs())
            layer = QgsVectorLayer(self.saveEdit.text(), self.tr('Grid Zones'), 'ogr')
            QgisHelper.appendToCanvas(define._canvas, [layer], "Grid Zones")
            # QgsMapLayerRegistry.instance().addMapLayer(layer)
            # layer = self.iface.addVectorLayer(self.saveEdit.text(), self.tr('Grid Zones'), 'ogr')
            self.updateMapCanvas(layer)
        else:
            # QgsMapLayerRegistry.instance().addMapLayer(self.layer)

            QgisHelper.appendToCanvas(define._canvas, [self.layer], "Grid Zones")
            self.updateMapCanvas(self.layer)
            
        QMessageBox.information(self, self.tr('Success!'), self.tr('Grid Created successfully!'))
        
    def updateMapCanvas(self, layer):
        # if layer:
        #     self.iface.setActiveLayer(layer)
            
        layer.updateExtents() 
        
        bbox = define._canvas.mapSettings().layerToMapCoordinates(layer, layer.extent())
        define._canvas.setExtent(bbox)
        define._canvas.refresh()
        