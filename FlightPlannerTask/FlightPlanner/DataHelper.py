# -*- coding: UTF-8 -*-
'''
Created on 20 Apr 2014

@author: Administrator
'''
from PyQt4.QtGui import QLineEdit, QComboBox, QTableView, QProgressBar, QApplication, QCheckBox, QStandardItemModel, QRadioButton
from PyQt4.QtXml import QDomDocument
from PyQt4.QtCore import QFile, QTextStream, Qt, QVariant, QFileInfo, QString
from FlightPlanner.Panels.PositionPanel import PositionPanel
from FlightPlanner.Panels.AltitudeBoxPanel import AltitudeBoxPanel, Altitude
from FlightPlanner.Panels.CheckBox import CheckBox
from FlightPlanner.Panels.ComboBoxPanel import ComboBoxPanel
from FlightPlanner.Panels.DegreesBoxPanel import DegreesBoxPanel
from FlightPlanner.Panels.DistanceBoxPanel import DistanceBoxPanel, Distance, DistanceUnits
from FlightPlanner.Panels.ListBox import ListBox
from FlightPlanner.Panels.MCAHPanel import MCAHPanel, MCAHType
from FlightPlanner.Panels.NumberBoxPanel import NumberBoxPanel
from FlightPlanner.Panels.OCAHPanel import OCAHPanel
from FlightPlanner.Panels.ProtectionAreaPanel import ProtectionAreaPanel, ProtectionAreaType
# from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.Panels.SpeedBoxPanel import SpeedBoxPanel, Speed, SpeedUnits
from FlightPlanner.Panels.TextBoxPanel import TextBoxPanel
from FlightPlanner.Panels.TrackRadialBoxPanel import TrackRadialBoxPanel
from FlightPlanner.Panels.AngleGradientBoxPanel import AngleGradientBoxPanel
# from FlightPlanner.Panels.RnavTolerancesPanel import RnavTolerancesPanel
from FlightPlanner.QgisHelper import QgisHelper
from FlightPlanner.types import Point3D, AltitudeUnits

from FlightPlanner.Dialogs.DlgCrcCheck import DlgCrcCheck

