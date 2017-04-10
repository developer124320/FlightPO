
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QDataStream, QFile, QIODevice
from FlightPlanner.types import PositionType, Point3dCollection, AngleUnits
from FlightPlanner.helpers import MathHelper, Unit, Distance, Altitude
from FlightPlanner.messages import Messages
from FlightPlanner.Confirmations import Confirmations
from FlightPlanner.Captions import Captions
from Type.Position import Position, Point3D
from Type.String import String, QString, StringBuilder
from Type.switch import switch
from Type.Degrees import Degrees

import define

class Fato(list):
    def __init__(self):
        list.__init__(self)

        self.des1 = ""
        self.des2 = ""
        self.name = ""

        self.safetyAreaStart = 0.0
        self.safetyAreaEnd = 0.0
        self.safetyAreaWidth = 0.0

        self.Add(Position(PositionType.START))
        self.Add(Position(PositionType.END))
        self.Add(Position(PositionType.CWY))
    def Add(self, position):
        self.append(position)
    
    def get_DesignatorCode(self):
        return self.des2
    def set_DesignatorCode(self, value):
        self.des2 = value
        if (self.des2 == None):
            self.des2 = ""
    DesignatorCode = property(get_DesignatorCode, set_DesignatorCode, None, None)
    
    def get_DesignatorHeading(self):
        return self.des1
    def set_DesignatorHeading(self, value):
        self.des1 = value
        if (self.des1 == None):
            self.des1 = ""
    DesignatorHeading = property(get_DesignatorHeading, set_DesignatorHeading, None, None)
    
    def get_Direction(self):
        position = self.method_1(PositionType.START)
        position1 = self.method_1(PositionType.END)
        return MathHelper.getBearing(position.Point3d, position1.Point3d)
    Direction = property(get_Direction, None, None, None)
    
    def get_FullName(self):
        return QString("{0} {1}{2}".format(QString(self.name).trimmed(), self.des1, self.des2)).trimmed()
    FullName = property(get_FullName, None, None, None)
    
    def get_Name(self):
        return self.name
    def set_Name(self, value):
        self.name = value
        if (self.name == None):
            self.name = ""
    Name = property(get_Name, set_Name, None, None)

    def get_Point3dCollection(self):
        point3dCollection = Point3dCollection()
        position = self.method_1(PositionType.START)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        for position1 in self:
            if (position1.Type != PositionType.Position or not position1.IsValidIncludingAltitude):
                continue
            point3dCollection.Add(position1.Point3d)
        position = self.method_1(PositionType.END)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        position = self.method_1(PositionType.CWY)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        Point3dCollection.smethod_147(point3dCollection, True)
        return point3dCollection
    Point3dCollection = property(get_Point3dCollection, None, None, None)

    def get_SafetyAreaEnd(self):
        return self.safetyAreaEnd
    def set_SafetyAreaEnd(self, value):
        self.safetyAreaEnd = value
    SafetyAreaEnd = property(get_SafetyAreaEnd, set_SafetyAreaEnd, None, None)

    def get_SafetyAreaStart(self):
        return self.safetyAreaStart
    def set_SafetyAreaStart(self, value):
        self.safetyAreaStart = value
    SafetyAreaStart = property(get_SafetyAreaStart, set_SafetyAreaStart, None, None)

    def get_SafetyAreaWidth(self):
        return self.safetyAreaWidth
    def set_SafetyAreaWidth(self, value):
        self.safetyAreaWidth = value
    SafetyAreaWidth = property(get_SafetyAreaWidth, set_SafetyAreaWidth, None, None)

    def ClearItems(self):
        while True:
            if len(self) == 0: break
            self.pop(len(self) - 1)
        self.Add(Position(PositionType.START))
        self.Add(Position(PositionType.END))
        self.Add(Position(PositionType.CWY))

    def InsertItem(self, index, item):
        self.insert(index, item)

    def method_0(self):
        str0 = ""
        try:
            position = self.method_1(PositionType.START)
            position1 = self.method_1(PositionType.END)
            str0 = "{0:00}".format(Unit.smethod_1(MathHelper.getBearing(position.Point3d, position1.Point3d)) / 10)
        except:
            str0 = ""
        return str0

    def method_1(self, positionType_0):
        position = None
        for current in self:
        # using (IEnumerator<Position> enumerator = base.GetEnumerator())
        # {
        #     while (enumerator.MoveNext())
        #     {
        #         Position current = enumerator.Current
            if (current.Type != positionType_0):
                continue
            position = current
            return position
        return Position(positionType_0)

    def method_2(self, positionType_0):
        num = 0
        for current in self:
        # using (IEnumerator<Position> enumerator = base.GetEnumerator())
        # {
        #     while (enumerator.MoveNext())
        #     {
        #         Position current = enumerator.Current
            if (current.Type != positionType_0):
                continue
            num = self.index(current)
            return num
        return -1

    def method_3(self, positionType_0):
        positionType0 = positionType_0
        if (positionType0 == PositionType.CWY):
            if (self.method_4(PositionType.CWY)):
                return self.method_1(PositionType.CWY)
            return self.method_1(PositionType.END)
        for case in switch(positionType0):
            if case(PositionType.END):
                return self.method_1(PositionType.END)
            elif case(PositionType.Position):
                return self.method_1(positionType_0)
            elif case(PositionType.START):
                return self.method_1(PositionType.START)
            else:
                return self.method_1(positionType_0)

    def method_4(self, positionType_0):
        return self.method_1(positionType_0).IsValidIncludingAltitude

    def method_5(self, bool_0, string_0, string_1):
        position = Position()
        stringBuilder = StringBuilder()
        string_1 = QString(string_1)
        str0 = "qa:{0}".format(string_1.length())
        sAFETYAREAWIDTH = Captions.SAFETY_AREA_WIDTH
        distance = Distance(self.safetyAreaWidth)
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, sAFETYAREAWIDTH, distance.method_0("0.##:m")))
        sAFETYAREALENGTHSTART = Captions.SAFETY_AREA_LENGTH_START
        distance1 = Distance(self.safetyAreaStart)
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, sAFETYAREALENGTHSTART, distance1.method_0("0.##:m")))
        sAFETYAREALENGTHEND = Captions.SAFETY_AREA_LENGTH_END
        distance2 = Distance(self.safetyAreaEnd)
        stringBuilder.AppendLine("{0}{1}\t{2}".format(string_0, sAFETYAREALENGTHEND, distance2.method_0("0.##:m")))
        if (self.method_4(PositionType.START)):
            position = self.method_1(PositionType.START).method_3() if(not bool_0) else self.method_1(PositionType.START).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, position.Type.VariableNames[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        for position1 in self:
            if (position1.Type != PositionType.Position or not position1.IsValidIncludingAltitude):
                continue
            position = position1.method_3() if(not bool_0) else position1.method_2()
            stringBuilder.AppendLine(String.Concat([string_0, position.Type.VariableNames[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_4(PositionType.END)):
            position = self.method_1(PositionType.END).method_3() if(not bool_0) else self.method_1(PositionType.END).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, position.Type.VariableNames[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_4(PositionType.CWY)):
            position = self.method_1(PositionType.CWY).method_3() if(not bool_0) else self.method_1(PositionType.CWY).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, position.Type.VariableNames[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        return stringBuilder.ToString()

    def method_6(self, binaryWriter_0):
        if not isinstance(binaryWriter_0, QDataStream):
            QMessageBox.warning(None, "Warning", "Please use the QDataStream")
            return
        binaryWriter_0.writeQString(QString(self.name))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.name))
        binaryWriter_0.writeQString(QString(self.des1))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.des1))
        binaryWriter_0.writeQString(QString(self.des2))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.des2))
        binaryWriter_0.writeDouble(float(self.safetyAreaWidth))
        binaryWriter_0.writeDouble(float(self.safetyAreaStart))
        binaryWriter_0.writeDouble(float(self.safetyAreaEnd))
        binaryWriter_0.writeInt(len(self))
        for position in self:
            binaryWriter_0.writeInt(position.Type)
            binaryWriter_0.writeBool(position.IsXY)
            binaryWriter_0.writeBool(position.IsValidIncludingAltitude)
            if (not position.IsValidIncludingAltitude):
                continue
            binaryWriter_0.writeDouble(position.XLat)
            binaryWriter_0.writeDouble(position.YLon)
            binaryWriter_0.writeDouble(position.AltitudeValue.Metres)

    def method_7(self, iwin32Window_0):
        direction = self.Direction
        point3dCollection = self.Point3dCollection
        num = 0
        for i in range(1, point3dCollection.get_Count() - 1):
            item = point3dCollection.get_Item(i - 1)
            point3d = point3dCollection.get_Item(i)
            item1 = point3dCollection.get_Item(i + 1)
            num = max(MathHelper.smethod_84(item, point3d, item1, AngleUnits.Degrees), num)
        if (num <= 60):
            return True
        QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_FATO_POSITIONS_TRACK_CHANGE_EXCEEDS_X%(60))
        return False

    def RemoveItem(self, index):
        self.pop(index)

    def SetItem(self, index, item):
        if (item != None):
            if (index == 0):
                item.Type = PositionType.START
            elif (index == 1):
                item.Type = PositionType.END
            elif (index != 2):
                item.Type = PositionType.Position
            else:
                item.Type = PositionType.CWY
        self.__setitem__(index, item)

    @staticmethod
    def smethod_0(binaryReader_0, byte_0):
        if not isinstance(binaryReader_0, QDataStream):
            return
        position = Position()
        fato = Fato()
        if (byte_0 != 1):
            raise Messages.ERR_INVALID_FILE_FORMAT
            # throw new Exception(Messages.ERR_INVALID_FILE_FORMAT)
        fato.name = binaryReader_0.readQString()
        fato.des1 = binaryReader_0.readQString()
        fato.des2 = binaryReader_0.readQString()
        fato.safetyAreaWidth = binaryReader_0.readDouble()
        fato.safetyAreaStart = binaryReader_0.readDouble()
        fato.safetyAreaEnd = binaryReader_0.readDouble()
        num = binaryReader_0.readInt()
        for i in range(num):
            positionType = binaryReader_0.readInt()
            flag = binaryReader_0.readBool()
            if (binaryReader_0.readBool()):
                position = Position(positionType, None, None, None, Altitude(binaryReader_0.readDouble()), Degrees.smethod_1(binaryReader_0.readDouble()), Degrees.smethod_5(binaryReader_0.readDouble())) if(not flag) else Position(positionType, None, binaryReader_0.readDouble(), binaryReader_0.readDouble(), Altitude(binaryReader_0.readDouble()))
                if (i >= 3):
                    fato.Add(position)
                else:
                    fato[i] = position
        return fato

    def ToString(self):
        return self.FullName
    
