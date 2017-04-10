'''
Created on 12 Feb 2015

@author: Administrator
'''
from map.ui_layerSaveAsDlg import ui_layerSaveAsDlg
from qgis.core import QgsCoordinateReferenceSystem, QgsVectorFileWriter, QgsCoordinateTransform
from qgis.gui import QgsGenericProjectionSelector

from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtCore import Qt, QCoreApplication
import define

class layerSaveAsDlg(QDialog):
    '''
    classdocs
    '''
    def __init__(self, parent, layer):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self.ui = ui_layerSaveAsDlg()
        self.ui.setupUi(self)
#         self.layerSet = layerSet
        self.baseLayer = layer
        self.shpFormats = ["ESRI Shapefile", "GeoJSON"]
        self.fileTypes = ["ESRI Shape file(*.shp )", "GeoJSON(*.geojson)"]
        self.crsList = ["Layer CRS", "Project CRS", "Selected CRS"]         
        self.ui.cmbFormat.addItems(self.shpFormats)
        self.ui.cmbCrs.addItems(self.crsList)
        self.ui.btnBrowse.clicked.connect(self.browse)
        self.ui.txtCrs.setText("WGS 84")
        self.ui.txtCrs.setEnabled(False)
#         self.ui.cmbFormat.currentIndexChanged.connect(self.enableTxtAPV)
        self.ui.cmbCrs.currentIndexChanged.connect(self.crsSelectChange)
        self.ui.btnChange.clicked.connect(self.crsChange)
        self.ui.buttonBox.accepted.connect(self.saveLayer)
        self.crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)

    def browse(self):
        type1 = self.fileTypes[self.ui.cmbFormat.currentIndex()]
        filePath = QFileDialog.getSaveFileName(self, "Save layer as...",QCoreApplication.applicationDirPath (),type1)
        self.ui.txtSavePath.setText(filePath)
    def crsSelectChange(self):
        if self.ui.cmbCrs.currentIndex() == 2:
            self.ui.txtCrs.setEnabled(True) 
        else:
            self.ui.txtCrs.setEnabled(False)                    
    def crsChange(self):
        projectionDlg = QgsGenericProjectionSelector(self)
        projectionDlg.exec_()
#         print projectionDlg.selectedCrsId()
        srs = QgsCoordinateReferenceSystem(projectionDlg.selectedCrsId(), QgsCoordinateReferenceSystem.InternalCrsId)
        self.mCRS = srs.srsid()
        self.crs = QgsCoordinateReferenceSystem()
        self.crs.createFromId(self.mCRS, QgsCoordinateReferenceSystem.InternalCrsId )
#         authId = projectionDlg.selectedAuthId()
#         crsId = projectionDlg.selectedCrsId()
#         if authId != "":
#             if authId[:4] != "EPSG":
#                 self.crs = QgsCoordinateReferenceSystem(crsId, QgsCoordinateReferenceSystem.InternalCrsId)
#             else:
#                 self.crs = QgsCoordinateReferenceSystem(crsId, QgsCoordinateReferenceSystem.EpsgCrsId)
        self.ui.cmbCrs.setCurrentIndex(2)
        self.ui.txtCrs.setText(self.crs.description())
    def saveLayer(self):
        destCrs = None
        ct = QgsCoordinateTransform()
        if self.ui.txtSavePath.text() == "":
            QMessageBox.warning(self, "Error", "Please input save file path")
            return
        else:
            if self.ui.cmbCrs.currentIndex() == 0:                
                if self.baseLayer.crs() is None:
                    destCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
#                     er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", destCrs, self.ui.cmbFormat.currentText())
                else:
                    destCrs = self.baseLayer.crs()
                    print destCrs.authid()  
#                     er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", self.baseLayer.crs(), self.ui.cmbFormat.currentText())
            elif self.ui.cmbCrs.currentIndex() == 1:
                destCrs = define._canvas.mapSettings().destinationCrs()
                if destCrs is None:
                    destCrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
#                     er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", destCrs, self.ui.cmbFormat.currentText())
#                 else:
#                     er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", destCrs, self.ui.cmbFormat.currentText())
                
            else:
                destCrs = QgsCoordinateReferenceSystem(self.mCRS, QgsCoordinateReferenceSystem.InternalCrsId) 
                 
       
            if destCrs != self.baseLayer.crs():
                ct = QgsCoordinateTransform( self.baseLayer.crs(), destCrs )  
            er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", destCrs, self.ui.cmbFormat.currentText())
                    
#                 er = QgsVectorFileWriter.writeAsVectorFormat(self.baseLayer, self.ui.txtSavePath.text(), "utf-8", self.crs, self.ui.cmbFormat.currentText())
            QMessageBox.information(self, "Successful", "Export to vector file has been completed. ")
        QDialog.accept(self)