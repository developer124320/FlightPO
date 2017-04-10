# -*- coding: UTF-8 -*-

from PyQt4.QtXml import QDomDocument
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QFile
from FlightPlanner.types import NavigationalAidType
from FlightPlanner.Captions import Captions
from FlightPlanner.helpers import XmlFile, Distance, Altitude, AngleGradientSlope
from FlightPlanner.messages import Messages
from Type.String import String, StringBuilder
from Type.Extensions import Extensions
from Type.switch import switch

import define

class NavigationalAid:
    def __init__(self):
        self.name = None
        self.type = None
        self.hardCoded = False

    def get_DisplayName(self):
        str0 = self.type if(String.IsNullOrEmpty(self.name)) else self.name
        if (self.hardCoded):
            return str0
        return String.Concat(["* ", str0])
    DisplayName = property(get_DisplayName, None, None, None)

    def get_HardCoded(self):
        return self.hardCoded
    HardCoded = property(get_HardCoded, None, None, None)

    def get_Name(self):
        return self.name
    def set_Name(self, value):
        self.name = value
    Name = property(get_Name, set_Name, None, None)

    def get_Type(self):
        return self.type
    Type = property(get_Type, None, None, None)

    def ToString(self):
        return self.DisplayName

    def vmethod_0(self, string_0):
        pass

    def vmethod_1(self, xmlFile_0):
        pass

    def vmethod_2(self, string_0):
        pass

