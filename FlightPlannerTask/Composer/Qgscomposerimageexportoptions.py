# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qgscomposerimageexportoptions.ui'
#
# Created: Wed Jun 22 10:05:53 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from qgis.gui import QgsSpinBox
from qgis.gui import QgsCollapsibleGroupBoxBasic
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class QgsComposerImageExportOptionsDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        # self.setObjectName(_fromUtf8("QgsComposerImageExportOptionsDialog"))
        self.resize(489, 325)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 2)
        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 2, 0, 1, 2)
        self.mResolutionSpinBox = QgsSpinBox(self.groupBox)
        self.mResolutionSpinBox.setPrefix(_fromUtf8(""))
        self.mResolutionSpinBox.setMaximum(3000)
        self.mResolutionSpinBox.setProperty("showClearButton", False)
        self.mResolutionSpinBox.setObjectName(_fromUtf8("mResolutionSpinBox"))
        self.gridLayout.addWidget(self.mResolutionSpinBox, 0, 2, 1, 2)
        self.mWidthSpinBox = QgsSpinBox(self.groupBox)
        self.mWidthSpinBox.setPrefix(_fromUtf8(""))
        self.mWidthSpinBox.setMinimum(0)
        self.mWidthSpinBox.setMaximum(99999999)
        self.mWidthSpinBox.setProperty("showClearButton", False)
        self.mWidthSpinBox.setObjectName(_fromUtf8("mWidthSpinBox"))
        self.gridLayout.addWidget(self.mWidthSpinBox, 1, 2, 1, 2)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.mHeightSpinBox = QgsSpinBox(self.groupBox)
        self.mHeightSpinBox.setPrefix(_fromUtf8(""))
        self.mHeightSpinBox.setMinimum(0)
        self.mHeightSpinBox.setMaximum(99999999)
        self.mHeightSpinBox.setProperty("showClearButton", False)
        self.mHeightSpinBox.setObjectName(_fromUtf8("mHeightSpinBox"))
        self.gridLayout.addWidget(self.mHeightSpinBox, 2, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.mClipToContentGroupBox = QgsCollapsibleGroupBoxBasic(self)
        self.mClipToContentGroupBox.setCheckable(True)
        self.mClipToContentGroupBox.setChecked(False)
        self.mClipToContentGroupBox.setObjectName(_fromUtf8("mClipToContentGroupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.mClipToContentGroupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_5 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_7.addWidget(self.label_5)
        self.mLeftMarginSpinBox = QgsSpinBox(self.mClipToContentGroupBox)
        self.mLeftMarginSpinBox.setMaximum(1000)
        self.mLeftMarginSpinBox.setObjectName(_fromUtf8("mLeftMarginSpinBox"))
        self.horizontalLayout_7.addWidget(self.mLeftMarginSpinBox)
        self.label_11 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_7.addWidget(self.label_11)
        self.mRightMarginSpinBox = QgsSpinBox(self.mClipToContentGroupBox)
        self.mRightMarginSpinBox.setMaximum(1000)
        self.mRightMarginSpinBox.setObjectName(_fromUtf8("mRightMarginSpinBox"))
        self.horizontalLayout_7.addWidget(self.mRightMarginSpinBox)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 4)
        self.label_12 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_5.addWidget(self.label_12, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.mClipToContentGroupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_5.addWidget(self.label_4, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 0, 1, 1)
        self.mTopMarginSpinBox = QgsSpinBox(self.mClipToContentGroupBox)
        self.mTopMarginSpinBox.setMaximum(1000)
        self.mTopMarginSpinBox.setObjectName(_fromUtf8("mTopMarginSpinBox"))
        self.gridLayout_5.addWidget(self.mTopMarginSpinBox, 0, 2, 1, 1)
        self.mBottomMarginSpinBox = QgsSpinBox(self.mClipToContentGroupBox)
        self.mBottomMarginSpinBox.setMaximum(1000)
        self.mBottomMarginSpinBox.setObjectName(_fromUtf8("mBottomMarginSpinBox"))
        self.gridLayout_5.addWidget(self.mBottomMarginSpinBox, 2, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_5)
        self.verticalLayout.addWidget(self.mClipToContentGroupBox)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.mResolutionSpinBox, self.mWidthSpinBox)
        self.setTabOrder(self.mWidthSpinBox, self.mHeightSpinBox)
        self.setTabOrder(self.mHeightSpinBox, self.mClipToContentGroupBox)
        self.setTabOrder(self.mClipToContentGroupBox, self.mTopMarginSpinBox)
        self.setTabOrder(self.mTopMarginSpinBox, self.mLeftMarginSpinBox)
        self.setTabOrder(self.mLeftMarginSpinBox, self.mRightMarginSpinBox)
        self.setTabOrder(self.mRightMarginSpinBox, self.mBottomMarginSpinBox)


        self.connect( self.mClipToContentGroupBox, QtCore.SIGNAL( "toggled( bool )" ), self.clipToContentsToggled);
        # self.mWidthSpinBox.valueChanged.connect(self.on_mWidthSpinBox_valueChanged)
        # self.mHeightSpinBox.valueChanged.connect(self.on_mHeightSpinBox_valueChanged)
        self.connect(self.mWidthSpinBox, QtCore.SIGNAL("valueChanged( int )"), self.on_mWidthSpinBox_valueChanged)
        self.connect(self.mHeightSpinBox, QtCore.SIGNAL("valueChanged( int )"), self.on_mHeightSpinBox_valueChanged)
        self.connect(self.mResolutionSpinBox, QtCore.SIGNAL("valueChanged( int )"), self.on_mResolutionSpinBox_valueChanged)


        settings = QtCore.QSettings();
        self.restoreGeometry( settings.value( "/Windows/ComposerImageExportOptionsDialog/geometry" ).toByteArray() );
    def retranslateUi(self):
        self.setWindowTitle(_translate("self", "Image export options", None))
        self.groupBox.setTitle(_translate("self", "Export options", None))
        self.label_9.setText(_translate("self", "Export resolution", None))
        self.label_13.setText(_translate("self", "Page height", None))
        self.mResolutionSpinBox.setSuffix(_translate("self", " dpi", None))
        self.mWidthSpinBox.setSpecialValueText(_translate("self", "Auto", None))
        self.mWidthSpinBox.setSuffix(_translate("self", " px", None))
        self.label_10.setText(_translate("self", "Page width", None))
        self.mHeightSpinBox.setSpecialValueText(_translate("self", "Auto", None))
        self.mHeightSpinBox.setSuffix(_translate("self", " px", None))
        self.mClipToContentGroupBox.setTitle(_translate("self", "Crop to content", None))
        self.label_5.setText(_translate("self", "Left", None))
        self.mLeftMarginSpinBox.setSuffix(_translate("self", " px", None))
        self.label_11.setText(_translate("self", "Right", None))
        self.mRightMarginSpinBox.setSuffix(_translate("self", " px", None))
        self.label_12.setText(_translate("self", "Bottom", None))
        self.label_4.setText(_translate("self", "Top margin", None))
        self.mTopMarginSpinBox.setSuffix(_translate("self", " px", None))
        self.mBottomMarginSpinBox.setSuffix(_translate("self", " px", None))

    def setResolution( self, resolution ):
        self.mResolutionSpinBox.setValue( resolution );

        if ( self.mImageSize.isValid() ):
            self.mWidthSpinBox.blockSignals( True );
            self.mHeightSpinBox.blockSignals( True );
            if ( self.mClipToContentGroupBox.isChecked() ):
                self.mWidthSpinBox.setValue( 0 );
                self.mHeightSpinBox.setValue( 0 );
            else:
                self.mWidthSpinBox.setValue( self.mImageSize.width() * resolution / 25.4 );
                self.mHeightSpinBox.setValue( self.mImageSize.height() * resolution / 25.4 );
            self.mWidthSpinBox.blockSignals( False );
            self.mHeightSpinBox.blockSignals( False );
    def resolution(self):
        return self.mResolutionSpinBox.value();
    def setImageSize( self, size ):
        self.mImageSize = size;
        self.mWidthSpinBox.blockSignals( True );
        self.mHeightSpinBox.blockSignals( True );
        self.mWidthSpinBox.setValue( size.width() * self.mResolutionSpinBox.value() / 25.4 );
        self.mHeightSpinBox.setValue( size.height() * self.mResolutionSpinBox.value() / 25.4 );
        self.mWidthSpinBox.blockSignals( False );
        self.mHeightSpinBox.blockSignals( False );
    def imageWidth(self):
        return self.mWidthSpinBox.value();
    def imageHeight(self):
        return self.mHeightSpinBox.value();
    def setCropToContents( self, crop ):
        self.mClipToContentGroupBox.setChecked( crop );
    
    def cropToContents(self):
        return self.mClipToContentGroupBox.isChecked();
    
    def getCropMargins( self):
        topMargin = self.mTopMarginSpinBox.value();
        rightMargin = self.mRightMarginSpinBox.value();
        bottomMargin = self.mBottomMarginSpinBox.value();
        leftMargin = self.mLeftMarginSpinBox.value();
        return topMargin, rightMargin, bottomMargin, leftMargin
    
    def setCropMargins( self, topMargin, rightMargin, bottomMargin, leftMargin ):
        self.mTopMarginSpinBox.setValue( topMargin );
        self.mRightMarginSpinBox.setValue( rightMargin );
        self.mBottomMarginSpinBox.setValue( bottomMargin );
        self.mLeftMarginSpinBox.setValue( leftMargin );
    
    def on_mWidthSpinBox_valueChanged( self, value ):
        self.mHeightSpinBox.blockSignals( True );
        self.mResolutionSpinBox.blockSignals( True );
        self.mHeightSpinBox.setValue( self.mImageSize.height() * self.mWidthSpinBox.value() / self.mImageSize.width() );
        self.mResolutionSpinBox.setValue( self.mWidthSpinBox.value() * 25.4 / self.mImageSize.width() );
        self.mHeightSpinBox.blockSignals( False );
        self.mResolutionSpinBox.blockSignals( False );
    
    def on_mHeightSpinBox_valueChanged( self, value ):
        self.mWidthSpinBox.blockSignals( True );
        self.mResolutionSpinBox.blockSignals( True );
        self.mWidthSpinBox.setValue( self.mImageSize.width() * self.mHeightSpinBox.value() / self.mImageSize.height() );
        self.mResolutionSpinBox.setValue( self.mHeightSpinBox.value() * 25.4 / self.mImageSize.height() );
        self.mWidthSpinBox.blockSignals( False );
        self.mResolutionSpinBox.blockSignals( False );
    
    def on_mResolutionSpinBox_valueChanged( self, value ):
        self.mWidthSpinBox.blockSignals( True );
        self.mHeightSpinBox.blockSignals( True );
        if ( self.mClipToContentGroupBox.isChecked() ):
            self.mWidthSpinBox.setValue( 0 );
            self.mHeightSpinBox.setValue( 0 );
        else:
            self.mWidthSpinBox.setValue( self.mImageSize.width() * self.mResolutionSpinBox.value() / 25.4 );
            self.mHeightSpinBox.setValue( self.mImageSize.height() * self.mResolutionSpinBox.value() / 25.4 );
        self.mWidthSpinBox.blockSignals( False );
        self.mHeightSpinBox.blockSignals( False );
    
    def clipToContentsToggled( self, state ):
        self.mWidthSpinBox.setEnabled( not state );
        self.mHeightSpinBox.setEnabled( not state );
        
        if ( state ):
            self.mWidthSpinBox.blockSignals( True );
            self.mWidthSpinBox.setValue( 0 );
            self.mWidthSpinBox.blockSignals( False );
            self.mHeightSpinBox.blockSignals( True );
            self.mHeightSpinBox.setValue( 0 );
            self.mHeightSpinBox.blockSignals( False );
        else:
            self.mWidthSpinBox.blockSignals( True );
            self.mWidthSpinBox.setValue( self.mImageSize.width() * self.mResolutionSpinBox.value() / 25.4 );
            self.mWidthSpinBox.blockSignals( False );
            self.mHeightSpinBox.blockSignals( True );
            self.mHeightSpinBox.setValue( self.mImageSize.height() * self.mResolutionSpinBox.value() / 25.4 );
            self.mHeightSpinBox.blockSignals( False );
