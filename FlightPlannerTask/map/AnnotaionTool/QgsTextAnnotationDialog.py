'''
Created on 28 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QWidget, QFontComboBox,  QDialog, QDialogButtonBox, QPushButton, QColorDialog, \
    QStackedWidget, QFont, QTextEdit, QSizePolicy, QSpinBox, QSpacerItem, QGridLayout, QHBoxLayout
from PyQt4.QtCore import QSize, Qt, QObject, SIGNAL
from qgis.gui import QgsColorButton, QgsSymbolV2SelectorDialog
from qgis.core import QgsStyleV2, QgsSymbolLayerV2Utils
from map.AnnotaionTool.QgsAnnotationWidget import QgsAnnotationWidget

class QgsTextAnnotationDialog(QDialog):
    def __init__(self, item):
        QDialog.__init__(self)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(("gridLayout"))
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(("horizontalLayout"))
        self.mFontComboBox = QFontComboBox(self)
        self.mFontComboBox.setObjectName(("mFontComboBox"))
        self.horizontalLayout.addWidget(self.mFontComboBox)
        spacerItem = QSpacerItem(38, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.mFontSizeSpinBox = QSpinBox(self)
        self.mFontSizeSpinBox.setObjectName(("mFontSizeSpinBox"))
        self.horizontalLayout.addWidget(self.mFontSizeSpinBox)
        self.mBoldPushButton = QPushButton(self)
        self.mBoldPushButton.setMinimumSize(QSize(50, 0))
        self.mBoldPushButton.setCheckable(True)
        self.mBoldPushButton.setObjectName(("mBoldPushButton"))
        self.horizontalLayout.addWidget(self.mBoldPushButton)
        self.mItalicsPushButton = QPushButton(self)
        self.mItalicsPushButton.setMinimumSize(QSize(50, 0))
        self.mItalicsPushButton.setCheckable(True)
        self.mItalicsPushButton.setObjectName(("mItalicsPushButton"))
        self.horizontalLayout.addWidget(self.mItalicsPushButton)
        self.mFontColorButton = QgsColorButton(self)
        self.mFontColorButton.setText((""))
        self.mFontColorButton.setAutoDefault(False)
        self.mFontColorButton.setObjectName(("mFontColorButton"))
        self.horizontalLayout.addWidget(self.mFontColorButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.mButtonBox = QDialogButtonBox(self)
        self.mButtonBox.setOrientation(Qt.Horizontal)
        self.mButtonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.mButtonBox.setObjectName(("mButtonBox"))
        self.gridLayout.addWidget(self.mButtonBox, 3, 0, 1, 1)
        self.mTextEdit = QTextEdit(self)
        self.mTextEdit.setObjectName(("mTextEdit"))
        self.gridLayout.addWidget(self.mTextEdit, 1, 0, 1, 1)
        self.mStackedWidget = QStackedWidget(self)
        self.mStackedWidget.setObjectName(("mStackedWidget"))
        self.page = QWidget()
        self.page.setObjectName(("page"))
        self.mStackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(("page_2"))
        self.mStackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.mStackedWidget, 2, 0, 1, 1)
        self.setLayout(self.gridLayout)
        
        self.mStackedWidget.setCurrentIndex(0)
        QObject.connect(self.mButtonBox, SIGNAL(("accepted()")), self.accept)
        QObject.connect(self.mButtonBox, SIGNAL(("rejected()")), self.reject)
        
        self.setTabOrder(self.mFontComboBox, self.mFontSizeSpinBox)
        self.setTabOrder(self.mFontSizeSpinBox, self.mBoldPushButton)
        self.setTabOrder(self.mBoldPushButton, self.mItalicsPushButton)
        self.setTabOrder(self.mItalicsPushButton, self.mFontColorButton)
        self.setTabOrder(self.mFontColorButton, self.mTextEdit)
        self.setTabOrder(self.mTextEdit, self.mButtonBox)
        
        self.setWindowTitle("Annotation text")
        self.mBoldPushButton.setText("B")
        self.mItalicsPushButton.setText("I")
        
        self.mTextDocument = None
        self.mItem = item
        self.mEmbeddedWidget = QgsAnnotationWidget(self, self.mItem )
        self.mEmbeddedWidget.show()
        self.mStackedWidget.addWidget( self.mEmbeddedWidget )
        self.mStackedWidget.setCurrentWidget( self.mEmbeddedWidget )
        if ( self.mItem != None ):
            self.mTextDocument = self.mItem.document()
            self.mTextEdit.setDocument( self.mTextDocument )
        self.mFontColorButton.setColorDialogTitle(  "Select font color"  )
        self.mFontColorButton.setColorDialogOptions( QColorDialog.ShowAlphaChannel )
        self.setCurrentFontPropertiesToGui()
        QObject.connect( self.mButtonBox, SIGNAL("accepted()"), self.applyTextToItem)
#         QObject.connect( self.mFontComboBox, SIGNAL( "currentFontChanged(QFont())"), self.changeCurrentFormat)
        self.mFontComboBox.currentFontChanged.connect(self.changeCurrentFormat)
        QObject.connect( self.mFontSizeSpinBox, SIGNAL( "valueChanged( int )" ), self.changeCurrentFormat ) 
        QObject.connect( self.mBoldPushButton, SIGNAL( "toggled( bool )" ), self.changeCurrentFormat)
        QObject.connect( self.mItalicsPushButton, SIGNAL( "toggled( bool )" ), self.changeCurrentFormat)
        QObject.connect( self.mTextEdit, SIGNAL( "cursorPositionChanged()" ), self.setCurrentFontPropertiesToGui )
        
#         QObject.connect( self.mButtonBox, SIGNAL( "accepted()" ), self.applySettingsToItem)
        deleteButton = QPushButton( "Delete" )
        QObject.connect( deleteButton, SIGNAL( "clicked()" ), self.deleteItem )
        self.mButtonBox.addButton( deleteButton, QDialogButtonBox.RejectRole )
    def applyTextToItem(self):
        if ( self.mItem  != None and self.mTextDocument !=None ):
            if ( self.mEmbeddedWidget != None):
                self.mEmbeddedWidget.apply()
            self.mItem.setDocument( self.mTextDocument )
            self.mItem.update()
    def changeCurrentFormat(self):
        newFont = QFont()
        newFont.setFamily( self.mFontComboBox.currentFont().family() )
        #bold
        if ( self.mBoldPushButton.isChecked() ):
            newFont.setBold( True )
        else:
            newFont.setBold( False )
        #italic
        if ( self.mItalicsPushButton.isChecked() ):
            newFont.setItalic( True )
        else:
            newFont.setItalic( False )
        #size
        newFont.setPointSize( self.mFontSizeSpinBox.value() )
        self.mTextEdit.setCurrentFont( newFont )
        #color
        self.mTextEdit.setTextColor( self.mFontColorButton.color() )
        
    def on_mFontColorButton_colorChanged(self, color ):
        self.changeCurrentFormat()
    def setCurrentFontPropertiesToGui(self):
        self.blockAllSignals( True )
        currentFont = self.mTextEdit.currentFont()
        self.mFontComboBox.setCurrentFont( currentFont )
        self.mFontSizeSpinBox.setValue( currentFont.pointSize() )
        self.mBoldPushButton.setChecked( currentFont.bold() )
        self.mItalicsPushButton.setChecked( currentFont.italic() )
        self.mFontColorButton.setColor( self.mTextEdit.textColor() )
        self.blockAllSignals( False )
        
    def blockAllSignals(self, block ):
        self.mFontComboBox.blockSignals( block )
        self.mFontSizeSpinBox.blockSignals( block )
        self.mBoldPushButton.blockSignals( block )
        self.mItalicsPushButton.blockSignals( block )
        self.mFontColorButton.blockSignals( block )
    
    def deleteItem(self):
        scene = self.mItem.scene()
        if ( scene != None ):
            scene.removeItem( self.mItem )
        self.mItem = None