class NavigationalAidList(list):
    fileName = None
    def __init__(self):
        list.__init__(self)
    def Add(self, item):
        self.append(item)

    def IndexOf(self, item):
        if len(self) == 0:
            return -1
        i = 0
        for navigationalAid in self:
            if navigationalAid.hardCoded == item.hardCoded and navigationalAid.DisplayName == item.DisplayName:
                return i
            i += 1
        return -1

    def Remove(self, item):
        if len(self) == 0:
            return
        i = 0
        sameFlag = False
        for navigationalAid in self:
            if navigationalAid.hardCoded == item.hardCoded and navigationalAid.DisplayName == item.DisplayName:
                sameFlag = True
                break
            i += 1
        if sameFlag:
            self.pop(i)


    @staticmethod
    def NavigationalAidList():
        path = ""
        if define.obstaclePath != None:
            path = define.obstaclePath
        elif define.xmlPath != None:
            path = define.xmlPath
        else:
            path = define.appPath
        NavigationalAidList.fileName = path + "/phxshield.xml"

    def method_0(self, iwin32Window_0):
        # try:
        xmlFile = XmlFile(NavigationalAidList.fileName, "NavigationalAids", True)
        for navigationalAid in self:
            if (navigationalAid.HardCoded):
                continue
            navigationalAid.vmethod_1(xmlFile)
        xmlFile.method_0()
        # except:
        #     QMessageBox.warning(iwin32Window_0, "Error", "Failed to save the navigational aids data file.")
    def method_1(self):
        self.sort(NavigationalAidList.smethod_1)
    @staticmethod
    def smethod_0(iwin32Window_0):
        num = 0
        str0 = ""
        navigationalAidList = NavigationalAidList()
        NavigationalAidList.NavigationalAidList()
        navigationalAidList.append(OmnidirectionalNavigationalAid("DME N", AngleGradientSlope(1), Distance(3000), Distance(300), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("VOR", AngleGradientSlope(1), Distance(3000), Distance(600), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("Directional Finder (DF)", AngleGradientSlope(1), Distance(3000), Distance(500), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("Markers", AngleGradientSlope(20), Distance(200), Distance(50), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("NDB", AngleGradientSlope(5), Distance(1000), Distance(200), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("GBAS ground reference receiver", AngleGradientSlope(3), Distance(3000), Distance(400), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("GBAS VDB station", AngleGradientSlope(0.9), Distance(3000), Distance(300), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("SBAS ground monitoring station", AngleGradientSlope(3), Distance(3000), Distance(400), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("VHF (Communication Tx)", AngleGradientSlope(1), Distance(2000), Distance(300), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("VHF (Communication Rx)", AngleGradientSlope(1), Distance(2000), Distance(300), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("PSR", AngleGradientSlope(0.25), Distance(15000), Distance(500), True))
        navigationalAidList.append(OmnidirectionalNavigationalAid("SSR", AngleGradientSlope(0.25), Distance(15000), Distance(500), True))
        navigationalAidList.append(DirectionalNavigationalAid("ILS LOC (single freq.)", Distance.NaN(), Distance(500), Altitude(70), Distance(6000), Distance(500), Altitude(10), Distance(2300), AngleGradientSlope(30), True))
        navigationalAidList.append(DirectionalNavigationalAid("ILS LOC (dual freq.)", Distance.NaN(), Distance(500), Altitude(70), Distance(6000), Distance(500), Altitude(20), Distance(1500), AngleGradientSlope(20), True))
        navigationalAidList.append(DirectionalNavigationalAid("ILS GP M-Type (dual freq.)", Distance(800), Distance(50), Altitude(70), Distance(6000), Distance(250), Altitude(5), Distance(325), AngleGradientSlope(10), True))
        navigationalAidList.append(DirectionalNavigationalAid("MLS AZ", Distance.NaN(), Distance(20), Altitude(70), Distance(6000), Distance(600), Altitude(20), Distance(1500), AngleGradientSlope(40), True))
        navigationalAidList.append(DirectionalNavigationalAid("MLS EL", Distance(300), Distance(20), Altitude(70), Distance(6000), Distance(200), Altitude(20), Distance(1500), AngleGradientSlope(40), True))
        navigationalAidList.append(DirectionalNavigationalAid("DME (directional antennas)", Distance.NaN(), Distance(20), Altitude(70), Distance(6000), Distance(600), Altitude(20), Distance(1500), AngleGradientSlope(40), True))
        try:
            if (QFile.exists(NavigationalAidList.fileName)):
                xmlFile = XmlFile(NavigationalAidList.fileName, "NavigationalAids", False)
                xmlNodeLists = xmlFile.elementsByTagName("NavigationalAid")
                if (xmlNodeLists != None):
                    count =  xmlNodeLists.count()
                    for i in range(count):
                        xmlElement = xmlNodeLists.item(i)
                    # foreach (XmlElement xmlElement in xmlNodeLists)
                        result1, num = xmlFile.method_7(xmlElement, "Type")
                        result2, str0 = xmlFile.method_7(xmlElement, "Name")
                        if (not result1 or not result2):
                            continue
                        for case in switch(num):
                            if case(NavigationalAidType.Omnidirectional):
                                navigationalAidList.Add(OmnidirectionalNavigationalAid(None, xmlFile, xmlElement, str0))
                                continue
                            elif case(NavigationalAidType.Directional):
                                navigationalAidList.Add(DirectionalNavigationalAid(None, xmlFile, xmlElement, str0))
                                continue
                            elif case(NavigationalAidType.LineOfSight):
                                navigationalAidList.Add(LineOfSight(None, xmlFile, xmlElement, str0))
                                continue
                            else:
                                continue
        except:
            # Exception exception = exception1
            QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_FAILED_TO_LOAD_NAVAID_DATA_FILE)
            # ErrorMessageBox.smethod_0(iwin32Window_0, string.Format(Messages.ERR_FAILED_TO_LOAD_NAVAID_DATA_FILE, exception.Message))

        navigationalAidList.method_1()
        return navigationalAidList

    @staticmethod
    def smethod_1(navigationalAid_0, navigationalAid_1):
        num = 0
        # num = navigationalAid_1.HardCoded.CompareTo(navigationalAid_0.HardCoded)
        if (navigationalAid_1.HardCoded and navigationalAid_0.HardCoded) or (not navigationalAid_1.HardCoded and not navigationalAid_0.HardCoded):
            num = 0
        elif (not navigationalAid_1.HardCoded and navigationalAid_0.HardCoded):
            num = -1
        elif (navigationalAid_1.HardCoded and not navigationalAid_0.HardCoded):
            num = 1
        if (num == 0):
            num = String.Str2QString(navigationalAid_0.DisplayName).compare(navigationalAid_1.DisplayName)
        return num

class DirectionalNavigationalAid(NavigationalAid):
    def __init__(self, string_0, distance_0, distance_1, altitude_0, distance_2 = None, distance_3 = None, altitude_1 = None, distance_4 = None, angleGradientSlope_0 = None, bool_0 = None):
        NavigationalAid.__init__(self)
        if string_0 != None:
            self.name = string_0
            self.type = NavigationalAidType.Directional
            self.m_a = distance_0
            self.m_b = distance_1
            self.m_h = altitude_0
            self.m_r = distance_2
            self.m_D = distance_3
            self.m_H = altitude_1
            self.m_L = distance_4
            self.m_phi = angleGradientSlope_0
            self.hardCoded = bool_0
        else:
            xmlFile_0 = distance_0
            xmlElement_0 = distance_1
            string_1 = altitude_0
            
            self.type = NavigationalAidType.Directional
            self.name = string_1
            self.m_a = xmlFile_0.method_39(xmlElement_0, "a")[1]
            self.m_b = xmlFile_0.method_39(xmlElement_0, "b")[1]
            self.m_h = xmlFile_0.method_35(xmlElement_0, "h")[1]
            self.m_r = xmlFile_0.method_39(xmlElement_0, "r")[1]
            self.m_D = xmlFile_0.method_39(xmlElement_0, "D")[1]
            self.m_H = xmlFile_0.method_35(xmlElement_0, "H")[1]
            self.m_L = xmlFile_0.method_39(xmlElement_0, "L")[1]
            self.m_phi = xmlFile_0.method_47(xmlElement_0, "phi")[1]
            self.hardCoded = False

    def get_a(self):
        return self.m_a
    def set_a(self, value):
        self.m_a = value
    a = property(get_a, set_a, None, None)

    def get_b(self):
        return self.m_b
    def set_b(self, value):
        self.m_b = value
    b = property(get_b, set_b, None, None)

    def get_D(self):
        return self.m_D
    def set_D(self, value):
        self.m_D = value
    D = property(get_D, set_D, None, None)

    def get_h(self):
        return self.m_h
    def set_h(self, value):
        self.m_h = value
    h = property(get_h, set_h, None, None)

    def get_H(self):
        return self.m_H
    def set_H(self, value):
        self.m_H = value
    H = property(get_H, set_H, None, None)

    def get_L(self):
        return self.m_L
    def set_L(self, value):
        self.m_L = value
    L = property(get_L, set_L, None, None)

    def get_phi(self):
        return self.m_phi
    def set_phi(self, value):
        self.m_phi = value
    phi = property(get_phi, set_phi, None, None)

    def get_r(self):
        return self.m_r
    def set_r(self, value):
        self.m_r = value
    r = property(get_r, set_r, None, None)
    
    
    def vmethod_0(self, string_0):
        return DirectionalNavigationalAid(string_0, self.m_a, self.m_b, self.m_h, self.m_r, self.m_D, self.m_H, self.m_L, self.m_phi, False)
    def vmethod_1(self, xmlFile_0):
        if not isinstance(xmlFile_0, XmlFile):
            return
        xmlElement = xmlFile_0.createElement("NavigationalAid")


        # xmlFile_0.method_17(xmlElement, "Type", (int)self.type)
        xmlFile_0.method_9(xmlElement, "Type", self.type)
        xmlFile_0.method_9(xmlElement, "Name", self.name)
        xmlFile_0.method_41(xmlElement, "a", self.m_a)
        xmlFile_0.method_41(xmlElement, "b", self.m_b)
        xmlFile_0.method_37(xmlElement, "h", self.m_h)
        xmlFile_0.method_41(xmlElement, "r", self.m_r)
        xmlFile_0.method_41(xmlElement, "D", self.m_D)
        xmlFile_0.method_37(xmlElement, "H", self.m_H)
        xmlFile_0.method_41(xmlElement, "L", self.m_L)
        xmlFile_0.method_49(xmlElement, "phi", self.m_phi)
        xmlFile_0.rootElement.appendChild(xmlElement)
    def vmethod_2(self, string_0):
        stringBuilder = StringBuilder()
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.NAME, self.name))
        if (self.m_a.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "a", self.m_a.method_0(":u")))
        if (self.m_b.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "b", self.m_b.method_0(":u")))
        if (self.m_h.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "h", self.m_h.method_0(":u")))
        if (self.m_r.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "r", self.m_r.method_0(":u")))
        if (self.m_D.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "D", self.m_D.method_0(":u")))
        if (self.m_H.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "H", self.m_H.method_0(":u")))
        if (self.m_L.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "L", self.m_L.method_0(":u")))
        if (self.m_phi.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "ɸ", self.m_phi.method_0(":u")))
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.STANDARD, Extensions.smethod_26(self.hardCoded)))
        return stringBuilder.ToString()