from Type.String import String
from Type.FasDataBlockFile import FasDataBlockFile
from qgis.core import QGis
from PyQt4.QtGui import QMessageBox
import define
class DataHelper:
    
    @staticmethod
    def createNameValueElem(doc, objType, objName, objValue):
        elem = doc.createElement(objType)
        objNameElem = doc.createElement("ObjectName")
        objNameElem.appendChild(doc.createTextNode(objName))
        elem.appendChild(objNameElem)
        valueElem = doc.createElement("Value")
        valueElem.appendChild(doc.createTextNode(str(objValue)))
        elem.appendChild(valueElem)
        return elem
    
    @staticmethod
    def createPositionPanelElem(doc, objType, positionPanel):
        elem = doc.createElement(objType)
        objNameElem = doc.createElement("ObjectName")
        objNameElem.appendChild(doc.createTextNode(positionPanel.objectName()))
        elem.appendChild(objNameElem)

        idElem = doc.createElement("ID")
        idElem.appendChild(doc.createTextNode(positionPanel.ID))
        elem.appendChild(idElem)

        xElem = doc.createElement("X")
        if positionPanel.Point3d == None:
            xElem.appendChild(doc.createTextNode(""))
        else:
            xElem.appendChild(doc.createTextNode(str(positionPanel.Point3d.get_X())))
        elem.appendChild(xElem)

        yElem = doc.createElement("Y")
        if positionPanel.Point3d == None:
            yElem.appendChild(doc.createTextNode(""))
        else:
            yElem.appendChild(doc.createTextNode(str(positionPanel.Point3d.get_Y())))
        elem.appendChild(yElem)

        zElem = doc.createElement("Z")
        if positionPanel.Point3d == None:
            zElem.appendChild(doc.createTextNode(""))
        else:
            zElem.appendChild(doc.createTextNode(str(positionPanel.Point3d.get_Z())))
        elem.appendChild(zElem)
        return elem
    @staticmethod
    def createTableElem(doc, objType, table):
        elem = doc.createElement(objType)
        objNameElem = doc.createElement("ObjectName")
        objNameElem.appendChild(doc.createTextNode(table.objectName()))
        elem.appendChild(objNameElem)
        model = table.model()
        if model != None:
            rowCount = model.rowCount()
            columCount = model.columnCount()

            for i in range(rowCount):
                recordElem = doc.createElement("record")
                for j in range(columCount):
                    value = model.data(model.index(i,j), Qt.EditRole).toString()
                    columElem = doc.createElement("column")
                    columElem.appendChild(doc.createTextNode(value))
                    recordElem.appendChild(columElem)
                elem.appendChild(recordElem)
            
        return elem
    
    @staticmethod
    def createObstacleTableElem(doc, objType, model, tblView, filterString = None, resultHideColumnIndexs = None):
        messageLabel = ""
        if filterString != None:
            messageLabel = "Exporting result(" + filterString + ") ..."
        else:
            messageLabel = "Exporting result ..."
        progressMessageBar = define._messagBar.createMessage(messageLabel)
        progress = QProgressBar()
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)        
        progressMessageBar.layout().addWidget(progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        progress.setValue(0)
#         surfsaceTypeStr = model.filterFixedString()
        
        elem = doc.createElement(objType)
#         objNameElem = doc.createElement("ObjectName")
#         objNameElem.appendChild(doc.createTextNode(table.objectName()))
#         elem.appendChild(objNameElem)
#         model = table.model()
        rowCount = model.rowCount()
        
        
#         progressMaxValue = rowCount
        progress.setMaximum(rowCount)
        columCount = model.columnCount()
#         recordElem = doc.createElement("record")
#         for j in range(columCount):
#             if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
#                 continue
#             tagName = model.fixedColumnLabels[j]
#             columElem = doc.createElement(DataHelper.filterTagName(tagName))
#             columElem.appendChild(doc.createTextNode(model.fixedColumnLabels[j]))
#             recordElem.appendChild(columElem)
#         elem.appendChild(recordElem)
        strLatLonNone = QVariant("0" + unicode("° ", "utf-8") + "0' 0.0000\"")
#         value = QVariant(strLatLonNone)
        rowCount = define._numberSavingObstacles
        for i in range(rowCount):

            recordElem = doc.createElement("record")
            if model.data(model.index(i,5), Qt.EditRole) == strLatLonNone and model.data(model.index(i,6), Qt.EditRole) == strLatLonNone:
                x = float(model.data(model.index(i,3), Qt.EditRole).toString())
                y = float(model.data(model.index(i,4), Qt.EditRole).toString())
                positionDegree = QgisHelper.Meter2DegreePoint3D(Point3D(x, y, 0))
            for j in range(columCount):
                if isinstance(model, QStandardItemModel):
                    if model.horizontalHeaderItem(j).text() == "" or model.horizontalHeaderItem(j).text() == "#":
                        continue
                flag = False
                for k in range(len(resultHideColumnIndexs)):                    
                    if j == resultHideColumnIndexs[k]:
                        flag = True
                        break
                if flag:
#                 if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
                    continue
                ss = model.data(model.index(i,5), Qt.EditRole).toString()
                ss1 = strLatLonNone.toString()
                if j == 5 and model.data(model.index(i,5), Qt.EditRole) == strLatLonNone:
                    variantValue = QVariant(QgisHelper.strDegree(positionDegree.y()))
                    value = variantValue.toString()
                elif j == 6 and model.data(model.index(i,6), Qt.EditRole) == strLatLonNone:
                    variantValue = QVariant(QgisHelper.strDegree(positionDegree.x()))
                    value = variantValue.toString()
                else:
                    value = model.data(model.index(i,j), Qt.EditRole).toString()
                # if isinstance(model, QStandardItemModel):
                try:
                    tagName = model.fixedColumnLabels[j]
                except:
                    tagName = model.horizontalHeaderItem(j).text()
                    if isinstance(tagName, QString):
                        tagName = String.QString2Str(tagName)
                
                columElem = doc.createElement(DataHelper.filterTagName(tagName))
                columElem.appendChild(doc.createTextNode(value))
                recordElem.appendChild(columElem)
            elem.appendChild(recordElem)    
            progress.setValue(i)
            QApplication.processEvents()  
        progress.setValue(rowCount)
        define._messagBar.hide()        
        return elem
    
    @staticmethod
    def saveInputParameters(fileName, dialog, otherParameters = None):
        newPanelExisting = False
        doc = QDomDocument()
        rootElem = doc.createElement(dialog.objectName())
        xmlDeclaration = doc.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"utf-8\"" )
        doc.appendChild( xmlDeclaration )

        # lineEditWriteFlag = True
        # comboBoxWriteFlag = True
        # checkBoxWriteFlag = True


        allTextBoxPanels = dialog.findChildren(TextBoxPanel)
        if len(allTextBoxPanels) > 0:
            textCtrlsElem = doc.createElement("TextBoxPanelCtrls")
            i = 0
            for textBoxPanel in allTextBoxPanels:
                i += 1
                elem = DataHelper.createNameValueElem(doc, "TextBoxPanel", textBoxPanel.objectName(), textBoxPanel.Value)
                textCtrlsElem.appendChild(elem)
                newPanelExisting = True

            rootElem.appendChild(textCtrlsElem)

        allCheckBoxs = dialog.findChildren(CheckBox)
        if len(allCheckBoxs) > 0:
            checkBoxsElem = doc.createElement("CheckBoxs")
            i = 0
            for checkBox in allCheckBoxs:
                i += 1
                elem = DataHelper.createNameValueElem(doc, "CheckBox", checkBox.objectName(), str(checkBox.Checked))
                checkBoxsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(checkBoxsElem)

        allRadioBtns = dialog.findChildren(QRadioButton)
        if len(allRadioBtns) > 0:
            radioBtnsElem = doc.createElement("QRadioButtons")
            for radioBtn in allRadioBtns:
                elem = DataHelper.createNameValueElem(doc, "QRadioButton", radioBtn.objectName(), str(radioBtn.isChecked()))
                radioBtnsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(radioBtnsElem)

        numberBoxPanels = dialog.findChildren(NumberBoxPanel)
        if len(numberBoxPanels) > 0:
            numberBoxPanelsElem = doc.createElement("NumberBoxPanels")
            for numberBoxPanel in numberBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "NumberBoxPanel", numberBoxPanel.objectName(), str(numberBoxPanel.Value))
                numberBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(numberBoxPanelsElem)

        altitudeBoxPanels = dialog.findChildren(AltitudeBoxPanel)
        if len(altitudeBoxPanels) > 0:
            altitudeBoxPanelsElem = doc.createElement("AltitudeBoxPanels")
            for altitudeBoxPanel in altitudeBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "AltitudeBoxPanel", altitudeBoxPanel.objectName(), str(altitudeBoxPanel.Value.Metres))
                altitudeBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(altitudeBoxPanelsElem)

        speedBoxPanels = dialog.findChildren(SpeedBoxPanel)
        if len(speedBoxPanels) > 0:
            speedBoxPanelsElem = doc.createElement("SpeedBoxPanels")
            for speedBoxPanel in speedBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "SpeedBoxPanel", speedBoxPanel.objectName(), str(speedBoxPanel.Value.Knots))
                speedBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(speedBoxPanelsElem)

        distanceBoxPanels = dialog.findChildren(DistanceBoxPanel)
        if len(distanceBoxPanels) > 0:
            distanceBoxPanelsElem = doc.createElement("DistanceBoxPanels")
            for distanceBoxPanel in distanceBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "DistanceBoxPanel", distanceBoxPanel.objectName(), str(distanceBoxPanel.Value.Metres))
                distanceBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(distanceBoxPanelsElem)

        trackRadialBoxPanels = dialog.findChildren(TrackRadialBoxPanel)
        if len(trackRadialBoxPanels) > 0:
            trackRadialBoxPanelsElem = doc.createElement("TrackRadialBoxPanels")
            for trackRadialBoxPanel in trackRadialBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "TrackRadialBoxPanel", trackRadialBoxPanel.objectName(), str(trackRadialBoxPanel.Value))
                trackRadialBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(trackRadialBoxPanelsElem)

        degreesBoxPanels = dialog.findChildren(DegreesBoxPanel)
        if len(degreesBoxPanels) > 0:
            degreesBoxPanelsElem = doc.createElement("DegreesBoxPanels")
            for degreesBoxPanel in degreesBoxPanels:
                elem = DataHelper.createNameValueElem(doc, "DegreesBoxPanel", degreesBoxPanel.objectName(), str(degreesBoxPanel.Value))
                degreesBoxPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(degreesBoxPanelsElem)

        mCAHPanels = dialog.findChildren(MCAHPanel)
        if len(mCAHPanels) > 0:
            mCAHPanelsElem = doc.createElement("MCAHPanels")
            for mCAHPanel in mCAHPanels:
                elem = DataHelper.createNameValueElem(doc, "MCAHPanel", mCAHPanel.objectName(), str(mCAHPanel.Value.Metres))
                mCAHPanelsElem.appendChild(elem)
                # newPanelExisting = True
            rootElem.appendChild(mCAHPanelsElem)

        oCAHPanels = dialog.findChildren(OCAHPanel)
        if len(oCAHPanels) > 0:
            oCAHPanelsElem = doc.createElement("OCAHPanels")
            for oCAHPanel in oCAHPanels:
                elem = DataHelper.createNameValueElem(doc, "OCAHPanel", oCAHPanel.objectName(), str(oCAHPanel.Value.Metres))
                oCAHPanelsElem.appendChild(elem)
            rootElem.appendChild(oCAHPanelsElem)

        allComboBoxs = dialog.findChildren(ComboBoxPanel)
        if len(allComboBoxs) > 0:
            comboBoxsElem = doc.createElement("ComboBoxPanels")
            for comboBox in allComboBoxs:
                elem = DataHelper.createNameValueElem(doc, "ComboBoxPanel", comboBox.objectName(), comboBox.SelectedIndex)
                comboBoxsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(comboBoxsElem)

        protectionAreaPanels = dialog.findChildren(ProtectionAreaPanel)
        if len(protectionAreaPanels) > 0:
            protectionAreaPanelsElem = doc.createElement("ProtectionAreaPanels")
            for protectionAreaPanel in protectionAreaPanels:
                elem = DataHelper.createNameValueElem(doc, "ProtectionAreaPanel", protectionAreaPanel.objectName(), protectionAreaPanel.SelectedIndex)
                protectionAreaPanelsElem.appendChild(elem)
                newPanelExisting = True
            rootElem.appendChild(protectionAreaPanelsElem)

        # tolerancePanels = dialog.findChildren(RnavTolerancesPanel)
        # if len(tolerancePanels) > 0:
        #     tolerancePanelsElem = doc.createElement("RnavTolerancesPanels")
        #     for tolerancePanel in tolerancePanels:
        #         val = str(tolerancePanel.ATT.Metres) + "," + str(tolerancePanel.XTT.Metres) + "," + str(tolerancePanel.ASW.Metres)
        #         elem = DataHelper.createNameValueElem(doc, "RnavTolerancesPanel", tolerancePanel.objectName(), val)
        #         tolerancePanelsElem.appendChild(elem)
        #         newPanelExisting = True
        #     rootElem.appendChild(tolerancePanelsElem)


        allLineEdits = dialog.findChildren(QLineEdit)

        if len(allLineEdits) > 0:
            textCtrlsElem = doc.createElement("QTextCtrls")
            for lineEdit in allLineEdits:
    #             parent = lineEdit.parent()
    #             if parent != dialog:
    #                 continue
                if lineEdit.text() == "":
                    continue
                lineEditWriteFlag = True
                parent0 = lineEdit.parent()
                while parent0 != None:
                    if isinstance(parent0, AltitudeBoxPanel) or \
                        isinstance(parent0, AngleGradientBoxPanel) or \
                        isinstance(parent0, DegreesBoxPanel) or \
                        isinstance(parent0, DistanceBoxPanel) or \
                        isinstance(parent0, MCAHPanel) or \
                        isinstance(parent0, NumberBoxPanel) or \
                        isinstance(parent0, OCAHPanel) or \
                        isinstance(parent0, PositionPanel) or \
                        isinstance(parent0, SpeedBoxPanel) or \
                        isinstance(parent0, TextBoxPanel) or \
                        isinstance(parent0, PositionPanel) or \
                        isinstance(parent0, TrackRadialBoxPanel):
                        lineEditWriteFlag = False
                        break
                    parent0 = parent0.parent()
                if not lineEditWriteFlag:
                    continue
                elem = DataHelper.createNameValueElem(doc, "QLineEdit", lineEdit.objectName(), lineEdit.text())
                textCtrlsElem.appendChild(elem)
            rootElem.appendChild(textCtrlsElem)



        allCheckBoxs = dialog.findChildren(QCheckBox)
        if len(allCheckBoxs) > 0:
            checkBoxsElem = doc.createElement("QCheckBoxs")
            for checkBox in allCheckBoxs:
                elem = DataHelper.createNameValueElem(doc, "QCheckBox", checkBox.objectName(), str(checkBox.isChecked()))
                checkBoxsElem.appendChild(elem)
            rootElem.appendChild(checkBoxsElem)


        allComboBoxs = dialog.findChildren(QComboBox)
        if len(allComboBoxs) > 0:
            comboBoxsElem = doc.createElement("QComboBoxs")
            for comboBox in allComboBoxs:
                elem = DataHelper.createNameValueElem(doc, "QComboBox", comboBox.objectName(), comboBox.currentIndex())
                comboBoxsElem.appendChild(elem)
            rootElem.appendChild(comboBoxsElem)



        
        allPositionPanels = dialog.findChildren(PositionPanel)
        if len(allPositionPanels) > 0:
            positionPanelsElem = doc.createElement("PositionPanels")
            for positionPanel in allPositionPanels:
                elem = DataHelper.createPositionPanelElem(doc, "PositionPanel", positionPanel)
                positionPanelsElem.appendChild(elem)
            rootElem.appendChild(positionPanelsElem)
        
        allTableViews = dialog.findChildren(QTableView)
        if len(allTableViews) > 0:
            tableElem = doc.createElement("QTableViews")
            for table in allTableViews:
                if  table.objectName() != "tblObstacles":
                    elem = DataHelper.createTableElem(doc, "QTableView", table)
                    tableElem.appendChild(elem)
            rootElem.appendChild(tableElem)
        
        if otherParameters != None:
            for data in otherParameters:
                name = data[0]
                dataElem = doc.createElement(name)
                for data0 in data[1]:
                    elem = DataHelper.createNameValueElem(doc, name + "0", data0[0], data0[1])
                    dataElem.appendChild(elem)
                rootElem.appendChild(dataElem)
        
        doc.appendChild(rootElem)
        qFile = QFile(fileName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            doc.save(textStream, 4)
            qFile.close()

            # ###CRC file is created.
            contents = None
            with open(fileName, 'rb', 0) as tempFile:
                contents = tempFile.read()
                tempFile.flush()
                tempFile.close()
            bytes = FasDataBlockFile.CRC_Calculation(contents)
            string_0 = QString(fileName)
            path = string_0.left(string_0.length() - 3) + "crc"
            fileStream = open(path, 'wb')
            fileStream.write(bytes)
            fileStream.close()

            # ###CRC file is created.
            # contents = None
            # with open(fileName, 'rb', 0) as tempFile:
            #     contents = tempFile.read()
            #     tempFile.flush()
            #     tempFile.close()
            # bytes = FasDataBlockFile.CRC_Calculation(contents)
            # string_0 = QString(fileName)
            # path = string_0.left(string_0.length() - 3) + "crc"
            # fileStream = open(path, 'wb')
            # fileStream.write(bytes)
            # fileStream.close()
        else:
            raise UserWarning, "can not open file:" + fileName
            
            
    @staticmethod
    def saveXmlDocToFile(fileName, doc):
        qFile = QFile(fileName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            doc.save(textStream, 4)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + fileName

            
    @staticmethod
    def loadXmlDocFromFile(fileName):
        doc = QDomDocument()
        qFile = QFile(fileName)
        if qFile.open(QFile.ReadOnly):
            doc.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + fileName
        return doc
        
        
    @staticmethod
    def loadInputParameters(fileName, dialog, otherParameterNames = None, resultOtherParameters = None):
        # contents = None
        # with open(fileName, 'rb', 0) as tempFile:
        #     contents = tempFile.read()
        #     tempFile.close()
        # bytes = FasDataBlockFile.CRC_Calculation(contents)
        #
        # string_0 = QString(fileName)
        # crcFileDir = string_0.left(string_0.length() - 3) + "crc"
        # crcFileContents = None
        # with open(crcFileDir, 'rb', 0) as tempFileCrc:
        #     crcFileContents = tempFileCrc.read()
        #     tempFileCrc.close()

        result = DlgCrcCheck.smethod_0(dialog, fileName)
        if not result:
            return

        doc = QDomDocument()
        qFile = QFile(fileName)
        if qFile.open(QFile.ReadOnly):
            doc.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + fileName
        dialogNodeList = doc.elementsByTagName(dialog.objectName())
        if dialogNodeList.isEmpty():
            raise UserWarning, "This file is not correct."
        dialogElem = dialogNodeList.at(0).toElement()

        positionPnlList = DataHelper.getNameValueListFromPositionPnlElem(dialogElem, "PositionPanel")
        for objectName, point3d in positionPnlList:
            try:
                positionPnlObj = dialog.findChild(PositionPanel, objectName)
                positionPnlObj.setPoint3D(point3d)
#                 comboBoxObj.setCurrentIndex(int(valueString))
            except:
                pass

        comboList = DataHelper.getNameValueListFromElem(dialogElem, "QComboBox")
        for objectName, valueString in comboList:
            try:
                comboBoxObj = dialog.findChild(QComboBox, objectName)
                parent = comboBoxObj.parent()
                writeAccept = True
                while not parent == None:
                    parent = parent.parent()
                    if isinstance(parent, ComboBoxPanel) or isinstance(parent, ProtectionAreaPanel):
                        writeAccept = False
                        break
                if writeAccept:
                    comboBoxObj.setCurrentIndex(int(valueString))
            except:
                pass

        checkList = DataHelper.getNameValueListFromElem(dialogElem, "QCheckBox")
        for objectName, valueString in checkList:
            try:
                checkBoxObj = dialog.findChild(QCheckBox, objectName)
                parent = checkBoxObj.parent()
                writeAccept = True
                while not parent == None:
                    parent = parent.parent()
                    if isinstance(parent, CheckBox):
                        writeAccept = False
                        break
                if writeAccept:
                    checkBoxObj.setChecked(True if(valueString == "True") else False)
            except:
                pass

        lineEditList = DataHelper.getNameValueListFromElem(dialogElem, "QLineEdit")
        for objectName, valueString in lineEditList:
            try:
                lineEditObj = dialog.findChild(QLineEdit, objectName)
                parent = lineEditObj.parent()
                writeAccept = True
                while not parent == None:
                    parent = parent.parent()
                    if isinstance(parent, PositionPanel) or isinstance(parent, TextBoxPanel)\
                            or isinstance(parent, NumberBoxPanel) or isinstance(parent, AltitudeBoxPanel)\
                            or isinstance(parent, MCAHPanel) or isinstance(parent, OCAHPanel)\
                            or isinstance(parent, AngleGradientBoxPanel) or isinstance(parent, DistanceBoxPanel)\
                            or isinstance(parent, TrackRadialBoxPanel) or isinstance(parent, DegreesBoxPanel)\
                            or isinstance(parent, SpeedBoxPanel):
                        writeAccept = False
                        break
                if writeAccept:
                    lineEditObj.setText(valueString)
            except:
                pass

        radioList = DataHelper.getNameValueListFromElem(dialogElem, "QRadioButton")
        for objectName, valueString in radioList:
            try:
                radioBtnObj = dialog.findChild(QRadioButton, objectName)
                radioBtnObj.setChecked(True if(valueString == "True") else False)
            except:
                pass

        # tolerancesPanelList = DataHelper.getNameValueListFromElem(dialogElem, "RnavTolerancesPanel")
        # for objectName, valueString in tolerancesPanelList:
        #     try:
        #         tolerancesPanelObj = dialog.findChild(RnavTolerancesPanel, objectName)
        #         valueString = QString(valueString)
        #         strList = valueString.split(",")
        #         tolerancesPanelObj.txtAtt.setText(strList[0])
        #         tolerancesPanelObj.txtXtt.setText(strList[1])
        #         tolerancesPanelObj.txtAsw.setText(strList[2])
        #     except:
        #         pass

        comboBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "ComboBoxPanel")
        for objectName, valueString in comboBoxPanelList:
            try:
                comboBoxPanelObj = dialog.findChild(ComboBoxPanel, objectName)
                comboBoxPanelObj.SelectedIndex = int(valueString)
            except:
                pass
        textBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "TextBoxPanel")
        for objectName, valueString in textBoxPanelList:
            try:
                textBoxPanelObj = dialog.findChild(TextBoxPanel, objectName)
                textBoxPanelObj.Value = valueString
            except:
                pass



        numberBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "NumberBoxPanel")
        for objectName, valueString in numberBoxPanelList:
            try:
                numberBoxPanelObj = dialog.findChild(NumberBoxPanel, objectName)
                numberBoxPanelObj.Value = float(valueString)
            except:
                pass

        altitudeBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "AltitudeBoxPanel")
        for objectName, valueString in altitudeBoxPanelList:
            try:
                altitudeBoxPanelObj = dialog.findChild(AltitudeBoxPanel, objectName)
                altitudeBoxPanelObj.Value = Altitude(float(valueString))
            except:
                pass

        distanceBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "DistanceBoxPanel")
        for objectName, valueString in distanceBoxPanelList:
            try:
                distanceBoxPanelObj = dialog.findChild(DistanceBoxPanel, objectName)
                distanceBoxPanelObj.Value = Distance(float(valueString))
            except:
                pass

        speedBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "SpeedBoxPanel")
        for objectName, valueString in speedBoxPanelList:
            try:
                speedBoxPanelObj = dialog.findChild(SpeedBoxPanel, objectName)
                speedBoxPanelObj.Value = Speed(float(valueString))
            except:
                pass

        trackRadialBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "TrackRadialBoxPanel")
        for objectName, valueString in trackRadialBoxPanelList:
            try:
                trackRadialBoxPanelObj = dialog.findChild(TrackRadialBoxPanel, objectName)
                trackRadialBoxPanelObj.Value = float(valueString)
            except:
                pass

        degreesBoxPanelList = DataHelper.getNameValueListFromElem(dialogElem, "DegreesBoxPanel")
        for objectName, valueString in degreesBoxPanelList:
            try:
                degreesBoxPanelObj = dialog.findChild(DegreesBoxPanel, objectName)
                degreesBoxPanelObj.Value = float(valueString)
            except:
                pass

        mCAHPanelList = DataHelper.getNameValueListFromElem(dialogElem, "MCAHPanel")
        for objectName, valueString in mCAHPanelList:
            try:
                mCAHPanelObj = dialog.findChild(MCAHPanel, objectName)
                mCAHPanelObj.Value = Altitude(float(valueString))
            except:
                pass

        oCAHPanelList = DataHelper.getNameValueListFromElem(dialogElem, "OCAHPanel")
        for objectName, valueString in oCAHPanelList:
            try:
                oCAHPanelObj = dialog.findChild(OCAHPanel, objectName)
                oCAHPanelObj.Value = Altitude(float(valueString))
            except:
                pass



        checkList = DataHelper.getNameValueListFromElem(dialogElem, "CheckBox")
        for objectName, valueString in checkList:
            try:
                checkBoxObj = dialog.findChild(CheckBox, objectName)
                checkBoxObj.Checked = True if(valueString == "True") else False
            except:
                pass

        protectionAreaPanelList = DataHelper.getNameValueListFromElem(dialogElem, "ProtectionAreaPanel")
        for objectName, valueString in protectionAreaPanelList:
            try:
                protectionAreaPanelObj = dialog.findChild(ProtectionAreaPanel, objectName)
                protectionAreaPanelObj.SelectedIndex = int(valueString)
            except:
                pass
        positionPnlList = DataHelper.getNameValueListFromPositionPnlElem(dialogElem, "PositionPanel")
        for objectName, point3d in positionPnlList:
            try:
                positionPnlObj = dialog.findChild(PositionPanel, objectName)
                positionPnlObj.setPoint3D(point3d)
