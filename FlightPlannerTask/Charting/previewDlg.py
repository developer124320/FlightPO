from PyQt4.QtCore import *
# import PyQt4
from PyQt4.QtGui import  QFileDialog, QDialog,QFontDialog, QColorDialog, QVBoxLayout,\
     QGridLayout, QSpinBox, QShortcut, QKeySequence, QWidget, QSpacerItem,\
    QGroupBox, QFrame, QWidget,QMainWindow, QLabel, QComboBox, QHBoxLayout,\
     QPushButton, QDialogButtonBox, QToolBar, QAction, QSizePolicy, QIcon, QPalette,\
      QFont,QPlainTextEdit,QCheckBox, QPen, QBrush, QColor,QMessageBox, QStandardItem, QStandardItemModel, QTableView
# from map.ui_preview import Ui_Previewself.grbPageProperty
# from map.textItem import TextItem
from FlightPlanner.Panels.GroupBox import GroupBox
from qgis.core import QgsComposerMap, QgsComposition, QgsComposerLabel,QgsComposerItem,QgsComposerMergeCommand
from qgis.gui import QgsComposerView, QgsComposerRuler,QgsPreviewEffect


import define
class previewDlg(QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent, comp, basePMCheck, model):
        '''
        Constructor
        '''
       
        QMainWindow.__init__(self, parent)
        
        self.basePMCheck = basePMCheck
#         self.ui = Ui_Previewself.grbPageProperty()
#         self.ui.setupUi(self)
        self.resize(1000,700)
        self.setWindowTitle("Preview Dialog")
        self.view = QgsComposerView(self)
        viewLayout = QGridLayout()
        viewLayout.setSpacing( 0 )
        viewLayout.setMargin( 0 )
        mHorizontalRuler = QgsComposerRuler( QgsComposerRuler.Horizontal )
        mVerticalRuler = QgsComposerRuler( QgsComposerRuler.Vertical )
        mRulerLayoutFix = QWidget()
        mRulerLayoutFix.setAttribute( Qt.WA_NoMousePropagation )
        mRulerLayoutFix.setBackgroundRole( QPalette.Window )
        mRulerLayoutFix.setFixedSize( mVerticalRuler.rulerSize(), mHorizontalRuler.rulerSize() )
        viewLayout.addWidget( mRulerLayoutFix, 0, 0 )
        viewLayout.addWidget( mHorizontalRuler, 0, 1 )
        viewLayout.addWidget( mVerticalRuler, 1, 0 )
        
        self.view.setContentsMargins( 0, 0, 0, 0 )
        self.view.setHorizontalRuler( mHorizontalRuler )
        self.view.setVerticalRuler( mVerticalRuler )
        viewLayout.addWidget( self.view, 1, 1 )

#         self.scene = comp

        self.view.setZoomLevel(1.0)
        self.view.setComposition(comp)
        self.scene = self.view.composition()   
        layout =  QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout.addLayout(viewLayout)

        self.mapItem = self.scene.getComposerMapById(0)
        
        self.view.scale(2.8, 2.8)        
        self.view.setPreviewModeEnabled(True)
                
        self.toolBarAction = self.addToolBar("composer action")
        self.actionMapRefresh = QAction(self)
        self.actionMapRefresh.setObjectName("actionMapRefresh")
        icon3 = QIcon("Resource/Refresh.png")
        self.actionMapRefresh.setIcon(icon3)
        self.actionMapRefresh.setToolTip("Refresh")
        # self.textItemAction.setCheckable(True)
        self.connect(self.actionMapRefresh, SIGNAL("triggered()"), self.actionMapRefresh_triggered)
        self.toolBarAction.addAction(self.actionMapRefresh)

        # # self.templeteCreateAction = QAction(self)
        # # self.templeteCreateAction.setObjectName("createTempleteAction")
        # # icon4 = QIcon("Resource\\templetepointer.png")
        # # self.templeteCreateAction.setIcon(icon4)
        # # self.templeteCreateAction.setToolTip("Create Templete")
        # # self.templeteCreateAction.setCheckable(True)
        # # self.connect(self.templeteCreateAction, SIGNAL("triggered()"), self.createTempleteAction)
        # # self.toolBar.addAction(self.templeteCreateAction)
        # layout.insertWidget(0, self.toolBar)