class LineOfSight(NavigationalAid):
    def __init__(self, string_0, angleGradientSlope_0, altitude_0, distance_0, bool_0 = None):
        NavigationalAid.__init__(self)
        if string_0 != None:
            self.name = string_0
            self.type = NavigationalAidType.LineOfSight
            self.slope = angleGradientSlope_0
            self.startingHeight = altitude_0
            self.finishingDistance = distance_0
            self.hardCoded = bool_0
        else:
            xmlFile_0 = angleGradientSlope_0
            xmlElement_0 = altitude_0
            string_1 = distance_0

            self.type = NavigationalAidType.LineOfSight
            self.name = string_1
            self.slope = xmlFile_0.method_47(xmlElement_0, "Slope")[1]
            self.startingHeight = xmlFile_0.method_35(xmlElement_0, "StartingHeight")[1]
            self.finishingDistance = xmlFile_0.method_39(xmlElement_0, "FinishingDistance")[1]
            self.hardCoded = False

    def get_FinishingDistance(self):
        return self.finishingDistance
    def set_FinishingDistance(self, value):
        self.finishingDistance = value
    FinishingDistance = property(get_FinishingDistance, set_FinishingDistance, None, None)

    def get_Slope(self):
        return self.slope
    def set_Slope(self, value):
        self.slope = value
    Slope = property(get_Slope, set_Slope, None, None)

    def get_StartingHeight(self):
        return self.startingHeight
    def set_StartingHeight(self, value):
        self.startingHeight = value
    StartingHeight = property(get_StartingHeight, set_StartingHeight, None, None)


    def vmethod_0(self, string_0):
        return LineOfSight(string_0, self.slope, self.startingHeight, self.finishingDistance, False)
    
    def vmethod_1(self, xmlFile_0):
        if not isinstance(xmlFile_0, XmlFile):
            return
        xmlElement = xmlFile_0.createElement("NavigationalAid")
        # xmlFile_0.method_17(xmlElement, "Type", (int)this.type)
        xmlFile_0.method_9(xmlElement, "Type", self.type)
        xmlFile_0.method_9(xmlElement, "Name", self.name)
        xmlFile_0.method_49(xmlElement, "Slope", self.slope)
        xmlFile_0.method_37(xmlElement, "StartingHeight", self.startingHeight)
        xmlFile_0.method_41(xmlElement, "FinishingDistance", self.finishingDistance)
        xmlFile_0.rootElement.appendChild(xmlElement)

    def vmethod_2(self, string_0):
        stringBuilder = StringBuilder()
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.NAME, self.name))
        if (self.slope.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.SLOPE, self.slope.method_0(":u")))
        if (self.startingHeight.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.STARTING_HEIGHT, self.startingHeight.method_0(":u")))
        if (self.finishingDistance.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.FINISHING_DISTANCE, self.finishingDistance.method_0(":u")))
        return stringBuilder.ToString()