#                 comboBoxObj.setCurrentIndex(int(valueString))
            except:
                pass
            

        
        if otherParameterNames != None:
            for name in otherParameterNames:
                checkList = DataHelper.getNameValueListFromElem(dialogElem, name + "0")
                for objName, data in checkList:
                    resultOtherParameters.append((objName, data))
        positionPnlList = DataHelper.loadDataFromTableElem(dialog, QTableView, dialogElem, "QTableView")
        
    @staticmethod
    def loadDataFromTableElem(dialog, tableClass, dialogElem, tagName):
        ctrlNodesList = dialogElem.elementsByTagName(tagName)
        for i in range(ctrlNodesList.count()):
            try:
                tableElem = ctrlNodesList.at(i).toElement()
                objectNameNode = tableElem.elementsByTagName("ObjectName").at(0)
                objectNameElem = objectNameNode.toElement()
                objectName = objectNameElem.text()
                tableViewObj = dialog.findChild(tableClass, objectName)
                if tableViewObj == None:
                    continue
                tableModel = tableViewObj.model()
                recordNodesList = tableElem.elementsByTagName("record")
                for j in range(recordNodesList.count()):
                    recordElem = recordNodesList.at(j).toElement()
                    tableModel.insertRow(j)
                    columnsNodeList = recordElem.elementsByTagName("column")
                    for k in range(columnsNodeList.count()):
                        columnElem = columnsNodeList.at(k).toElement()
                        columnValue = columnElem.text()
                        tableModel.setData(tableModel.index(j, k), QVariant(columnValue))
                    
            except:
                pass
        
    @staticmethod
    def getNameValueListFromElem(elem, controlType):
        lst = []
        ctrlNodesList = elem.elementsByTagName(controlType)
        for i in range(ctrlNodesList.count()):
            try:
                lineEditElem = ctrlNodesList.at(i).toElement()
                objectNameNode = lineEditElem.elementsByTagName("ObjectName").at(0)
                objectNameElem = objectNameNode.toElement()
                objectName = objectNameElem.text()
                valueElem = objectNameNode.nextSiblingElement()
                valueString = valueElem.text()
                lst.append((objectName, valueString))
            except:
                pass
        return lst
    
    
    @staticmethod
    def getPointValueFromElem(elem):
        try:
            elemX = elem.elementsByTagName("X").at(0).toElement()
            elemY = elem.elementsByTagName("Y").at(0).toElement()
            return float(elemX.text()), float(elemY.text())
        except BaseException as e:
            raise UserWarning, "Position Element is incorrect!\n" + e.message
    