#         self.scene.selectedItemChanged.connect(self.selectedItemDisplay)
        self.view.selectedItemChanged.connect(self.selectedItemDisplay)
        
        self.view.cursorPosChanged.connect(self.cursorPosChangedEvent)
#         self.connect(self.view, SIGNAL("selectedItemChanged(QgsComposerItem)"),self, SLOT("selectedItemDisplay(QgsComposerItem)"))        
#         self.scene.composerLabelAdded.connect(self.composerLabelAddedEvent)
        self.view.itemRemoved.connect(self.deleteItem)
        # self.connect( self.view, SIGNAL( "actionFinished()" ), self.setSelectionTool)
        
        #listen out for position updates from the QgsComposerView
        self.propertyWidget = QWidget(self)
        hLayout.addWidget(self.propertyWidget)
        self.propertyWidget.setObjectName("propertyWidget")
        self.propertyWidget.resize(222, 302)
        self.vLayout_3 = QVBoxLayout(self.propertyWidget)
        self.vLayout_3.setObjectName("vLayout_3")
        self.groupBox = QGroupBox(self.propertyWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QFrame(self.groupBox)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.labelText = QPlainTextEdit(self.frame)
        self.labelText.setObjectName("labelText")
        self.verticalLayout.addWidget(self.labelText)
        self.btnLabelFont = QPushButton(self.frame)
        self.btnLabelFont.setObjectName("btnLabelFont")
        self.verticalLayout.addWidget(self.btnLabelFont)
        self.btnLabelColor = QPushButton(self.frame)
        self.btnLabelColor.setObjectName("btnLabelColor")
        self.verticalLayout.addWidget(self.btnLabelColor)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinLabelRotation = QSpinBox(self.frame_2)
        self.spinLabelRotation.setObjectName("spinLabelRotation")
        self.spinLabelRotation.setMinimum(-360)
        self.spinLabelRotation.setMaximum(360)
        self.horizontalLayout.addWidget(self.spinLabelRotation)
        self.verticalLayout.addWidget(self.frame_2)
        self.chbBackgroundEnable = QCheckBox(self.frame)
        self.chbBackgroundEnable.setChecked(True)
        self.chbBackgroundEnable.setObjectName("chbBackgroundEnable")
        self.verticalLayout.addWidget(self.chbBackgroundEnable)
        self.horizontalLayout_2.addWidget(self.frame)
        self.vLayout_3.addWidget(self.groupBox)
        
        self.resolutionFrame = QFrame(self.frame)
        self.resolutionFrame.setFrameShape(QFrame.StyledPanel)
        self.resolutionFrame.setFrameShadow(QFrame.Raised)
        self.resolutionFrame.setObjectName("resolutionFrame")
        self.horizontalLayout4 = QHBoxLayout(self.resolutionFrame)
        self.horizontalLayout4.setObjectName("horizontalLayout4")
        self.label_resolution = QLabel(self.resolutionFrame)
        self.label_resolution.setObjectName("label_resolution")
        self.label_resolution.setText("Print Resolution (dpi):")
        self.horizontalLayout4.addWidget(self.label_resolution)
        self.spinResolution = QSpinBox(self.resolutionFrame)
        self.spinResolution.setObjectName("spinResolution")
        self.spinResolution.setMinimum(0)
        self.spinResolution.setMaximum(1000)
        self.spinResolution.setValue(300)
        self.horizontalLayout4.addWidget(self.spinResolution)
#         self.verticalLayout.addWidget(self.frame_2)
        self.vLayout_3.addWidget(self.resolutionFrame)

        self.gbTable = GroupBox(self.propertyWidget)
        self.gbTable.Caption = "Table"
        self.vLayout_3.addWidget(self.gbTable)

        self.mTableView = QTableView(self.gbTable)
        self.gbTable.Add = self.mTableView
        hHeder = self.mTableView.horizontalHeader()
        hHeder.setVisible(False)
        vHeder = self.mTableView.verticalHeader()
        vHeder.setVisible(False)
        # self.mTableView.setFixedHeight(70)
        # self.mTableView.setFixedWidth(comp.paperWidth() - 40)

        # self.stdItemModel = QStandardItemModel()
        # self.

        self.spaceItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vLayout_3.addItem(self.spaceItem)
        
        self.groupBox.setTitle("Label Property")
        self.label.setText("Label Text:")
        self.btnLabelFont.setText("Label Font")
        self.btnLabelColor.setText("Label Color")
        self.label_2.setText("Label Rotation:")
        self.chbBackgroundEnable.setText("Background Enable")
        self.groupBox.setEnabled(False)
        self.connect( self.btnLabelFont, SIGNAL( "clicked()" ), self.btnLabelFontClick)
        self.connect( self.btnLabelColor, SIGNAL( "clicked()" ), self.btnLabelColorClick)
        self.connect( self.chbBackgroundEnable, SIGNAL( "clicked()" ), self.chbBackgroundEnableClick)
        self.labelText.textChanged.connect(self.labelTextChanged)
        self.spinLabelRotation.valueChanged.connect(self.spinLabelRotationValueChanged)
        layout.addLayout(hLayout)  
#
        self.btnBack = QPushButton()
        self.btnBack.setText("back")
        footerLayout = QHBoxLayout()
        footerLayout.addWidget(self.btnBack)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        footerLayout.addWidget(self.buttonBox)
        layout.addLayout(footerLayout)
        self.setLayout(layout)
        
        deleteItemKey = QShortcut(QKeySequence(Qt.Key_Delete), self)
        deleteItemKey.activated.connect(self.deleteItem)
        
        # self.btnBack.clicked.connect(self.back)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.acceptMethod)
        self.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        self.btnCancel = self.buttonBox.button(QDialogButtonBox.Cancel)
        self.view.setCurrentTool( QgsComposerView.Select )

        self.btnLabelColor.setVisible(False)
        # self.btnBack.setVisible(False)
        self.chbBackgroundEnable.setVisible(False)
#         self.view.emit(SIGNAL("actionFinished"))
        
#         if self.scene.plotStyle() != QgsComposition.Preview:
#         self.scene.setPlotStyle(QgsComposition.Preview)
#         self.mapItem.setPreviewMode(QgsComposerMap.Render)
#         self.mapItem.updateCachedImage()
#         self.mapItem.setSelected(True)
        self.mComposition = comp
        self.composerMapItem = self.mComposition.composerMapItems()[0]
        self.composerMapItem.setUpdatesEnabled(True)
        self.mStdModel = model

        self.mTableView.setModel(self.mStdModel)
        self.mTableView.setSpan(0, 0, 1, 6)
        self.mTableView.setSpan(1, 0, 1, 2)
        self.mTableView.setSpan(2, 0, 2, 1)
        self.mTableView.setSpan(4, 0, 1, 2)
        self.mTableView.setSpan(5, 0, 1, 2)
        self.mTableView.setSpan(6, 0, 1, 2)

        self.mTableView.setSpan(0, 6, 1, 8)
        self.mTableView.setSpan(1, 7, 1, 4)
        self.mTableView.setSpan(1, 11, 1, 3)
        self.mTableView.setSpan(2, 7, 1, 4)
        self.mTableView.setSpan(2, 11, 1, 3)


    def acceptMethod(self):
        # self.mStdModel.setItem(0, QStandardItem("nnnnnnnn"))
        filePath = QFileDialog.getSaveFileName(self, "Save PDF File",QCoreApplication.applicationDirPath (),"pdf files(*.pdf )")
        if filePath == "":
            return
        self.mComposition.clearSelection()
        self.mComposition.setPrintResolution(self.spinResolution.value())
        resultPdf = self.mComposition.exportAsPDF(filePath)
        if resultPdf :
            message = QMessageBox.information(self, "Result", "Successful export PDF")
        else:
            message = QMessageBox.information(self, "Result", "Don't export PDF")
    def rePresent(self, comp, model):
        self.mComposition = comp
        self.mStdModel = model
        self.view.setComposition(comp)
        self.scene = self.view.composition()
    def back(self):
        self.done(2)
    def spinLabelRotationValueChanged(self, rotationValue):
        self.selectedLabelItem.setItemRotation(rotationValue)
    def cursorPosChangedEvent(self, scenePointF):
        self.scenePoint = scenePointF
#         i = 100
    def labelTextChanged(self):
        self.selectedLabelItem.beginCommand( "Label text changed", QgsComposerMergeCommand.ComposerLabelSetText )
        self.selectedLabelItem.blockSignals( True )
        self.selectedLabelItem.setText( self.labelText.toPlainText() )
        self.selectedLabelItem.update()
        self.selectedLabelItem.blockSignals( False )
        self.selectedLabelItem.endCommand() 
    def chbBackgroundEnableClick(self):
        if self.chbBackgroundEnable.isChecked():
            self.selectedLabelItem.setBackgroundEnabled(True)
            self.mapItem.updateCachedImage()
        else:
            self.selectedLabelItem.setBackgroundEnabled(False)
            self.mapItem.updateCachedImage()
         
    def btnLabelFontClick(self):
        dlgFont = QFontDialog(self) 
        dlgFont.setCurrentFont(self.selectedLabelItem.font())
        result = dlgFont.exec_()  
        if result == 1:
            self.labelFont = dlgFont.selectedFont()
        else:
            self.labelFont = QFont()
            
        self.selectedLabelItem.setFont(self.labelFont)
    def btnLabelColorClick(self):
        dlgColor = QColorDialog(self) 
        dlgColor.setCurrentColor(self.selectedLabelItem.fontColor())
        result = dlgColor.exec_() 
        if result == 1:            
            self.labelColor = dlgColor.selectedColor()
            self.selectedLabelItem.setFontColor(self.labelColor)
        
    def createTempleteAction(self):
        if self.templeteCreateAction.isChecked() and self.basePMCheck:
            font = QFont("Arial", 13)
            font.setItalic(True)
            self.compLabel1 = QgsComposerLabel(self.scene)
            self.compLabel1.setFont(font)
            self.compLabel1.setText("South China Sea")
            self.compLabel1.setBackgroundEnabled(False)
            self.compLabel1.setItemPosition(156,100)
            self.compLabel1.adjustSizeToText()
            self.compLabel1.setItemRotation(60)
#             mapitem = self.scene.composerMapItems()
#             mapitem[0].addItem(self.compLabel1)
            self.scene.addItem(self.compLabel1)
            
            self.compLabel2 = QgsComposerLabel(self.scene)
            self.compLabel2.setFont(font)
            self.compLabel2.setText("Straits Of Malacca")
            self.compLabel2.setBackgroundEnabled(False)
            self.compLabel2.setItemPosition(35,100)
            self.compLabel2.adjustSizeToText()
            self.compLabel2.setItemRotation(60)
            self.scene.addItem(self.compLabel2)
            
            font.setItalic(False)
            self.compLabel3 = QgsComposerLabel(self.scene)
            self.compLabel3.setFont(font)
            self.compLabel3.setBackgroundEnabled(False)
            self.compLabel3.setText("THAILAND")
            self.compLabel3.setItemPosition(68,60)
            self.compLabel3.adjustSizeToText()
#             self.compLabel3.setItemRotation(0.5)
            self.scene.addItem(self.compLabel3)
#             self.templeteCreateAction.setChecked(False)
            
            self.compLabel4 = QgsComposerLabel(self.scene)
            self.compLabel4.setFont(font)
            self.compLabel4.setBackgroundEnabled(False)
            self.compLabel4.setText("SINGAPORE")
            self.compLabel4.setItemPosition(141,218)
            self.compLabel4.adjustSizeToText()
#             self.compLabel3.setItemRotation(0.5)
            self.scene.addItem(self.compLabel4)
            self.templeteCreateAction.setChecked(False)
            self.compLabel4.setSelected(True)
        elif self.templeteCreateAction.isChecked() and self.basePMCheck == False:
            font = QFont("Arial", 14)
            font.setItalic(True)
            self.compLabel5 = QgsComposerLabel(self.scene)
            self.compLabel5.setFont(font)
            self.compLabel5.setText("South China Sea")
            self.compLabel5.setBackgroundEnabled(False)
            self.compLabel5.setItemPosition(108,86)
            self.compLabel5.adjustSizeToText()
            self.compLabel5.setItemRotation(-45)
#             mapitem = self.scene.composerMapItems()
#             mapitem[0].addItem(self.compLabel1)
            self.scene.addItem(self.compLabel5)
            
            self.compLabel6 = QgsComposerLabel(self.scene)
            self.compLabel6.setFont(font)
            self.compLabel6.setText("Sulu Sea")
            self.compLabel6.setBackgroundEnabled(False)
            self.compLabel6.setItemPosition(236,38)
            self.compLabel6.adjustSizeToText()
            self.compLabel6.setItemRotation(45)
            self.scene.addItem(self.compLabel6)
            
            font.setItalic(False)
            self.compLabel7 = QgsComposerLabel(self.scene)
            self.compLabel7.setFont(font)
            self.compLabel7.setBackgroundEnabled(False)
            self.compLabel7.setText("Celebes Sea")
            self.compLabel7.setItemPosition(242,112)
            self.compLabel7.adjustSizeToText()
            self.compLabel7.setItemRotation(-45)
#             self.compLabel3.setItemRotation(0.5)
            self.scene.addItem(self.compLabel7)
#             self.templeteCreateAction.setChecked(False)
            
            self.compLabel8 = QgsComposerLabel(self.scene)
            self.compLabel8.setFont(font)
            self.compLabel8.setBackgroundEnabled(False)
            self.compLabel8.setText("INDONESIA\n(Kalimantan)")
            self.compLabel8.setItemPosition(172,148,32,16)
#             self.compLabel8.setHAlign(Qt.AlignHCenter)
#             self.compLabel8.setVAlign(Qt.AlignVCenter)
#             self.compLabel8.setFrameEnabled(False)
#             self.compLabel8.setItemPosition()
#             self.compLabel8.adjustSizeToText()
#             self.compLabl3.setItemRotation(0.5)
            self.scene.addItem(self.compLabel8)
            
            self.compLabel9 = QgsComposerLabel(self.scene)
            self.compLabel9.setFont(font)
            self.compLabel9.setBackgroundEnabled(False)
            self.compLabel9.setText("BRUNEI")
            self.compLabel9.setItemPosition(136,83)
            self.compLabel9.adjustSizeToText()
#             self.compLabl3.setItemRotation(0.5)
            self.scene.addItem(self.compLabel9)
            self.templeteCreateAction.setChecked(False)
            
            
        pass
    def actionMapRefresh_triggered(self):

        self.view.setCurrentTool(QgsComposerView.AddRectangle)
    def setSelectionTool(self):
        self.view.deleteSelectedItems()
        font = QFont("Arial", 14)
        newLabelItem = QgsComposerLabel( self.scene )
        newLabelItem.setText( "QGIS" )
        newLabelItem.setFont(font)
        
        newLabelItem.setItemPosition(self.scenePoint.x(),self.scenePoint.y())
        newLabelItem.adjustSizeToText()
    
        self.scene.addItem( newLabelItem )
#         selectItemPoint = self.scene.composerItemAt(self.scenePoint)
        newLabelItem.setSelected( True )
        self.groupBox.setEnabled(True)
        self.selectedLabelItem = newLabelItem 
#         txt = self.selectedLabelItem.text()
#         textDoc = QTextDocument(txt) 
        self.labelText.setPlainText(self.selectedLabelItem.text())
#         self.scene.setSelectedItem(self.newLabelItem)
        
        self.view.setCurrentTool( QgsComposerView.Select )
#         self.selectedLabelItem = self.view.currentTool()
        self.textItemAction.setChecked(False)
    def selectedItemDisplay(self, item):
        
        if self.scene.plotStyle() != QgsComposition.Preview:
            self.scene.setPlotStyle(QgsComposition.Preview)
            self.mapItem.setPreviewMode(QgsComposerMap.Render)
            self.mapItem.updateCachedImage()
        item._class_ = QgsComposerLabel
#         selectedItems = self.scene.selectedComposerItems(True)
#         if isinstance(item, QgsComposerItem):
#             self.selectedLabelItem = item
#         if isinstance(item, QGraphicsRectItem):
#             self.selectedLabelItem = item
        if isinstance(item, QgsComposerLabel):
            self.selectedLabelItem = item 
            self.groupBox.setEnabled(True)
            self.labelText.setPlainText(self.selectedLabelItem.text())
            self.spinLabelRotation.setValue(self.selectedLabelItem.rotation())
        else:
            self.groupBox.setEnabled(False)
#         print "debug"
        itemName = self.view.currentTool() 
        if  itemName == 5:
            item.setText("label")
        pass
    def deleteItem(self):
        self.view.deleteSelectedItems()
        
#     def initPaperSize(self):
#         self.paperStyle = {}
# #           // ISO formats
#         self.paperStyle[ "A5 (148x210 mm)" ] = [148.0, 210.0]
#         self.paperStyle[ "A4 (210x297 mm)" ] = [210.0, 297.0]
#         self.paperStyle[ "A3 (297x420 mm)" ] = [297.0, 420.0]
#         self.paperStyle[ "A2 (420x594 mm)" ] = [420.0, 594.0]
#         self.paperStyle[ "A1 (594x841 mm)" ] = [594.0, 841.0]
#         self.paperStyle[ "A0 (841x1189 mm)"] = [841.0, 1189.0]
#         self.paperStyle[ "B5 (176 x 250 mm)"] = [176.0, 250.0]
#         self.paperStyle[ "B4 (250 x 353 mm)"] = [250.0, 353.0]
#         self.paperStyle[ "B3 (353 x 500 mm)"] = [353.0, 500.0]
#         self.paperStyle[ "B2 (500 x 707 mm)"] = [500.0, 707.0]
#         self.paperStyle[ "B1 (707 x 1000 mm)"] = [707.0, 1000.0]
#         self.paperStyle[ "B0 (1000 x 1414 mm)"] = [1000.0, 1414.0]
# #         // North american formats
#         self.paperStyle[ "Legal (8.5x14 in)"] = [215.9, 355.6]
#         self.paperStyle[ "ANSI A (Letter; 8.5x11 in)"] = [215.9, 279.4]
#         self.paperStyle[ "ANSI B (Tabloid; 11x17 in)"] = [279.4, 431.8]
#         self.paperStyle[ "ANSI C (17x22 in)"] = [431.8, 558.8]
#         self.paperStyle[ "ANSI D (22x34 in)"] = [558.8, 863.6]
#         self.paperStyle[ "ANSI E (34x44 in)"] = [863.6, 1117.6]
#         self.paperStyle[ "Arch A (9x12 in)"] = [228.6, 304.8]
#         self.paperStyle[ "Arch B (12x18 in)"] = [304.8, 457.2]
#         self.paperStyle[ "Arch C (18x24 in)"] = [457.2, 609.6]
#         self.paperStyle[ "Arch D (24x36 in)"] = [609.6, 914.4]
#         self.paperStyle[ "Arch E (36x48 in)"] = [914.4, 1219.2]
#         self.paperStyle[ "Arch E1 (30x42 in)"] = [762, 1066.8]
#         for name in self.paperStyle:
#             self.cmbPresects.addItem(name)
#         i = 0
#         for name in self.paperStyle:
#             if [self.scene.paperWidth(),self.scene.paperHeight()] == self.paperStyle[name]:
#                 self.cmbPresects.setCurrentIndex(i)
#             i += 1
#             
#         
#             
