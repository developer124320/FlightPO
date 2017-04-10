
'''
Created on 25 May 2014

@author: Administrator
'''
from PyQt4.QtGui import QProgressBar, QApplication
from PyQt4.QtCore import Qt, QFile, QDateTime
from PyQt4.QtXml import QDomDocument
from FlightPlanner.types import AltitudeUnits, DegreesType, ProcEntityParseNodeType,\
                                  DataBaseCoordinateType, AngleGradientSlopeUnits, CodeCatAcftAixm, CodeTypeSidAixm,\
    CodeTypeStarAixm, CodeTypeIapAixm, CodeTypeHoldProcAixm, CodeTypeApchAixm, CodeRefOchAixm, CodePhaseProcAixm, CodeTypeProcPathAixm,\
    CodeTypeCourseAixm, CodeTypeFlyByAixm, CodeDirTurnAixm, CodeDescrDistVerAixm, CodeDistVerAixm, CodeSpeedRefAixm, CodeRepAtcAixm,\
    CodeIapFixAixm, CodeLegTypeAixm, CodePathTypeAixm
from FlightPlanner.helpers import Altitude, Distance, Speed, EnumHelper
from FlightPlanner.Captions import Captions
from Type.Degrees import Degrees
from Type.DataBase import DataBaseCoordinate, DataBaseCoordinates
from Type.Symbol import SymbolAttributes
from Type.DataBase import DataBase, DataBaseIapOcaOchs, DataBaseIapOcaOch
from Type.DataBaseProcedureLegs import DataBaseProcedureLegs, DataBaseProcedureLegsEx, DataBaseProcedureLegEx, DataBaseProcedureLeg
import define
from FlightPlanner.types import SymbolType
from FlightPlanner.messages import Messages

import  math




class DataBaseLoaderAixm:
    def __init__(self, fileName = None, bool_0 = None):
        dateTime = None
        num = None
        self.dataBase = None;

        self.includeProcedureData = bool_0;
        if bool_0 == None or bool_0:
            return

        self.pointData = []
        self.pointDataObstacles = []
        self.pointDataRoutes = []
        self.pointDataAirspace = []
        self.pointDataBorder = []

        doc = QDomDocument()
        qFile = QFile(fileName)
        if qFile.open(QFile.ReadOnly):
            doc.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + fileName

        progressMessageBar = define._messagBar.createMessage("Reding xml file...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        self.progress.setMaximum(100)
        if bool_0:
            nodes = doc.elementsByTagName("AIXM-Snapshot")
            if (self.method_20(doc.elementsByTagName("Vor") )):
                pass
        elif (self.method_3(doc.elementsByTagName("Ahp"))):
            self.progress.setValue(6)
            QApplication.processEvents()
            if (self.method_4(doc.elementsByTagName("Rcp"))):
                self.progress.setValue(12)
                QApplication.processEvents()
                if (self.method_5(doc.elementsByTagName("Rdn"))):
                    self.progress.setValue(18)
                    QApplication.processEvents()
                    if (self.method_6(doc.elementsByTagName("Dpn"))):
                        self.progress.setValue(24)
                        QApplication.processEvents()
                        if (self.method_7(doc.elementsByTagName("Vor"))):
                            self.progress.setValue(30)
                            QApplication.processEvents()
                            if (self.method_8(doc.elementsByTagName("Tcn"))):
                                self.progress.setValue(36)
                                QApplication.processEvents()
                                if (self.method_9(doc.elementsByTagName("Dme"))):
                                    self.progress.setValue(42)
                                    QApplication.processEvents()
                                    if (self.method_11(doc.elementsByTagName("Mkr"))):
                                        self.progress.setValue(48)
                                        QApplication.processEvents()
                                        if (self.method_12(doc.elementsByTagName("Sns"))):
                                            self.progress.setValue(54)
                                            QApplication.processEvents()
                                            if (self.method_13(doc.elementsByTagName("Ils"))):
                                                self.progress.setValue(60)
                                                QApplication.processEvents()
                                                if (self.method_14(doc.elementsByTagName("Mls"))):
                                                    self.progress.setValue(66)
                                                    QApplication.processEvents()
                                                    if (self.method_15(doc.elementsByTagName("Obs"))):
                                                        self.progress.setValue(72)
                                                        QApplication.processEvents()
                                                        if (self.method_16(doc.elementsByTagName("Rsg"))):
                                                            self.progress.setValue(80)
                                                            QApplication.processEvents()
                                                            if (self.method_17(doc.elementsByTagName("Ase"))):
                                                                self.progress.setValue(86)
                                                                QApplication.processEvents()
                                                                if (self.method_18(doc.elementsByTagName("Abd"))):
                                                                    self.progress.setValue(95)
                                                                    QApplication.processEvents()
                                                                    if (self.method_19(doc.elementsByTagName("Gbr"))):
                                                                        self.progress.setValue(100)
                                                                        QApplication.processEvents()
                                                                        pass
        self.progress.setValue(100)
        define._messagBar.hide()

#         print element.text()
#         print "sdfadsgad"
    
    def method_1(self, string_0, bool_0):
        # self.method_2();
        self.includeProcedureData = bool_0;
        self.dataBase = DataBase(string_0);
        self.worker_DoWork();
    def method_3(self, xmlNodeList_0):
        flag = None;
        resultPoint = []
        altitude_metre = None
        if (xmlNodeList_0 != None and xmlNodeList_0.count() > 0):
#             IEnumerator enumerator = xmlNodeList_0.GetEnumerator();
            count = xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = [];
                innerText = None;
                str0 = None;
                xmlNodes = current.namedItem("AhpUid");
                if (not xmlNodes.isNull()):
                    node = xmlNodes.namedItem("codeId");
                    symbolAttribute.append(node.toElement().text())
                    pass
                xmlNodes = current.namedItem("geoLat");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.toElement().text(), DegreesType.Latitude).value));
                xmlNodes = current.namedItem("geoLong");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.toElement().text(), DegreesType.Longitude).value));
                xmlNodes = current.namedItem("OrgUid");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(xmlNodes.namedItem("txtName").toElement().text());
                xmlNodes = current.namedItem("txtName");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(xmlNodes.toElement().text());
                xmlNodes = current.namedItem("valElev");
                if (not xmlNodes.isNull()):
                    innerText = xmlNodes.toElement().text();
                xmlNodes = current.namedItem("uomDistVer");
                if (not xmlNodes.isNull()):
                    str0 = xmlNodes.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
#                         symbolAttribute.append(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
#                         symbolAttribute.append(Altitude(float(innerText)).Metres)
                else:
                    altitude_metre = "0.0"
#                     symbolAttribute.append(0)


                xmlNodes = current.namedItem("valMagVar");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR + ")");
                xmlNodes = current.namedItem("dateMagVar");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR_DATE + ")");
                xmlNodes = current.namedItem("dateMagVarChg");
                if (not xmlNodes.isNull()):
                    symbolAttribute.append(xmlNodes.toElement().text() + " (" + Captions.MAGN_VAR_ANNUAL_CHANGE + ")");
#                 self.dataBase.method_1(symbolAttribute[0], Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude), Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude), Altitude.smethod_4(innerText, str), new Symbol(SymbolType.Arp), symbolAttribute);

                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Arp])