class FatoList(list):
    fileName = ""

    @staticmethod
    def FatoList():
        path = ""
        if define.obstaclePath != None:
            path = define.obstaclePath
        elif define.xmlPath != None:
            path = define.xmlPath
        else:
            path = define.appPath
        FatoList.fileName = path + "/phxhsaf.dat"
        # FatoList.fileName = Path.Combine(ApplicationInfo.FolderAsapCommonData, "phxhsaf.dat")

    def __init__(self):
        list.__init__(self)

        self.HEADER = "PHXHSAF"
        self.VERSION = 1
    def Add(self, item):
        self.append(item)
    def Remove(self, index):
        self.pop(index)

    def IndexOf(self, item):
        i = 0
        for item0 in self:
            if item.FullName == item0.FullName:
                return i
            i += 1


    def method_0(self, iwin32Window_0):
        if QFile.exists(FatoList.fileName):
            fl = QFile.remove(FatoList.fileName)
            f = open(FatoList.fileName, 'w')
            f.flush()
            f.close()

        else:
            f = open(FatoList.fileName, 'w')
            # f = open("D:/xml/phxasar.txt")
            f.flush()
            f.close()

        file0 = QFile(FatoList.fileName)
        file0.open(QIODevice.WriteOnly)
        dataStream = QDataStream(file0)
        dataStream.writeQString(QString("PHXHSAF"))
        dataStream.writeInt(1)
        dataStream.writeInt(len(self))

        for fato in self:
            fato.method_6(dataStream)
        file0.flush()
        file0.close()




    def method_1(self):
        self.sort(FatoList.smethod_1)

    @staticmethod
    def smethod_0(iwin32Window_0):
        FatoList.FatoList()
        fatoList = FatoList()

        if (not QFile.exists(FatoList.fileName)):
            return fatoList
        file0 = QFile(FatoList.fileName)
        file0.open(QIODevice.ReadOnly)
        dataStream = QDataStream(file0)
        str0 = dataStream.readQString()
        num = dataStream.readInt()
        if (not (str0 == "PHXHSAF") or num != 1):
            raise Messages.ERR_INVALID_FILE_FORMAT
            # throw new Exception(Messages.ERR_INVALID_FILE_FORMAT)
        num1 = dataStream.readInt()
        for i in range(num1):
            fatoList.append(Fato.smethod_0(dataStream, num))
        fatoList.method_1()
        return fatoList

    @staticmethod
    def smethod_1(fato_0, fato_1):
        return 1 if(fato_0.FullName == fato_1.FullName) else -1