#     @staticmethod
#     def getNameValueListFromTableViewElem(elem, controlType):
#         lst = []
#         ctrlNodesList = elem.elementsByTagName(controlType)
#         for i in range(ctrlNodesList.count()):
#             try:
#                 tableViewElem = ctrlNodesList.at(i).toElement()
#                 objectNameNode = tableViewElem.elementsByTagName("ObjectName").at(0)
#                 objectNameElem = objectNameNode.toElement()
#                 objectName = objectNameElem.text()
#                 recordNodeList = tableViewElem.elementsByTagName("record")
#                 recordStrValue = []
#                 if recordNodeList.count() > 0:
#                     for i in range(recordNodeList.count()):
#                         recordNode = recordNodeList.item(i)
#                         recordElement = recordNode.toElement()
#                         colNodList = recordElement.elementsByTagName("column")
#                         colStrValue = []
#                         if colNodList.count() > 0:
#                             for j in range(colNodList.count()):
#                                 colNode = colNodList.item(j)
#                                 colElement = colNode.toElement()
#                                 colStrValue.append(colElement.text())
#                         
#                 xElem = objectNameNode.nextSiblingElement()
#                 xString = xElem.text()
#                 yElem = xElem.nextSiblingElement()
#                 yString = yElem.text()
#                 zElem = yElem.nextSiblingElement()
#                 if zElem.text() != "":
#                     zString = zElem.text()
#                 else:
#                     zString = "0"
#                 point3d = Point3D(float(xString), float(yString), float(zString))
#                 lst.append((objectName, point3d))
#             except:
#                 pass
#         return lst
#     
    
    @staticmethod
    def getNameValueListFromPositionPnlElem(elem, controlType):
        lst = []
        ctrlNodesList = elem.elementsByTagName(controlType)
        for i in range(ctrlNodesList.count()):
            try:
                lineEditElem = ctrlNodesList.at(i).toElement()
                objectNameNode = lineEditElem.elementsByTagName("ObjectName").at(0)
                objectNameElem = objectNameNode.toElement()
                objectName = objectNameElem.text()
                idElem = objectNameNode.nextSiblingElement()
                idString = idElem.text()
                xElem = idElem.nextSiblingElement()
                xString = xElem.text()
                yElem = xElem.nextSiblingElement()
                yString = yElem.text()
                zElem = yElem.nextSiblingElement()
                if zElem.text() != "":
                    zString = zElem.text()
                else:
                    zString = "0"
                point3d = Point3D(float(xString), float(yString), float(zString))
                point3d.ID = idString
                lst.append((objectName, point3d))
            except:
                pass
        return lst
    
    @staticmethod
    def saveExportResult(fileName, strDlgName, tblView, filterList, ParameterList, resultHideColumnIndexs = None, subName = "Checked Obstacles"):
        # xml init