#             print self.pointData
            return True;
        return True;
    def method_4(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("RcpUid");
                xmlNodes1 = xmlNodes.namedItem("RwyUid");
                xmlNodes2 = xmlNodes1.namedItem("AhpUid");
                symbolAttribute.append(Captions.RWY_BIG + " " + xmlNodes1.namedItem("txtDesig").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
#                     symbolAttribute.append(xmlNodes.namedItem("geoLat").toElement().text());
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text());
                symbolAttribute.append(xmlNodes2.namedItem("codeId").toElement().text());
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Default])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;

    def method_5(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("RdnUid");
                xmlNodes1 = xmlNodes.namedItem("RwyUid").namedItem("AhpUid");
                symbolAttribute.append(Captions.THR_BIG + " " + Captions.RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text());
                xmlNodes2 = current.namedItem("geoLat")
                if xmlNodes2.toElement().text() == "":
                    continue
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.toElement().text(), DegreesType.Latitude).value));
                if current.namedItem("geoLong").toElement().text() == "":
                    continue
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
#                     symbolAttribute.append(xmlNodes.namedItem("geoLat").toElement().text());
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text());
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text());
                xmlNodes3 = current.namedItem("valElevTdz");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomElevTdz");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Default])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;

    def method_6(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("DpnUid");
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                symbolAttribute.append(current.namedItem("codeType").toElement().text());
#                     symbolAttribute.append(xmlNodes.namedItem("geoLong").toElement().text());

                xmlNodes1 = current.namedItem("txtName");
                if (not xmlNodes1.isNull()):
                    symbolAttribute.append(xmlNodes1.toElement().text());
                xmlNodes3 = current.namedItem("txtRmk");
                if (not xmlNodes3.isNull()):
                    symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("valCrc");
                if (not xmlNodes3.isNull()):
                    symbolAttribute.append(xmlNodes3.toElement().text());
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                symbolType = SymbolType.Repnc
                if symbolAttribute[4].count("FAF") > 0:
                    symbolType = SymbolType.Faf
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], "", attr, symbolType])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;


    def method_7(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("VorUid");
                xmlNodes1 = xmlNodes.namedItem("OrgUid")
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text());
                xmlNodes2 = current.namedItem("valFreq");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text());

                xmlNodes2 = current.namedItem("uomFreq");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text());
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("txtName");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("valMagVar");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("dateMagVar");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text());
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                symbolType = SymbolType.Vor

                xmlNodes2 = current.namedItem("codeType");
                codeTypeStr = xmlNodes2.toElement().text()
                if xmlNodes2 != None and codeTypeStr.count("DVOR") > 0:
                    symbolType = SymbolType.Vord
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, symbolType])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;

    def method_8(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("TcnUid");
                xmlNodes1 = current.namedItem("VorUid");
                xmlNodes2 = current.namedItem("OrgUid");
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text());
                xmlNodes3 = current.namedItem("codeChannel");
                if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                    symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text());
                if xmlNodes1 != None and xmlNodes1.toElement().text() != "":
                    symbolAttribute.append(Captions.COLLOCATED_WITH + " " + symbolAttribute[0]);
                    s = symbolAttribute[0]
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0, xmlNodes1.namedItem("codeId").toElement().text());
                    xmlNodes3 = current.namedItem("codeChannel");
                    if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                        symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text());
                    xmlNodes3 = current.namedItem("txtName");
                    if (not xmlNodes3.isNull()):
                        symbolAttribute.append(xmlNodes3.toElement().text());

                xmlNodes3 = current.namedItem("txtName");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 5:
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("valMagVar");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 6:
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("dateMagVar");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, s + " (" + xmlNodes3.toElement().text() + ")")
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("txtRmk");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 7:
                        symbolAttribute.pop(7)
                        symbolAttribute.insert(7, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());

                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Tacan])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;

    def method_9(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
#             try:
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("DmeUid");
                xmlNodes1 = current.namedItem("VorUid");
                xmlNodes2 = current.namedItem("OrgUid");
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text());
                xmlNodes3 = current.namedItem("codeChannel");
                if (not xmlNodes3.isNull()):
                    symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text());
                if xmlNodes1 != None:
                    symbolAttribute.append(Captions.COLLOCATED_WITH + " " + symbolAttribute[0]);
                    s = symbolAttribute[0]
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0, xmlNodes1.namedItem("codeId").toElement().text());
                    xmlNodes3 = current.namedItem("codeChannel");
                    if (xmlNodes3 != None and xmlNodes3.toElement().text() != ""):
                        symbolAttribute.append(Captions.CHANNEL_BIG + " " + xmlNodes3.toElement().text());
                    xmlNodes3 = current.namedItem("txtName");
                    if (not xmlNodes3.isNull()):
                        symbolAttribute.append(xmlNodes3.toElement().text());

                xmlNodes3 = current.namedItem("txtName");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 5:
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("valMagVar");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 6:
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("dateMagVar");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.insert(6, s + " (" + xmlNodes3.toElement().text() + ")")
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());
                xmlNodes3 = current.namedItem("txtRmk");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 7:
                        symbolAttribute.pop(7)
                        symbolAttribute.insert(7, xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes3.toElement().text());

                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Dme])
#                 print self.pointData
            return True;
#             except:
#                 return False
        return True;
    def method_10(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("NdbUid");
                xmlNodes1 = current.namedItem("OrgUid");
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text());
                xmlNodes2 = current.namedItem("valFreq");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("uomFreq");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtName");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());

                xmlNodes2 = current.namedItem("valMagVar");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("dateMagVar");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Ndb])
#                 print self.pointData
            return True;
        return True;
    def method_11(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("MkrUid");
                xmlNodes1 = current.namedItem("OrgUid");
                symbolAttribute.append(xmlNodes.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes1.namedItem("txtName").toElement().text());
                xmlNodes2 = current.namedItem("valFreq");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("uomFreq");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtName");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());

                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Be1])