class OmnidirectionalNavigationalAid(NavigationalAid):
    def __init__(self, string_0, angleGradientSlope_0, distance_0, distance_1, bool_0 = None):
        NavigationalAid.__init__(self)
        if string_0 != None:
            self.type = NavigationalAidType.Omnidirectional
            self.name = string_0
            self.m_alfa = angleGradientSlope_0
            self.m_R = distance_0
            self.m_r = distance_1
            self.hardCoded = bool_0
        else:
            xmlFile_0 = angleGradientSlope_0
            xmlElement_0 = distance_0
            string_1 = distance_1
            self.type = NavigationalAidType.Omnidirectional
            self.name = string_1
            self.m_alfa = xmlFile_0.method_47(xmlElement_0, "alfa")[1]
            self.m_R = xmlFile_0.method_39(xmlElement_0, "R")[1]
            self.m_r = xmlFile_0.method_39(xmlElement_0, "r")[1]
            self.hardCoded = False

    def get_Alfa(self):
        return self.m_alfa
    def set_Alfa(self, value):
        self.m_alfa = value
    Alfa = property(get_Alfa, set_Alfa, None, None)

    def get_r(self):
        return self.m_r
    def set_r(self, value):
        self.m_r = value
    r = property(get_r, set_r, None, None)

    def get_R(self):
        return self.m_R
    def set_R(self, value):
        self.m_R = value
    R = property(get_R, set_R, None, None)
    
    
    def vmethod_0(self, string_0):
        return OmnidirectionalNavigationalAid(string_0, self.m_alfa, self.m_R, self.m_r, False)

    def vmethod_1(self, xmlFile_0):
        if not isinstance(xmlFile_0, XmlFile):
            return
        xmlElement = xmlFile_0.createElement("NavigationalAid")
        # xmlFile_0.method_17(xmlElement, "Type", (int)self.type)
        xmlFile_0.method_9(xmlElement, "Type", self.type)
        xmlFile_0.method_9(xmlElement, "Name", self.name)
        xmlFile_0.method_49(xmlElement, "alfa", self.m_alfa)
        xmlFile_0.method_41(xmlElement, "R", self.m_R)
        xmlFile_0.method_41(xmlElement, "r", self.m_r)
        xmlFile_0.rootElement.appendChild(xmlElement)

    def vmethod_2(self, string_0):
        stringBuilder = StringBuilder()
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.NAME, self.name))
        if (self.m_alfa.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "Alpha (α - Cone)", self.m_alfa.method_0(":u")))
        if (self.m_R.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "Radius (R - Cone)", self.m_R.method_0(":u")))
        if (self.m_r.IsValid()):
            stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, "Radius (r - Cylinder)", self.m_r.method_0(":u")))
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, Captions.STANDARD, Extensions.smethod_26(self.hardCoded)))
        return stringBuilder.ToString()