#         
        model = tblView.model()
        xmlDoc = QDomDocument()
        strType = DataHelper.filterTagName(strDlgName)
        rootElem = xmlDoc.createElement(strType)
        xmlDeclaration = xmlDoc.createProcessingInstruction( "xml", "version=\"1.0\" encoding=\"utf-8\"" )
        xmlDoc.appendChild( xmlDeclaration ) 
        
        strFullName = QFileInfo(fileName)
        strXmlName = strFullName.fileName()
        strXslName = strXmlName[:len(strXmlName)-4] + ".xsl"
        xmlDeclaration_1 = xmlDoc.createProcessingInstruction( "xml-stylesheet", "type='text/xsl' href='" + strXslName + "'" )
        xmlDoc.appendChild( xmlDeclaration_1 )
#         parameter table

        if len(ParameterList) > 0:
            paramElem = xmlDoc.createElement("Parameters")
            fieldElem = None
            for id,value in ParameterList:
                if value == "group":

                    fieldElem = xmlDoc.createElement(DataHelper.filterTagName(id))
    #                 fieldElem.appendChild(xmlDoc.createTextNode(id))
                    paramElem.appendChild(fieldElem)
                    continue

                recordElem = xmlDoc.createElement("ParameterRecord")
                columElem = xmlDoc.createElement("ObjectName")
                columElem.appendChild(xmlDoc.createTextNode(id))
                recordElem.appendChild(columElem)
                columElem = xmlDoc.createElement("Value")
                if isinstance(value, int) or isinstance(value, float):
                    value = str(value)
                if value == None:
                    value = ""
                columElem.appendChild(xmlDoc.createTextNode(value))
                recordElem.appendChild(columElem)
                fieldElem.appendChild(recordElem)

            rootElem.appendChild(paramElem)
        