#                 print self.pointData
            return True;
        return True;
    def method_12(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("SnsUid");
                xmlNodes1 = xmlNodes.namedItem("SnyUid");
                xmlNodes2 = current.namedItem("OrgUid");
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(current.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                xmlNodes3 = current.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = current.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(xmlNodes2.namedItem("txtName").toElement().text());
                xmlNodes2 = current.namedItem("valFreq");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("uomFreq");
                if (not xmlNodes2.isNull()):
                    if len(symbolAttribute) > 4:
                        s = symbolAttribute[4]
                        symbolAttribute.pop(4)
                        symbolAttribute.append(s + " " + xmlNodes2.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes.namedItem("txtName");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("codeTypeSer");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(xmlNodes2.toElement().text());
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp])
#                 print self.pointData
            return True;
        return True;
    def method_13(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("IlsUid").namedItem("RdnUid");
                xmlNodes1 = current.namedItem("Ilz");
                xmlNodes2 = current.namedItem("Igp");
                symbolAttribute.append(xmlNodes1.namedItem("codeId").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));

                symbolAttribute.append(Captions.ILS_LOCALIZER_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text());
                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text());
                symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes1.namedItem("valFreq").toElement().text() + " " + xmlNodes1.namedItem("uomFreq").toElement().text());
                xmlNodes3 = xmlNodes1.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = xmlNodes1.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp])

                symbolAttribute = []
                if xmlNodes2.isNull():
                    continue
                symbolAttribute.append(Captions.ILS_GP_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes2.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));

                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text());
                symbolAttribute.append(Captions.FREQUENCY_BIG + " " + xmlNodes2.namedItem("valFreq").toElement().text() + " " + xmlNodes2.namedItem("uomFreq").toElement().text());
                xmlNodes3 = xmlNodes2.namedItem("valSlope");
                if (not xmlNodes3.isNull()):
                    symbolAttribute.append(Captions.SLOPE + " " + xmlNodes3.toElement().text());
                xmlNodes3 = xmlNodes2.namedItem("valRdh");
                if (not xmlNodes3.isNull()):
                    symbolAttribute.append(Captions.RDH + " " + xmlNodes3.toElement().text());
                xmlNodes3 = xmlNodes2.namedItem("uomRdh");
                if (not xmlNodes3.isNull()):
                    if len(symbolAttribute) > 6:
                        s = symbolAttribute[6]
                        symbolAttribute.pop(6)
                        symbolAttribute.append(s + " " + xmlNodes3.toElement().text())
                    else:
                        symbolAttribute.append(xmlNodes2.toElement().text())
                xmlNodes3 = xmlNodes2.namedItem("valElev");
                if (not xmlNodes3.isNull()):
                    innerText = xmlNodes3.toElement().text();
                xmlNodes3 = xmlNodes2.namedItem("uomDistVer");
                if (not xmlNodes3.isNull()):
                    str0 = xmlNodes3.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp])
            return True;
        return True;
    def method_14(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None

                xmlNodes = current.namedItem("MlsUid").namedItem("RdnUid");
                current.namedItem("DmeUid");
                xmlNodes1 = current.namedItem("Men");
                symbolAttribute.append(Captions.MLS_ELEVATION_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                symbolAttribute.append(Captions.CAT_BIG + " " + current.namedItem("codeCat").toElement().text());
                symbolAttribute.append(Captions.CHANNEL_BIG + " " + current.namedItem("codeChannel").toElement().text());
                xmlNodes2 = xmlNodes1.namedItem("valAngleNml");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.NOMINAL_ANGLE_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = xmlNodes1.namedItem("valAngleMnm");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.MINIMAL_ANGLE_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = xmlNodes1.namedItem("valAngleSpan");
                if (not xmlNodes2.isNull()):
                    symbolAttribute.append(Captions.ANGLE_SPAN_BIG + " " + xmlNodes2.toElement().text());
                xmlNodes2 = xmlNodes1.namedItem("valElev");
                if (not xmlNodes2.isNull()):
                    innerText = xmlNodes2.toElement().text();
                xmlNodes2 = xmlNodes1.namedItem("uomDistVer");
                if (not xmlNodes2.isNull()):
                    str0 = xmlNodes2.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp])


                current1_List = current.childNodes()
                for current1 in current1_List:
                    if (current1.nodeName() != "Mah"):
                        continue;
                    symbolAttribute = []
                    symbolAttribute.append(Captions.MLS_AZIMUTH_RWY_BIG + " " + xmlNodes.namedItem("txtDesig").toElement().text());
                    symbolAttribute.append(str(Degrees.smethod_15(current1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                    symbolAttribute.append(str(Degrees.smethod_15(current1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));
                    symbolAttribute.append(Captions.CODE_TYPE_BIG + " " + current1.namedItem("codeType").toElement().text());
                    xmlNodes2 = current1.namedItem("valAnglePropLeft");
                    if (not xmlNodes2.isNull()):
                        symbolAttribute.append(Captions.LEFT_ANGLE_OF_PROPORTIONALITY_BIG + " " + xmlNodes2.toElement().text());
                    xmlNodes2 = current1.namedItem("valAnglePropRight");
                    if (not xmlNodes2.isNull()):
                        symbolAttribute.append(Captions.RIGHT_ANGLE_OF_PROPORTIONALITY_BIG + " " + xmlNodes2.toElement().text());

                    xmlNodes2 = current1.namedItem("valAngleCoverLeft");
                    if (not xmlNodes2.isNull()):
                        symbolAttribute.append(Captions.LEFT_ANGLE_OF_COVERAGE_BIG + " " + xmlNodes2.toElement().text());

                    xmlNodes2 = current1.namedItem("valAngleCoverRight");
                    if (not xmlNodes2.isNull()):
                        symbolAttribute.append(Captions.RIGHT_ANGLE_OF_COVERAGE_BIG + " " + xmlNodes2.toElement().text());

                    xmlNodes2 = xmlNodes1.namedItem("valElev");
                    if (not xmlNodes2.isNull()):
                        innerText = xmlNodes2.toElement().text();
                    xmlNodes2 = xmlNodes1.namedItem("uomDistVer");
                    if (not xmlNodes2.isNull()):
                        str0 = xmlNodes2.toElement().text();
                    if innerText != None and innerText != "":
                        if str0 == "FT":
                            altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                        elif str0 == "M":
                            altitude_metre = innerText
                    else:
                        altitude_metre = "0.0"

                    attr = ""
                    for i in range(3, len(symbolAttribute)):
                        if len(attr) > 0:
                            attr += ", "
                        attr += symbolAttribute[i]
                    self.pointData.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, SymbolType.Gp])
#                 return True
            return True
        return True
    def method_15(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)
                symbolAttribute = []
                innerText = None;
                str0 = None;
                altitude_metre = None
                xmlNodes = current.namedItem("ObsUid")
                xmlNodes1 = current.namedItem("txtName");

                if (xmlNodes1 == None):
                    symbolAttribute.append(Captions.OBS);
                else:
                    symbolAttribute.append(xmlNodes1.toElement().text());
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(xmlNodes.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));

                innerText1 = current.namedItem("codeGroup").toElement().text();
                str1 = current.namedItem("codeLgt").toElement().text();
                xmlNodes1 = current.namedItem("txtDescrType");
                if (not xmlNodes1.isNull()):
                    symbolAttribute.append(xmlNodes1.toElement().text());
                xmlNodes1 = current.namedItem("txtRmk");
                if (not xmlNodes1.isNull()):
                    symbolAttribute.append(xmlNodes1.toElement().text());

                xmlNodes2 = current.namedItem("valElev");
                if (not xmlNodes2.isNull()):
                    innerText = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("uomDistVer");
                if (not xmlNodes2.isNull()):
                    str0 = xmlNodes2.toElement().text();
                if innerText != None and innerText != "":
                    if str0 == "FT":
                        altitude_metre = str(Altitude(float(innerText), AltitudeUnits.FT).Metres)
                    elif str0 == "M":
                        altitude_metre = innerText
                else:
                    altitude_metre = "0.0"
                symbolAttribute.append(Captions.VERTICAL_UNITS_BIG + " " + str0);
                symbolAttribute.append(innerText)
                xmlNodes1 = current.namedItem("valHgt");
                if (not xmlNodes1.isNull()):
                    symbolAttribute.append(xmlNodes1.toElement().text());
                attr = ""
                for i in range(3, len(symbolAttribute)):
                    if len(attr) > 0:
                        attr += ", "
                    attr += symbolAttribute[i]
                symbolType = SymbolType.Obst1
                if innerText1.count("Y") > 0 and str1.count("Y"):
                    symbolType = SymbolType.Obst4
                elif innerText1.count("Y") > 0:
                    symbolType = SymbolType.Obst3
                elif str1.count("Y") > 0:
                    symbolType = SymbolType.Obst2
                self.pointDataObstacles.append([symbolAttribute[0], "", "", symbolAttribute[1], symbolAttribute[2], altitude_metre, attr, symbolType])
            return True
        return True

    def method_16(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            strArrays = ["TcnUidSta", "VorUidSta", "DpnUidSta", "NdbUidSta", "DmeUidSta", "MkrUidSta"];
            strArrays1 = strArrays;
            strArrays2 = ["TcnUidEnd", "VorUidEnd", "DpnUidEnd", "NdbUidEnd", "DmeUidEnd", "MkrUidEnd"];
            strArrays3 = strArrays2;

            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)

                xmlNodes = current.namedItem("RsgUid");
                xmlNodes1 = xmlNodes.namedItem("RteUid");
                nodes = xmlNodes.childNodes()
#                 n = nodes.count()
                itemOf = nodes.item(1);
                if (not self.listComp(itemOf.nodeName(), strArrays1)):
                    continue;
                itemOf1 = nodes.item(2);
                if (not self.listComp(itemOf1.nodeName(), strArrays3)):
                    continue;
                str0 = xmlNodes1.namedItem("txtDesig").toElement().text() + " " + xmlNodes1.namedItem("txtLocDesig").toElement().text();
                symbolAttribute = []
                symbolAttribute.append(str0);
                symbolAttribute.append(str(Degrees.smethod_15(itemOf.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                symbolAttribute.append(str(Degrees.smethod_15(itemOf.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));

                degree = Degrees.smethod_15(itemOf.namedItem("geoLat").toElement().text(), DegreesType.Latitude)
                degree1 = Degrees.smethod_15(itemOf.namedItem("geoLong").toElement().text(), DegreesType.Longitude)

                symbolAttribute.append(itemOf.namedItem("codeId").toElement().text());
#                 Degrees degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude);
#                 Degrees degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude);
                innerText = []
                innerText.append(str0);
                innerText.append(str(Degrees.smethod_15(itemOf1.namedItem("geoLat").toElement().text(), DegreesType.Latitude).value));
                innerText.append(str(Degrees.smethod_15(itemOf1.namedItem("geoLong").toElement().text(), DegreesType.Longitude).value));

                degree2 = Degrees.smethod_15(itemOf1.namedItem("geoLat").toElement().text(), DegreesType.Latitude)
                degree3 = Degrees.smethod_15(itemOf1.namedItem("geoLong").toElement().text(), DegreesType.Longitude)

                innerText.append(itemOf1.namedItem("codeId").toElement().text());
                routList = []
                dataBaseCoordinate = DataBaseCoordinates("Segments");
                dataBaseCoordinate.method_0(degree, degree1, Altitude.NaN(), DataBaseCoordinateType.Point, symbolAttribute);
                dataBaseCoordinate.method_0(degree2, degree3, Altitude.NaN(), DataBaseCoordinateType.Point, innerText);
#                 routList.append([symbolAttribute[1], symbolAttribute[2], symbolAttribute[3]])
#                 routList.append([innerText[1], innerText[2], innerText[3]])
                self.pointDataRoutes.append([str0, dataBaseCoordinate])
            return True
        return True
    def method_17(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)

                xmlNodes = current.namedItem("AseUid");
                str0 = xmlNodes.namedItem("codeId").toElement().text() + " (" +  xmlNodes.namedItem("codeType").toElement().text() + ")";
                naN = None
                xmlNodes1 = current.namedItem("valDistVerLower");
                if (not xmlNodes1.isNull()):
                    naN = Altitude.smethod_4(xmlNodes1.toElement().text(), current.namedItem("uomDistVerLower").toElement().text());
                altitude = None
                xmlNodes1 = current.namedItem("valDistVerUpper");
                if (not xmlNodes1.isNull()):
                    altitude = Altitude.smethod_4(xmlNodes1.toElement().text(), current.namedItem("uomDistVerUpper").toElement().text());
                dataRow, rowIndex = self.airspaceMethod2(str0)
                if (dataRow == None):
                    if naN == None:
                        naN = Altitude(0)
                    if altitude == None:
                        altitude = Altitude(0)
                    self.pointDataAirspace.append([str0, str(naN.Metres), str(altitude.Metres), None, "True", "True", []])
#                     self.dataBase.method_6(str, naN, altitude, Distance.NaN, true, true, null);
                else:
                    if (naN.IsValid()):
                        dataRow.pop(1)
                        dataRow.insert(1, str(naN.Metres))
#                         dataRow["LowerLimit"] = naN;
#                     }
                    if (altitude.IsValid()):
                        dataRow.pop(2)
                        dataRow.insert(2, str(altitude.Metres))
#                         dataRow["UpperLimit"] = altitude;
#                     }

                    dataRow.pop(4)
                    dataRow.insert(4, "True")
                    item = dataRow[6]
                    if len(item) == 0:
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)
                        continue
                    for dataBaseCoordinate in item:
                        if dataBaseCoordinate.attributes == None:
                            continue
                        if (naN.IsValid()):
                            dataBaseCoordinate.set_attribute(4,  Captions.LOWER_LIMIT_BIG + " " + str(naN.Metres))
                        if (not altitude.IsValid()):
                            continue
                        dataBaseCoordinate.set_attribute(5, Captions.UPPER_LIMIT_BIG + " " + str(altitude.Metres));
#                     dataRow.pop(6)
#                     self.pointDataAirspace.insert(rowIndex, dataRow)
                    self.pointDataAirspace.pop(rowIndex)
                    self.pointDataAirspace.insert(rowIndex, dataRow)
            return True
        return True

    def method_18(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and  xmlNodeList_0.count() > 0):
            count =  xmlNodeList_0.count()
            for i in range(count):
                current = xmlNodeList_0.item(i)

                xmlNodes = current.namedItem("AbdUid").namedItem("AseUid");
                str0 = xmlNodes.namedItem("codeId").toElement().text() + " (" + xmlNodes.namedItem("codeType").toElement().text() + ")";
                symbolAttribute = SymbolAttributes();

                symbolAttribute.pop(0)
                symbolAttribute.insert(0, str0);

                dataRow, rowIndex = self.airspaceMethod2(str0);
                if (dataRow != None):
                    item = Altitude(float(dataRow[1]));
                    altitude = Altitude(float(dataRow[2]));
                    if (item.IsValid()):
                        symbolAttribute.pop(4)
                        symbolAttribute.insert(4, Captions.LOWER_LIMIT_BIG + " " + str(item.Metres));
                    if (altitude.IsValid()):
                        symbolAttribute.pop(5)
                        symbolAttribute.insert(5, Captions.UPPER_LIMIT_BIG + " " + str(altitude.Metres));

                xmlNodes1 = current.namedItem("Circle");
                if xmlNodes1.isNull():
                    flag1 = False
                    dataBaseCoordinate = DataBaseCoordinates("Vertices");
                    nodes = current.childNodes()
                    for i in range(nodes.count()):
                        current1 = nodes.item(i)
                        name = current1.nodeName()
                        if not name.count("Avx") > 0:
                            continue
                        innerText = current1.namedItem("codeType").toElement().text();
                        if innerText.count("CIR") > 0:
                            xmlNodes2 = current1.namedItem("geoLatArc");
                            xmlNodes3 = current1.namedItem("geoLongArc");
                            if (xmlNodes2 == None or xmlNodes3 == None):
                                symbolAttribute.pop(1)
                                symbolAttribute.insert(1, current1.namedItem("geoLat").toElement().text());
                                symbolAttribute.pop(2)
                                symbolAttribute.insert(2, current1.namedItem("geoLong").toElement().text());
#
#                                 symbolAttribute.append(current1.namedItem("geoLat").toElement().text());
#                                 symbolAttribute[2] = current1.namedItem("geoLong").toElement().text();
                            else:
                                symbolAttribute.pop(1)
                                symbolAttribute.insert(1, xmlNodes2.toElement().text());
                                symbolAttribute.pop(2)
                                symbolAttribute.insert(2, xmlNodes3.toElement().text());
# #
#                                 symbolAttribute[1] = xmlNodes2.toElement().text();
#                                 symbolAttribute[2] = xmlNodes3.toElement().text();
                            degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude);
                            degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude);
                            xmlNodes2 = current1.namedItem("valRadiusArc");
                            xmlNodes3 = current1.namedItem("uomRadiusArc");
                            if (xmlNodes2 == None or xmlNodes3 == None):
                                flag1 = True;
                                break;
                            else:
                                distance = Distance.smethod_7(xmlNodes2.toElement().text(), xmlNodes3.toElement().text());
                                symbolAttribute.pop(3)
                                symbolAttribute.insert(3, Captions.RADIUS_BIG + "" + str(distance.Metres));
                                dataBaseCoordinate.method_0(degree, degree1, Altitude.NaN, DataBaseCoordinateType.CenPoint, symbolAttribute);

                                if (dataRow == None):
                                    self.pointDataAirspace.append([str0, None, None, distance, "False", "False", dataBaseCoordinate])
                                else:
                                    dataRow.pop(3)
                                    dataRow.insert(3, str(distance.Metres))
                                    dataRow.pop(6)
                                    dataRow.insert(6, dataBaseCoordinate)

                                    self.pointDataAirspace.pop(rowIndex)
                                    self.pointDataAirspace.insert(rowIndex, dataRow)
                                flag1 = True;
                                break;
                        else:
                            naN = None;
                            naN1 = None;
                            symbolAttribute.pop(1)
                            symbolAttribute.insert(1, current1.namedItem("geoLat").toElement().text());
                            symbolAttribute.pop(2)
                            symbolAttribute.insert(2, current1.namedItem("geoLong").toElement().text());
                            degree2 = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude);
                            degree3 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude);
                            dataBaseCoordinateType = DataBaseCoordinateType.GRC;
                            if (innerText.count("FNT") > 0):
                                dataBaseCoordinateType = DataBaseCoordinateType.FNT;
                            elif (innerText.count("CCA") > 0):
                                dataBaseCoordinateType = DataBaseCoordinateType.CCA;
                            elif (innerText.count("CWA")>0):
                                dataBaseCoordinateType = DataBaseCoordinateType.CWA;
                            if (dataBaseCoordinateType == DataBaseCoordinateType.CCA or dataBaseCoordinateType == DataBaseCoordinateType.CWA):
                                try:
                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, current1.namedItem("geoLatArc").toElement().text());
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, current1.namedItem("geoLongArc").toElement().text());
                                    naN = Degrees.smethod_15(symbolAttribute[6], DegreesType.Latitude);
                                    naN1 = Degrees.smethod_15(symbolAttribute[7], DegreesType.Longitude);
                                    sss = symbolAttribute[6]
                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, Captions.CENTER_LATITUDE_BIG + " " + sss);
                                    sss = symbolAttribute[7]
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, Captions.CENTER_LONGITUDE_BIG + " " + sss);
                                except:
                                    dataBaseCoordinateType = DataBaseCoordinateType.GRC;

                                    symbolAttribute.pop(6)
                                    symbolAttribute.insert(6, "");
                                    symbolAttribute.pop(7)
                                    symbolAttribute.insert(7, "");
                                    naN = None;
                                    naN1 = None;
                            dataBaseCoordinate.method_3(None, None, degree2, degree3, None, naN, naN1, dataBaseCoordinateType, symbolAttribute);
                    if (flag1):
                        continue;
                    if (dataRow == None):
                        self.pointDataAirspace.append([str0, None, None, None, "False", "False", dataBaseCoordinate])
                    else:
                        dataRow.pop(6)
                        dataRow.insert(6, dataBaseCoordinate);
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)
                else:
                    symbolAttribute.pop(1)
                    symbolAttribute.insert(1, xmlNodes1.namedItem("geoLatCen").toElement().text());
                    symbolAttribute.pop(2)
                    symbolAttribute.insert(2, xmlNodes1.namedItem("geoLongCen").toElement().text());
                    degree4 = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude);
                    degree5 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude);
                    distance1 = Distance.smethod_7(xmlNodes1.namedItem("valRadius").toElement().text(), xmlNodes1.namedItem("uomRadius").toElement().text());
                    symbolAttribute.pop(3)
                    symbolAttribute.insert(3, Captions.RADIUS_BIG + " " + str(distance1.Metres));
                    dataBaseCoordinate1 = DataBaseCoordinates("Vertices");
                    dataBaseCoordinate1.method_0(degree4, degree5, None, "CenPoint", symbolAttribute);
                    if (dataRow == None):
                        self.pointDataAirspace.append([str0, None, None, str(distance1.Metres), "False", "False", dataBaseCoordinate1])
                    else:
                        dataRow.pop(3)
                        dataRow.insert(3, str(distance1.Metres));
                        dataRow.pop(6)
                        dataRow.insert(6, dataBaseCoordinate1);
                        self.pointDataAirspace.pop(rowIndex)
                        self.pointDataAirspace.insert(rowIndex, dataRow)

            self.airspaceMethod3()
            return True
        return True
    def method_19(self, xmlNodeList_0):
        flag = None;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("GbrUid");
                innerText = xmlNodes.namedItem("txtName").toElement().text();
                dataBaseGeoBorderType = current.namedItem("codeType").toElement().text();
                dataBaseCoordinate = DataBaseCoordinates("Vertices");
                nodes = current.childNodes()
                for i in range(nodes.count()):
                    current1 = nodes.item(i)
                    if current1.nodeName() != "Gbv":
                        continue
#                 for current1 in current.namedItem("Gbv"):
                    symbolAttribute = SymbolAttributes();
                    symbolAttribute.pop(0)
                    symbolAttribute.insert(0,innerText);
                    symbolAttribute.pop(1)
                    symbolAttribute.insert(1,current1.namedItem("geoLat").toElement().text());
                    symbolAttribute.pop(2)
                    symbolAttribute.insert(2,current1.namedItem("geoLong").toElement().text());
                    symbolAttribute.pop(3)
                    symbolAttribute.insert(3,dataBaseGeoBorderType);
                    degree = Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude);
                    degree1 = Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude);
                    dataBaseCoordinate.method_0(degree, degree1, None, DataBaseCoordinateType.GRC, symbolAttribute);
                self.pointDataBorder.append([innerText, dataBaseGeoBorderType, dataBaseCoordinate]);
            return True;
        return True
    def method_20(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_0(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    def method_21(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_3(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    def method_22(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_6(current, ProcEntityParseNodeType.Node);
            return True;
        return flag;
    def method_23(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_9(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    def method_24(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_12(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    def method_25(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_15(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    def method_26(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_36(current, ProcEntityParseNodeType.Node);
            return True;
        return True;

    def method_27(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_39(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    #
    def method_28(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_18(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_29(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_21(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_30(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_42(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_31(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_53(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_32(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_25(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_33(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_48(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_34(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_29(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
        
    def method_35(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_32(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
        
    def method_36(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                self.dataBase.ProcedureData.method_45(current, ProcEntityParseNodeType.Node);
            return True;
        return True;
    
    def method_37(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("SidUid");
                xmlNodes1 = xmlNodes.namedItem("AhpUid");
                innerText = self.dataBase.SIDs.NewRow();
                innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[4]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[1]] = xmlNodes.namedItem("txtDesig").toElement().text();
                innerText[innerText.nameList[5]] = xmlNodes.namedItem("txtDesig").toElement().text();
                xmlNodes2 = xmlNodes.namedItem("codeCatAcft");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[2]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text());
                    innerText[innerText.nameList[6]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text());
                xmlNodes2 = xmlNodes.namedItem("codeTransId");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[3]] = xmlNodes2.toElement().text();
                    innerText[innerText.nameList[7]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("RdnUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[8]] = self.dataBase.ProcedureData.method_29(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("FdnUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[8]] = self.dataBase.ProcedureData.method_32(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("MgpUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[9]] = self.dataBase.ProcedureData.method_45(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("codeRnp");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[10]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("txtDescrComFail");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[11]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("codeTypeRte");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[12]] = EnumHelper.Parse(CodeTypeSidAixm, xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtDescr");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[13]] = xmlNodes2.toElement().text()
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[14]] = xmlNodes2.toElement().text();
                innerText[innerText.nameList[15]] = self.method_42(current.toElement().elementsByTagName("Plg"));
                innerText[innerText.nameList[16]] = self.method_43(current.toElement().elementsByTagName("Pcl"));

                self.dataBase.SIDs.RowsAdd(innerText);
            return True;
        return True;

    def method_38(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("SiaUid");
                xmlNodes1 = xmlNodes.namedItem("AhpUid");
                innerText = self.dataBase.STARs.NewRow();
                innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[4]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[1]] = xmlNodes.namedItem("txtDesig").toElement().text();
                innerText[innerText.nameList[5]] = xmlNodes.namedItem("txtDesig").toElement().text();
                xmlNodes2 = xmlNodes.namedItem("codeCatAcft");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[2]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text())
                    innerText[innerText.nameList[6]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text())
                xmlNodes2 = xmlNodes.namedItem("codeTransId");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[3]] = xmlNodes2.toElement().text();
                    innerText[innerText.nameList[7]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("MgpUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[8]] = self.dataBase.ProcedureData.method_45(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("codeRnp");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[9]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("txtDescrComFail");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[10]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("codeTypeRte");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[11]] = EnumHelper.Parse(CodeTypeStarAixm, xmlNodes2.toElement().text());
                xmlNodes2 = current.namedItem("txtDescr");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[12]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[13]] = xmlNodes2.toElement().text();
                innerText[innerText.nameList[14]] = self.method_42(current.toElement().elementsByTagName("Plg"));
                innerText[innerText.nameList[15]] = self.method_43(current.toElement().elementsByTagName("Pcl"));

                self.dataBase.STARs.RowsAdd(innerText);
            return True;
        return True;

    def method_39(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("IapUid");
                xmlNodes1 = xmlNodes.namedItem("AhpUid");
                innerText = self.dataBase.IAPs.NewRow();
                innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[4]] = self.dataBase.ProcedureData.method_48(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[1]] = xmlNodes.namedItem("txtDesig").toElement().text();
                innerText[innerText.nameList[5]] = xmlNodes.namedItem("txtDesig").toElement().text();
                xmlNodes2 = xmlNodes.namedItem("codeCatAcft");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[2]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text())
                    innerText[innerText.nameList[6]] = EnumHelper.Parse(CodeCatAcftAixm, xmlNodes2.toElement().text());
                xmlNodes2 = xmlNodes.namedItem("codeTransId");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[3]] = xmlNodes2.toElement().text();
                    innerText[innerText.nameList[7]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("RdnUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[8]] = self.dataBase.ProcedureData.method_29(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("FdnUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[8]] = self.dataBase.ProcedureData.method_32(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("MgpUid");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[9]] = self.dataBase.ProcedureData.method_45(xmlNodes2, ProcEntityParseNodeType.UidNode);
                xmlNodes2 = current.namedItem("codeRnp");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[10]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("txtDescrComFail");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[11]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("codeTypeRte");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[12]] = EnumHelper.Parse(CodeTypeIapAixm, xmlNodes2.toElement().text())
                xmlNodes2 = current.namedItem("txtDescrMiss");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[13]] = xmlNodes2.toElement().text();
                xmlNodes2 = current.namedItem("txtRmk");
                if (not xmlNodes2.isNull()):
                    innerText[innerText.nameList[14]] = xmlNodes2.toElement().text();
                innerText[innerText.nameList[15]] = self.method_41(current.toElement().elementsByTagName("Ooh"));
                innerText[innerText.nameList[16]] = self.method_42(current.toElement().elementsByTagName("Plg"));
                innerText[innerText.nameList[17]] = self.method_43(current.toElement().elementsByTagName("Pcl"));

                self.dataBase.IAPs.RowsAdd(innerText);
            return True;
        return True;

    # def method_4(XmlNodeList xmlNodeList_0)
    # {
    #     bool flag;
    #     if (xmlNodeList_0 != null)
    #     {
    #         IEnumerator enumerator = xmlNodeList_0.GetEnumerator();
    #         try
    #         {
    #             while (enumerator.MoveNext())
    #             {
    #                 XmlNode current = (XmlNode)enumerator.Current;
    #                 if (this.worker.CancellationPending)
    #                 {
    #                     flag = false;
    #                     return flag;
    #                 }
    #                 else
    #                 {
    #                     SymbolAttributes symbolAttribute = new SymbolAttributes();
    #                     string innerText = null;
    #                     string str = null;
    #                     XmlNode xmlNodes = current.namedItem("RcpUid");
    #                     XmlNode xmlNodes1 = xmlNodes.namedItem("RwyUid");
    #                     XmlNode xmlNodes2 = xmlNodes1.namedItem("AhpUid");
    #                     symbolAttribute[0] = string.Format("{0} {1}", Captions.RWY_BIG, xmlNodes1.namedItem("txtDesig").toElement().text());
    #                     symbolAttribute[1] = xmlNodes.namedItem("geoLat").toElement().text();
    #                     symbolAttribute[2] = xmlNodes.namedItem("geoLong").toElement().text();
    #                     symbolAttribute[3] = xmlNodes2.namedItem("codeId").toElement().text();
    #                     XmlNode xmlNodes3 = current.namedItem("valElev");
    #                     if (xmlNodes3 != null)
    #                     {
    #                         innerText = xmlNodes3.toElement().text();
    #                     }
    #                     xmlNodes3 = current.namedItem("uomDistVer");
    #                     if (xmlNodes3 != null)
    #                     {
    #                         str = xmlNodes3.toElement().text();
    #                     }
    #                     this.dataBase.method_1(symbolAttribute[0], Degrees.smethod_15(symbolAttribute[1], DegreesType.Latitude, this.formatProvider), Degrees.smethod_15(symbolAttribute[2], DegreesType.Longitude, this.formatProvider), Altitude.smethod_4(innerText, str, this.formatProvider), new Symbol(SymbolType.Default), symbolAttribute);
    #                 }
    #             }
    #             return true;
    #         }
    #         finally
    #         {
    #             IDisposable disposable = enumerator as IDisposable;
    #             if (disposable != null)
    #             {
    #                 disposable.Dispose();
    #             }
    #         }
    #         return flag;
    #     }
    #     return true;
    # # }
    #
    def method_40(self, xmlNodeList_0):
        flag = False;
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                current = xmlNodeList_0.item(i)
                xmlNodes = current.namedItem("HpeUid");
                innerText = self.dataBase.Holdings.NewRow();
                xmlNodes1 = xmlNodes.namedItem("TcnUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_3(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_3(xmlNodes1, ProcEntityParseNodeType.UidNode);
                xmlNodes1 = xmlNodes.namedItem("VorUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_0(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_0(xmlNodes1, ProcEntityParseNodeType.UidNode);
                xmlNodes1 = xmlNodes.namedItem("DpnUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_53(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_53(xmlNodes1, ProcEntityParseNodeType.UidNode);
                xmlNodes1 = xmlNodes.namedItem("NdbUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_9(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_9(xmlNodes1, ProcEntityParseNodeType.UidNode);
                xmlNodes1 = xmlNodes.namedItem("DmeUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_6(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_6(xmlNodes1, ProcEntityParseNodeType.UidNode);
                xmlNodes1 = xmlNodes.namedItem("MkrUidSpn");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[0]] = self.dataBase.ProcedureData.method_12(xmlNodes1, ProcEntityParseNodeType.UidNode);
                    innerText[innerText.nameList[2]] = self.dataBase.ProcedureData.method_12(xmlNodes1, ProcEntityParseNodeType.UidNode);
                innerText[innerText.nameList[1]] = EnumHelper.Parse(CodeTypeHoldProcAixm, xmlNodes.namedItem("codeType").toElement().text());
                innerText[innerText.nameList[3]] = EnumHelper.Parse(CodeTypeHoldProcAixm, xmlNodes.namedItem("codeType").toElement().text());
                xmlNodes1 = current.namedItem("txtDescr");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[4]] = xmlNodes1.toElement().text();
                xmlNodes1 = current.namedItem("txtRmk");
                if (not xmlNodes1.isNull()):
                    innerText[innerText.nameList[5]] = xmlNodes1.toElement().text();
                innerText[innerText.nameList[6]] = self.method_42(current.toElement().elementsByTagName("Plg"));
                innerText[innerText.nameList[7]] = self.method_43(current.toElement().elementsByTagName("Pcl"));
                
                self.dataBase.Holdings.RowsAdd(innerText);
            return True;
        return True;
    
    def method_41(self, xmlNodeList_0):
        innerText = None;
        dataBaseIapOcaOch = DataBaseIapOcaOchs();
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                xmlNodeList0 = xmlNodeList_0.at(i)
                xmlNodes = None;
                dataBaseIapOcaOch1 = DataBaseIapOcaOch()
                dataBaseIapOcaOch1.CodeCatAcft = EnumHelper.Parse(CodeCatAcftAixm, xmlNodeList0.namedItem("codeCatAcft").toElement().text())
                dataBaseIapOcaOch1.CodeTypeApch = EnumHelper.Parse(CodeTypeApchAixm, xmlNodeList0.namedItem("codeTypeApch").toElement().text())
                xmlNodes = xmlNodeList0.namedItem("uomDistVer");
                if (xmlNodes == None):
                    innerText = None;
                else:
                    innerText = xmlNodes.toElement().text();
                strS = innerText;
                xmlNodes = xmlNodeList0.namedItem("valOca");
                if (not xmlNodes.isNull()):
                    dataBaseIapOcaOch1.ValOca = Altitude.smethod_4(xmlNodes.toElement().text(), strS);
                xmlNodes = xmlNodeList0.namedItem("valOch");
                if (not xmlNodes.isNull()):
                    dataBaseIapOcaOch1.ValOch = Altitude.smethod_4(xmlNodes.toElement().text(), strS);
                    dataBaseIapOcaOch1.CodeRefOch = EnumHelper.Parse(CodeRefOchAixm, xmlNodeList0.namedItem("codeRefOch").toElement().text())
                xmlNodes = xmlNodeList0.namedItem("txtRmk");
                if (not xmlNodes.isNull()):
                    dataBaseIapOcaOch1.TxtRmk = xmlNodes.toElement().text();
                dataBaseIapOcaOch.Add(dataBaseIapOcaOch1);
        return dataBaseIapOcaOch;

    def method_42(self, xmlNodeList_0):
        dataBaseProcedureLeg = DataBaseProcedureLegs();
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            i = 0
            for i in range(xmlNodeList_0.count()):
                xmlNodeList0 = xmlNodeList_0.at(i)
                innerText = DataBaseProcedureLeg();
                xmlNodes = xmlNodeList0.namedItem("SnyUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_15(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("IlsUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_36(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MlsUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_39(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("TcnUid");
                if (not xmlNodes.isNull()):
                    innerText.RecommendedEnt = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("TcnUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUidFix");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("TcnUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUidCen");
                if (not xmlNodes.isNull()):
                    innerText.PointEnt = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("codePhase");
                if (not xmlNodes.isNull()):
                    innerText.CodePhase = EnumHelper.Parse(CodePhaseProcAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeType");
                if (not xmlNodes.isNull()):
                    innerText.CodeType = EnumHelper.Parse(CodeTypeProcPathAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valCourse");
                if (not xmlNodes.isNull()):
                    innerText.ValCourse = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeTypeCourse");
                if (not xmlNodes.isNull()):
                    innerText.CodeTypeCourse = EnumHelper.Parse(CodeTypeCourseAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeDirTurn");
                if (not xmlNodes.isNull()):
                    innerText.CodeDirTurn = EnumHelper.Parse(CodeDirTurnAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeTurnValid");
                if (not xmlNodes.isNull()):
                    innerText.CodeTurnValid = EnumHelper.Parse(CodeTypeFlyByAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeDescrDistVer");
                if (not xmlNodes.isNull()):
                    innerText.CodeDescrDistVer = EnumHelper.Parse(CodeDescrDistVerAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeDistVerUpper");
                if (not xmlNodes.isNull()):
                    innerText.CodeDistVerUpper = EnumHelper.Parse(CodeDistVerAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valDistVerUpper");
                if (not xmlNodes.isNull()):
                    xmlNodes1 = xmlNodeList0.namedItem("uomDistVerUpper");
                    if (not xmlNodes1.isNull()):
                        innerText.ValDistVerUpper = Altitude.smethod_4(xmlNodes.toElement().text(), xmlNodes1.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("codeDistVerLower");
                if (not xmlNodes.isNull()):
                    innerText.CodeDistVerLower = EnumHelper.Parse(CodeDistVerAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valDistVerLower");
                if (not xmlNodes.isNull()):
                    xmlNodes2 = xmlNodeList0.namedItem("uomDistVerLower");
                    if (not xmlNodes2.isNull()):
                        innerText.ValDistVerLower = Altitude.smethod_4(xmlNodes.toElement().text(), xmlNodes2.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valVerAngle");
                if (not xmlNodes.isNull()):
                    innerText.ValVerAngle = float(xmlNodes.toElement().text())#AngleGradientSlope.smethod_1(xmlNodes.toElement().text(), AngleGradientSlopeUnits.Degrees);
                xmlNodes = xmlNodeList0.namedItem("valSpeedLimit");
                if (not xmlNodes.isNull()):
                    xmlNodes3 = xmlNodeList0.namedItem("uomSpeed");
                    if (not xmlNodes3.isNull()):
                        innerText.ValSpeedLimit = Speed.smethod_6(xmlNodes.toElement().text(), xmlNodes3.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeSpeedRef");
                if (not xmlNodes.isNull()):
                    innerText.CodeSpeedRef = EnumHelper.Parse(CodeSpeedRefAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valDist");
                if (not xmlNodes.isNull()):
                    xmlNodes4 = xmlNodeList0.namedItem("uomDistHorz");
                    if (not xmlNodes4.isNull()):
                        innerText.ValDist = Distance.smethod_7(xmlNodes.toElement().text(), xmlNodes4.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valDur");
                if (not xmlNodes.isNull()):
                    xmlNodes5 = xmlNodeList0.namedItem("uomDur");
                    if (not xmlNodes5.isNull()):
                        innerText.ValDur = float(xmlNodes.toElement().text())# Duration.smethod_4(xmlNodes.toElement().text(), xmlNodes5.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valTheta");
                if (not xmlNodes.isNull()):
                    innerText.ValTheta = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valRho");
                if (not xmlNodes.isNull()):
                    xmlNodes6 = xmlNodeList0.namedItem("uomDistHorz");
                    if (not xmlNodes6.isNull()):
                        innerText.ValRho = Distance.smethod_7(xmlNodes.toElement().text(), xmlNodes6.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valBankAngle");
                if (not xmlNodes.isNull()):
                    innerText.ValBankAngle = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeRepAtc");
                if (not xmlNodes.isNull()):
                    innerText.CodeRepAtc = EnumHelper.Parse(CodeRepAtcAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codeRoleFix");
                if (not xmlNodes.isNull()):
                    innerText.CodeRoleFix = EnumHelper.Parse(CodeIapFixAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("txtRmk");
                if (not xmlNodes.isNull()):
                    innerText.TxtRmk = xmlNodes.toElement().text();
                dataBaseProcedureLeg.Add(innerText);
        return dataBaseProcedureLeg;

    def method_43(self, xmlNodeList_0):
        dataBaseProcedureLegsEx = DataBaseProcedureLegsEx();
        if (xmlNodeList_0 != None and xmlNodeList_0.count() >  0):
            for i in range(xmlNodeList_0.count()):
                xmlNodeList0 = xmlNodeList_0.at(i)
                dataBaseProcedureLegEx = DataBaseProcedureLegEx();
                xmlNodes = xmlNodeList0.namedItem("VorUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("TcnUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("PcpUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_25(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("RcpUidPnt");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.PointEnt = self.dataBase.ProcedureData.method_18(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("TcnUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("PcpUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_25(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("RcpUidCen");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CenterEnt = self.dataBase.ProcedureData.method_18(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("codeLegType");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CodeLegType = EnumHelper.Parse(CodeLegTypeAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("codePathType");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CodePathType = EnumHelper.Parse(CodePathTypeAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valMinAlt");
                if (not xmlNodes.isNull()):
                    xmlNodes1 = xmlNodeList0.namedItem("uomMinAlt");
                    if (not xmlNodes1.isNull()):
                        dataBaseProcedureLegEx.ValMinAlt = Altitude.smethod_4(xmlNodes.toElement().text(), xmlNodes1.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valDist");
                if (not xmlNodes.isNull()):
                    xmlNodes2 = xmlNodeList0.namedItem("uomDist");
                    if (not xmlNodes2.isNull()):
                        dataBaseProcedureLegEx.ValDist = Distance.smethod_7(xmlNodes.toElement().text(), xmlNodes2.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("valCourse");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.ValCourse = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valLegRadial");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.ValLegRadial = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("VorUidLeg");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.VorUidLeg = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("codePointType");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CodePointType = xmlNodes.toElement().text();
                xmlNodes = xmlNodeList0.namedItem("codeRepAtc");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CodeRepAtc = EnumHelper.Parse(CodeRepAtcAixm, xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("valPointRadial");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.ValPointRadial = float(xmlNodes.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("VorUidPoint");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.VorUidPoint = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("valLegRadialBack");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.ValLegRadialBack = float(xmlNodes.toElement().text())
                xmlNodes = xmlNodeList0.namedItem("VorUidLegBack");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.VorUidLegBack = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("valPointDist1");
                if (not xmlNodes.isNull()):
                    xmlNodes3 = xmlNodeList0.namedItem("uomPointDist1");
                    if (not xmlNodes3.isNull()):
                        dataBaseProcedureLegEx.ValPointDist1 = Distance.smethod_7(xmlNodes.toElement().text(), xmlNodes3.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("TcnUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUid1");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist1 = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("valPointDist2");
                if (not xmlNodes.isNull()):
                    xmlNodes4 = xmlNodeList0.namedItem("uomPointDist2");
                    if (not xmlNodes4.isNull()):
                        dataBaseProcedureLegEx.ValPointDist2 = Distance.smethod_7(xmlNodes.toElement().text(), xmlNodes4.toElement().text());
                xmlNodes = xmlNodeList0.namedItem("TcnUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_3(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("VorUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_0(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DpnUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_53(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("NdbUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_9(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("DmeUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_6(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("MkrUid2");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.UidPointDist2 = self.dataBase.ProcedureData.method_12(xmlNodes, ProcEntityParseNodeType.UidNode);
                xmlNodes = xmlNodeList0.namedItem("valDur");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.ValDur = xmlNodes.toElement().text();
                xmlNodes = xmlNodeList0.namedItem("txtRmk");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.TxtRmk = xmlNodes.toElement().text();
                xmlNodes = xmlNodeList0.namedItem("codeFlyBy");
                if (not xmlNodes.isNull()):
                    dataBaseProcedureLegEx.CodeFlyBy = EnumHelper.Parse(CodeTypeFlyByAixm, xmlNodes.toElement().text())
                dataBaseProcedureLegsEx.Add(dataBaseProcedureLegEx);
        return dataBaseProcedureLegsEx;


    def findNodes(self, domNodeList, findedStr):
        count = domNodeList.count()
        resultIndex = []
        for i in range(count):
            node = domNodeList.item(i)
            name = node.nodeName()
            if name.contains(findedStr):
                resultIndex.append(i)
        return resultIndex
    def listComp(self, str0, strArray):
        for str1 in strArray:
            if str0 == str1:
                return True
        return False

    def airspaceMethod2(self, str0):
        if len(self.pointDataAirspace) == 0:
            return (None, 0)
        i = 0
        for airspace in self.pointDataAirspace:
            if airspace[0].count(str0) > 0:
                return (airspace, i)
            i += 1

        return (None, 0)
    def airspaceMethod3(self):
        num = 0
        numList = []
        if len(self.pointDataAirspace) > 0:
            flag = False
            i = 0
            while not flag:

                if i == len(self.pointDataAirspace):
                    flag = True
                    continue
                dataBaseCoordinate = self.pointDataAirspace[i][6]
                if dataBaseCoordinate == None or len(dataBaseCoordinate) == 0:
                    self.pointDataAirspace.pop(i)
                    continue
                i += 1

    def worker_DoWork(self):
        dateTime = None;
        num = None;
        xmlDocument = QDomDocument()
        qFile = QFile(self.dataBase.fileName)
        if qFile.open(QFile.ReadOnly):
            xmlDocument.setContent(qFile)
            qFile.close()
        else:
            raise UserWarning, "can not open file:" + self.dataBase.fileName

        progressMessageBar = define._messagBar.createMessage("Reding xml file...")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(self.progress)
        define._messagBar.pushWidget(progressMessageBar, define._messagBar.INFO)
        self.progress.setMaximum(100)
        xmlNodes = xmlDocument.elementsByTagName("AIXM-Snapshot");
        if (xmlNodes == None):
    #         XmlNamespaceManager xmlNamespaceManagers = new XmlNamespaceManager(xmlDocument.NameTable);
    #         xmlNamespaceManagers.AddNamespace("aixm-message", "http://www.aixm.aero/schema/5.1/message");
            if (xmlDocument.elementsByTagName("aixm-message:AIXMBasicMessage") == None):
                raise UserWarning, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_SNAPSHOT_NOT_FOUND)
            raise UserWarning, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, "unable to parse the AIXM 5.1 message features");
        namedItem = xmlNodes.item(0);
        if (namedItem == None):
            raise SystemError, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_UNKNOWN_VERSION);
        
        try:
            name = namedItem.nodeName()
            num = float(namedItem.toElement().attribute("version"))
        except:
            raise SystemError, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_PARSE_VERSION)
        # if (!double.TryParse(namedItem.toElement().text(), NumberStyles.Number, this.formatProvider, out num))
    #     {
    #         throw new Exception(string.Format("{0}, {1}", Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_PARSE_VERSION));
    #     }
        if (num > 4.5):
            raise SystemError, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_SUPPORTED_VERSION)
    #         throw new Exception(string.Format("{0}, {1}", Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_SUPPORTED_VERSION));
    #     }
        self.dataBase.Version = num;
        if (self.includeProcedureData):
            namedItem1 = xmlNodes.item(0)#self.findNodes(xmlNodes, "effective")[0])
            if (namedItem1 == None):
                raise SystemError, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_UNKNOWN_EFFECTIVE_DATE)
            try:
                dateTime = QDateTime.fromString(namedItem1.toElement().attribute("effective"), "yyyy-MM-dd'T'hh:mm:ss")
            except:
                raise SystemError, "{0}, {1}".format(Messages.ERR_AIXM_PREFIX, Messages.ERR_AIXM_PARSE_EFFECTIVE_DATE)
            self.dataBase.EffectiveDate = dateTime;
            xmlNodes = xmlDocument
            if (self.method_20(xmlNodes.elementsByTagName("Vor"))):
                self.progress.setValue(3)
                QApplication.processEvents()
                if (self.method_21(xmlNodes.elementsByTagName("Tcn"))):
                    self.progress.setValue(6);
                    QApplication.processEvents()
                    if (self.method_22(xmlNodes.elementsByTagName("Dme"))):
                        self.progress.setValue(10);
                        QApplication.processEvents()
                        if (self.method_23(xmlNodes.elementsByTagName("Ndb"))):
                            self.progress.setValue(13);
                            QApplication.processEvents()
                            if (self.method_25(xmlNodes.elementsByTagName("Sny"))):
                                self.progress.setValue(16);
                                QApplication.processEvents()
                                if (self.method_24(xmlNodes.elementsByTagName("Mkr"))):
                                    self.progress.setValue(20);
                                    QApplication.processEvents()
                                    if (self.method_28(xmlNodes.elementsByTagName("Rcp"))):
                                        self.progress.setValue(23);
                                        QApplication.processEvents()
                                        if (self.method_29(xmlNodes.elementsByTagName("Fcp"))):
                                            self.progress.setValue(26);
                                            QApplication.processEvents()
                                            if (self.method_30(xmlNodes.elementsByTagName("Tla"))):
                                                self.progress.setValue(30);
                                                QApplication.processEvents()
                                                if (self.method_33(xmlNodes.elementsByTagName("Ahp"))):
                                                    self.progress.setValue(33);
                                                    QApplication.processEvents()
                                                    if (self.method_34(xmlNodes.elementsByTagName("Rdn"))):
                                                        self.progress.setValue(36);
                                                        QApplication.processEvents()
                                                        if (self.method_35(xmlNodes.elementsByTagName("Fdn"))):
                                                            self.progress.setValue(40);
                                                            QApplication.processEvents()
                                                            if (self.method_26(xmlNodes.elementsByTagName("Ils"))):
                                                                self.progress.setValue(43);
                                                                QApplication.processEvents()
                                                                if (self.method_27(xmlNodes.elementsByTagName("Mls"))):
                                                                    self.progress.setValue(46);
                                                                    QApplication.processEvents()
                                                                    if (self.method_36(xmlNodes.elementsByTagName("Mgp"))):
                                                                        self.progress.setValue(50);
                                                                        QApplication.processEvents()
                                                                        if (self.method_31(xmlNodes.elementsByTagName("Dpn"))):
                                                                            self.progress.setValue(55);
                                                                            QApplication.processEvents()
                                                                            if (self.method_32(xmlNodes.elementsByTagName("Pcp"))):
                                                                                self.progress.setValue(60);
                                                                                QApplication.processEvents()
                                                                                if (self.method_37(xmlNodes.elementsByTagName("Sid"))):
                                                                                    self.progress.setValue(70);
                                                                                    QApplication.processEvents()
                                                                                    if (self.method_38(xmlNodes.elementsByTagName("Sia"))):
                                                                                        self.progress.setValue(80);
                                                                                        QApplication.processEvents()
                                                                                        if (self.method_39(xmlNodes.elementsByTagName("Iap"))):
                                                                                            self.progress.setValue(90);
                                                                                            QApplication.processEvents()
                                                                                            if (self.method_40(xmlNodes.elementsByTagName("Hpe"))):
                                                                                                self.progress.setValue(100);
                                                                                                QApplication.processEvents()
        elif self.method_3(xmlNodes.elementsByTagName("Ahp")):
            self.progress.setValue(5);
            QApplication.processEvents()
            if (self.method_4(xmlNodes.elementsByTagName("Rcp"))):
                self.progress.setValue(10);
                QApplication.processEvents()
                if (self.method_5(xmlNodes.elementsByTagName("Rdn"))):
                    self.progress.setValue(15);
                    QApplication.processEvents()
                    if (self.method_6(xmlNodes.elementsByTagName("Dpn"))):
                        self.progress.setValue(20);
                        QApplication.processEvents()
                        if (self.method_7(xmlNodes.elementsByTagName("Vor"))):
                            self.progress.setValue(25);
                            QApplication.processEvents()
                            if (self.method_8(xmlNodes.elementsByTagName("Tcn"))):
                                self.progress.setValue(30);
                                QApplication.processEvents()
                                if (self.method_10(xmlNodes.elementsByTagName("Ndb"))):
                                    self.progress.setValue(35);
                                    QApplication.processEvents()
                                    if (self.method_9(xmlNodes.elementsByTagName("Dme"))):
                                        self.progress.setValue(40);
                                        QApplication.processEvents()
                                        if (self.method_11(xmlNodes.elementsByTagName("Mkr"))):
                                            self.progress.setValue(45);
                                            QApplication.processEvents()
                                            if (self.method_12(xmlNodes.elementsByTagName("Sns"))):
                                                self.progress.setValue(50);
                                                QApplication.processEvents()
                                                if (self.method_13(xmlNodes.elementsByTagName("Ils"))):
                                                    self.progress.setValue(55);
                                                    QApplication.processEvents()
                                                    if (self.method_14(xmlNodes.elementsByTagName("Mls"))):
                                                        self.progress.setValue(60);
                                                        QApplication.processEvents()
                                                        if (self.method_15(xmlNodes.elementsByTagName("Obs"))):
                                                            self.progress.setValue(65);
                                                            QApplication.processEvents()
                                                            if (self.method_16(xmlNodes.elementsByTagName("Rsg"))):
                                                                self.progress.setValue(70);
                                                                QApplication.processEvents()
                                                                if (self.method_17(xmlNodes.elementsByTagName("Ase"))):
                                                                    self.progress.setValue(80);
                                                                    QApplication.processEvents()
                                                                    if (self.method_18(xmlNodes.elementsByTagName("Abd"))):
                                                                        self.progress.setValue(90);
                                                                        QApplication.processEvents()
                                                                        if (self.method_19(xmlNodes.elementsByTagName("Gbr"))):
                                                                            self.progress.setValue(100);
                                                                            QApplication.processEvents()

        self.progress.setValue(100)
        define._messagBar.hide()
    # catch (Exception exception1)
    # {
    #     Exception exception = exception1;
    #     if (self.ExceptionRaised != None)
    #     {
    #         self.ExceptionRaised(self, string.Format(Messages.ERR_FAILED_TO_IMPORT_AIXM_FILE, exception.Message));
    #     }
    #     e.Cancel = true;