#         ExportObstacles table
        exportObElem = xmlDoc.createElement("ExportObstacles")
        if filterList != None:
            for strFliter in filterList:                
                model.setFilterFixedString(strFliter)
                strName = DataHelper.filterTagName(strFliter)
                strTableTagName = strType + "CheckedObstacles" + strName
                tableElem = DataHelper.createObstacleTableElem(xmlDoc, strTableTagName, model, tblView, strFliter, resultHideColumnIndexs)
                exportObElem.appendChild(tableElem)
        else:
            strTableTagName = strType + "CheckedObstacles" 
            tableElem = DataHelper.createObstacleTableElem(xmlDoc, strTableTagName, model, tblView, None, resultHideColumnIndexs)
            exportObElem.appendChild(tableElem)
        rootElem.appendChild(exportObElem)
        xmlDoc.appendChild(rootElem)        
        
        strXmlFileName = fileName[:len(fileName)-4] + ".xml" 
        xmlFNameInfo = QFileInfo(strXmlFileName)
        xmlName = xmlFNameInfo.fileName()
        qFile = QFile(fileName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            xmlDoc.save(textStream, 4)
            qFile.close()

            ###CRC file is created.
            contents = None
            with open(strXmlFileName, 'rb', 0) as tempFile:
                contents = tempFile.read()
                tempFile.flush()
                tempFile.close()
            bytes = FasDataBlockFile.CRC_Calculation(contents)
            string_0 = QString(strXmlFileName)
            path = string_0.left(string_0.length() - 3) + "crc"
            fileStream = open(path, 'wb')
            fileStream.write(bytes)
            fileStream.close()
        else:
            raise UserWarning, "can not open file:" + fileName
        
        
        # xslt make
        xsltDoc = QDomDocument()                          
#             // Create XML document contained calculation results.
#             // Create a processing instruction targeted for xml.
        xmlDeclaration = xsltDoc.createProcessingInstruction( "xml", "version=\"1.0\"" )
        xsltDoc.appendChild( xmlDeclaration )          
          
        peStyleSheet = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:stylesheet" )
        peStyleSheet.setAttribute("version", "1.0")
        
        peTemplate = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:template" )
        peTemplate.setAttribute("match", "/")
          
        peHtml = xsltDoc.createElement("html")
        peHtml.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")
        # header tag
        pdfHead = xsltDoc.createDocumentFragment()
#         
        peTag = xsltDoc.createElement("meta")
        peTag.setAttribute("http-equiv", "Content-Type")
        peTag.setAttribute("content", "'text/html; charset=utf-8'")
          
        pdfHead.appendChild(peTag)
        peTag = xsltDoc.createElement("title")
        peTag.appendChild(xsltDoc.createTextNode("StyleSheet"))
        pdfHead.appendChild(peTag)
        peTag = xsltDoc.createElement("Head")
        peTag.appendChild(pdfHead)
        pdfHead = xsltDoc.createDocumentFragment()
        pdfHead.appendChild(peTag)
#         peHtml.appendChild(pdfHead)
          
        # body tag
        peBody = xsltDoc.createElement("body")
        pdfBody = xsltDoc.createDocumentFragment()
        
        peTitle = xsltDoc.createElement("div")
        peTitle.setAttribute("align", "center")
        peTag = xsltDoc.createElement("h2")
        peTag.appendChild(xsltDoc.createTextNode(strDlgName))
        peTitle.appendChild(peTag)
        pdfBody.appendChild(peTitle)



        # parameter Table make
        if len(ParameterList) > 0:
            peTable = xsltDoc.createElement("table")
            peTable.setAttribute("width", "50%")
            peTable.setAttribute("border", "1")
            peTable.setAttribute("align", "center")

            for id, value in ParameterList:
                if value == "group":
                    peTR = xsltDoc.createElement("tr")
                    peTd = xsltDoc.createElement("td")
                    peTd.setAttribute("colspan", 2)
                    peTag = xsltDoc.createElement("h4")
                    peTag.appendChild(xsltDoc.createTextNode(id))
    #         peTitle.appendChild(peTag)
    #                 peFieldLValue = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:value-of")
    #                 strField = dialog.objectName() + "/Parameters/" + DataHelper.filterTagName(id)
    #                 peFieldLValue.setAttribute("select", strField)
                    peTd.appendChild(peTag)
                    peTR.appendChild(peTd)
                    peTable.appendChild(peTR)

                    peTR = xsltDoc.createElement("tr")
                    peTd = xsltDoc.createElement("td")
                    peTd.setAttribute("style", "padding-left:20px;")
                    petdValue = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:value-of")
                    petdValue.setAttribute("select", "ObjectName")
                    peTd.appendChild(petdValue)
                    peTR.appendChild(peTd)
                    peTd = xsltDoc.createElement("td")
                    petdValue = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:value-of")
                    petdValue.setAttribute("select", "Value")
                    peTd.appendChild(petdValue)
                    peTR.appendChild(peTd)

                    peParamForEach = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:for-each")
                    strSelect = DataHelper.filterTagName(strDlgName) + "/Parameters/" + DataHelper.filterTagName(id) + "/ParameterRecord"
                    peParamForEach.setAttribute("select", strSelect)
                    peParamForEach.appendChild(peTR)
                    peTable.appendChild(peParamForEach)

            pdfBody.appendChild(peTable)
        
#         obstacle Table
#         tblView = dialog.ui.tblObstacles
        wstrTableName = ""
        if filterList != None:
            for strFilter in filterList:
                wstrTableName = strDlgName + "-" + subName + "-" + strFilter
                peDiv = xsltDoc.createElement("div")
                peDiv.setAttribute("align", "center")
                
                peTag = xsltDoc.createElement("h2")
                peTag.appendChild(xsltDoc.createTextNode(wstrTableName))
                peDiv.appendChild(peTag)
                pdfBody.appendChild(peDiv)
                
    #                     // <Table>
                peTable = xsltDoc.createElement("table")
                peTable.setAttribute("width", "90%")
                peTable.setAttribute("border", "1")
                peTable.setAttribute("align", "center")
                pdfTable = xsltDoc.createDocumentFragment()            
                
    #                     // table header write
                pdfTR = xsltDoc.createDocumentFragment()
                j = -1                   
                for strField in model.fixedColumnLabels:
                    j += 1
                    flag = False
                    for k in range(len(resultHideColumnIndexs)):
                        if j == resultHideColumnIndexs[k]:
                            flag = True
                            break
                    if flag:
#                     if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
                            continue
                    peTH = xsltDoc.createElement("th")
                    peTH.appendChild(xsltDoc.createTextNode(strField))
                    peTH.setAttribute("scope", "col")
                    pdfTR.appendChild(peTH)
                    
                peTR = xsltDoc.createElement("tr")
                peTR.appendChild(pdfTR)
                pdfTable.appendChild(peTR)
                
    #             // table header end
    # //////////////////////////////////////////////////////////////////////////
    #             // <xsl:for-each select="Root/ProjectList/Project">
                pdfTR = xsltDoc.createDocumentFragment()
                j = -1
                for strField in model.fixedColumnLabels:
                    j += 1
                    flag = False
                    for k in range(len(resultHideColumnIndexs)):
                        if j == resultHideColumnIndexs[k]:
                            flag = True
                            break
                    if flag:
#                     if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
                        continue
    #                 // <td>
                    peTH = xsltDoc.createElement("td")
                    peDiv = xsltDoc.createElement("div")
                    peXSLValue = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:value-of")
                    peXSLValue.setAttribute("select", DataHelper.filterTagName(strField))
                    peDiv.appendChild(peXSLValue)
                    
                    peDiv.setAttribute("align", "center")
                    peTH.appendChild(peDiv)
                    pdfTR.appendChild(peTH)
                    
    #                         // </td>
                peTR = xsltDoc.createElement("tr")
                peTR.appendChild(pdfTR)
                
                peXSLForEach = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:for-each")
                peXSLForEach.appendChild(peTR)
                strSelect = DataHelper.filterTagName(strDlgName) + "/ExportObstacles/" + strType + "CheckedObstacles" + DataHelper.filterTagName(strFilter) +"/record"
                peXSLForEach.setAttribute("select", strSelect)
                
                pdfTable.appendChild(peXSLForEach)
                
    #                     // </xsl:for-each>
                peTable.appendChild(pdfTable)
                
                pdfBody.appendChild(peTable)
        else:
            wstrTableName = strDlgName + "-" + subName
            peDiv = xsltDoc.createElement("div")
            peDiv.setAttribute("align", "center")
            
            peTag = xsltDoc.createElement("h2")
            peTag.appendChild(xsltDoc.createTextNode(wstrTableName))
            peDiv.appendChild(peTag)
            pdfBody.appendChild(peDiv)
            
#                     // <Table>
            peTable = xsltDoc.createElement("table")
            peTable.setAttribute("width", "90%")
            peTable.setAttribute("border", "1")
            peTable.setAttribute("align", "center")
            pdfTable = xsltDoc.createDocumentFragment()            
            
#                     // table header write
            pdfTR = xsltDoc.createDocumentFragment()
            j = -1
            labels = []
            try:
                labels = model.fixedColumnLabels
            except:
                for i in range(model.columnCount()):
                    if model.horizontalHeaderItem(i) == None or model.horizontalHeaderItem(i).text() == "#" or model.horizontalHeaderItem(i).text() == "":
                        continue
                    else:
                        labels.append(model.horizontalHeaderItem(i).text())
            for strField in labels:
                j += 1
                flag = False
                for k in range(len(resultHideColumnIndexs)):
                    if j == resultHideColumnIndexs[k]:
                        flag = True
                        break
                if flag:
#                 if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
                        continue
                peTH = xsltDoc.createElement("th")
                peTH.appendChild(xsltDoc.createTextNode(strField))
                peTH.setAttribute("scope", "col")
                pdfTR.appendChild(peTH)
                
            peTR = xsltDoc.createElement("tr")
            peTR.appendChild(pdfTR)
            pdfTable.appendChild(peTR)
            
#             // table header end
# //////////////////////////////////////////////////////////////////////////
#             // <xsl:for-each select="Root/ProjectList/Project">
            pdfTR = xsltDoc.createDocumentFragment()
            j = -1
            for strField in labels:
                j += 1
                flag = False
                for k in range(len(resultHideColumnIndexs)):
                    if j == resultHideColumnIndexs[k]:
                        flag = True
                        break
                if flag:
#                 if tblView.isColumnHidden(j) and j !=3 and j !=4 and j !=5 and j !=6:
                    continue
#                 // <td>
                peTH = xsltDoc.createElement("td")
                peDiv = xsltDoc.createElement("div")
                peXSLValue = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:value-of")
                peXSLValue.setAttribute("select", DataHelper.filterTagName(strField))
                peDiv.appendChild(peXSLValue)
                
                peDiv.setAttribute("align", "center")
                peTH.appendChild(peDiv)
                pdfTR.appendChild(peTH)
                
#                         // </td>
            peTR = xsltDoc.createElement("tr")
            peTR.appendChild(pdfTR)
            
            peXSLForEach = xsltDoc.createElementNS("http://www.w3.org/1999/XSL/Transform", "xsl:for-each")
            peXSLForEach.appendChild(peTR)
            strSelect = DataHelper.filterTagName(strDlgName) + "/ExportObstacles/" + strType + "CheckedObstacles"  +"/record"
            peXSLForEach.setAttribute("select", strSelect)
            
            pdfTable.appendChild(peXSLForEach)
            
#                     // </xsl:for-each>
            peTable.appendChild(pdfTable)
            
            pdfBody.appendChild(peTable)
#                     // <Table> End
        peBody.appendChild(pdfBody)
        pdfHead.appendChild(peBody)
#                         // <body> End

        peHtml.appendChild(pdfHead)
        peTemplate.appendChild(peHtml)
        peStyleSheet.appendChild(peTemplate)
        xsltDoc.appendChild(peStyleSheet)

         
        strXslFileName = fileName[:len(fileName)-4] + ".xsl"
        qFile = QFile(strXslFileName)
        if qFile.open(QFile.WriteOnly):
            textStream = QTextStream(qFile)
            xsltDoc.save(textStream, 4)
            qFile.close()


        else:
            raise UserWarning, "can not open file:" + fileName

    @staticmethod
    def filterTagName(tagName):
        strName = tagName
#         if "(" in tagName:
        strName = strName.replace("(", "")
        strName = strName.replace(")", "")
        strName = strName.replace(" ", "")
        strName = strName.replace(".", "")
        strName = strName.replace("/", "")
        strName = strName.replace("*", "")
        strName = strName.replace("-", "")
        strName = strName.replace("'", "")
        strName = strName.replace(define._degreeStr, "")
        
        return strName
    
    @staticmethod
    def pnlPositionParameter(pnlPosition, parameterLst):
        if define._units == QGis.Meters:
            position = pnlPosition.Point3d
            positionDegree = QgisHelper.Meter2DegreePoint3D(position)
        elif define._units == QGis.DecimalDegrees:
            positionDegree = pnlPosition.Point3d
            position = QgisHelper.Degree2MeterPoint3D(positionDegree)
        parameterLst.append(("X", str(position.x())))
        parameterLst.append(("Y", str(position.y())))
        parameterLst.append(("Lat", pnlPosition.txtLat.Value))
        parameterLst.append(("Lon", pnlPosition.txtLong.Value))
        if not pnlPosition.frameAltitude.isHidden():
            parameterLst.append(("Altitude", pnlPosition.txtAltitudeM.text() + " m/" + pnlPosition.txtAltitudeFt.text() + " ft"))
    @staticmethod
    def strPnlPositionParameter(strX, strY, parameterLst):
        if define._units == QGis.Meters:
            parameterLst.append(("X", strX))
            parameterLst.append(("Y", strY))
            position = Point3D(float(strX), float(strY), 0)
            positionDegree = QgisHelper.Meter2DegreePoint3D(position)        
            parameterLst.append(("Lat", QgisHelper.strDegree(positionDegree.y())))
            parameterLst.append(("Lon", QgisHelper.strDegree(positionDegree.x())))
        elif define._units == QGis.DecimalDegrees:
            parameterLst.append(("Lat", strY))
            parameterLst.append(("Lon", strX))
            position = Point3D(float(strX), float(strY), 0)
            positionDegree = QgisHelper.Degree2MeterPoint3D(position)        
            parameterLst.append(("x", str(positionDegree.x())))
            parameterLst.append(("y", str(positionDegree.y())))
        