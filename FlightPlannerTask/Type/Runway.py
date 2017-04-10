
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QDataStream, QFile, QIODevice
from FlightPlanner.types import PositionType, Point3dCollection, AngleUnits
from FlightPlanner.helpers import MathHelper, Unit, Distance, Altitude
from FlightPlanner.messages import Messages
from FlightPlanner.Confirmations import Confirmations
from Type.Position import Position, Point3D
from Type.String import String, QString, StringBuilder
from Type.switch import switch
from Type.Degrees import Degrees

import define

class Runway(list):
    def __init__(self):
        list.__init__(self)

        self.des1 = ""
        self.des2 = ""
        self.name = ""
        
        self.Add(Position(PositionType.START))
        self.Add(Position(PositionType.THR))
        self.Add(Position(PositionType.END))
        self.Add(Position(PositionType.SWY))
        self.Add(Position(PositionType.CWY))
    def Add(self, position):
        if not isinstance(position, Position):
            raise "Please add the Position instance."
        self.append(position)
    
    
    def get_DesignatorCode(self):
        return self.des2
    def set_DesignatorCode(self, value):
        self.des2 = value
        if self.des2 == None:
            self.des2 = ""
    DesignatorCode = property(get_DesignatorCode, set_DesignatorCode, None, None)
    
    def get_DesignatorHeading(self):
        return self.des1
    def set_DesignatorHeading(self, value):
        self.des1 = value
        if self.des1 == None:
            self.des1 = ""
    DesignatorHeading = property(get_DesignatorHeading, set_DesignatorHeading, None, None)
    
    def get_Direction(self):
        position = self.method_1(PositionType.THR)
        position1 = self.method_1(PositionType.END)
        return MathHelper.getBearing(position.Point3d, position1.Point3d)
    Direction = property(get_Direction, None, None, None)
    
    def get_FullName(self):
        nameStr = String.Str2QString(self.name)
        return QString("{0} {1}{2}".format(nameStr.trimmed(), self.des1, self.des2)).trimmed()
    FullName = property(get_FullName, None, None, None)
    
    def get_Name(self):
        return self.name
    def set_Name(self, value):
        self.name = value
        if self.name == None:
            self.name = ""
    Name = property(get_Name, set_Name, None, None)

    def get_Point3dCollection(self):
        point3dCollection = Point3dCollection()
        position = self.method_1(PositionType.START)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        position = self.method_1(PositionType.THR)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        for position1 in self:
            if (position1.Type != PositionType.Position or not position1.IsValidIncludingAltitude):
                continue
            point3dCollection.Add(position1.Point3d)
        position = self.method_1(PositionType.END)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        position = self.method_1(PositionType.SWY)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        position = self.method_1(PositionType.CWY)
        if (position.IsValidIncludingAltitude):
            point3dCollection.Add(position.Point3d)
        Point3dCollection.smethod_147(point3dCollection, True)
        return point3dCollection
    Point3dCollectionValue = property(get_Point3dCollection, None, None, None)
        
    def ClearItems(self):
        while True:
            if len(self) == 0: break
            self.pop(len(self) - 1)
        self.Add(Position(PositionType.START))
        self.Add(Position(PositionType.THR))
        self.Add(Position(PositionType.END))
        self.Add(Position(PositionType.SWY))
        self.Add(Position(PositionType.CWY))

    def InsertItem(self, index, item):
        self.insert(index, item)

    def method_0(self):
        str0 = ""
        try:
            position = self.method_1(PositionType.THR)
            position1 = self.method_1(PositionType.END)
            str0 = str(int(round(Unit.smethod_1(MathHelper.getBearing(position.Point3d, position1.Point3d)) / 10)))
            if len(str0) == 1:
                str0 = "0" + str0
        except:
            str0 = ""
        return str0

    def method_1(self, positionType_0):
        position = None
        try:
            for current in self:
                if (current.Type != positionType_0):
                    continue
                position = current
                return position
            return Position(positionType_0)
        except:
            pass
        return position

    def method_2(self, positionType_0):
        num = None
        try:
            i = 0
            for current in self:
                if (current.Type != positionType_0):
                    i += 1
                    continue
                num = i
                return num
            return -1
        except:
            pass
        return num

    def method_3(self, bool_0):
        point3d = None
        if (not bool_0):
            position = self.method_1(PositionType.START)
            point3d = self.method_1(PositionType.THR).Point3d if(not position.IsValidIncludingAltitude) else position.Point3d
        else:
            point3d = self.method_1(PositionType.THR).Point3d
        point3d1 = self.method_1(PositionType.END).Point3d
        return Distance(MathHelper.calcDistance(point3d, point3d1))

    def method_4(self, positionType_0):
        for case in switch(positionType_0):
            if case(PositionType.CWY):
                if (self.method_5(PositionType.CWY)):
                    return self.method_1(PositionType.CWY)
                if (self.method_5(PositionType.SWY)):
                    return self.method_1(PositionType.SWY)
                return self.method_1(PositionType.END)
            elif case(PositionType.SWY):
                if (self.method_5(PositionType.SWY)):
                    return self.method_1(PositionType.SWY)
                return self.method_1(PositionType.END)
            elif case(PositionType.THR):
                return self.method_1(PositionType.THR)
            elif case(PositionType.END):
                return self.method_1(PositionType.END)
            elif case(PositionType.Position):
                return self.method_1(positionType_0)
            elif case(PositionType.START):
                if (self.method_5(PositionType.START)):
                    return self.method_1(PositionType.START)
                return self.method_1(PositionType.THR)
            else:
                return self.method_1(positionType_0)
                
    def method_5(self, positionType_0):
        return self.method_1(positionType_0).IsValidIncludingAltitude

    def method_6(self, bool_0, string_0, string_1):
        position = None
        stringBuilder = StringBuilder()
        str0 = "qa:{0}".format(string_1.Length)
        if (self.method_5(PositionType.START)):
            position = self.method_1(PositionType.START).method_3() if(not bool_0) else self.method_1(PositionType.START).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_5(PositionType.THR)):
            position = self.method_1(PositionType.THR).method_3() if(not bool_0) else self.method_1(PositionType.THR).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        for position1 in self:
            if (position1.Type != PositionType.Position or not position1.IsValidIncludingAltitude):
                continue
            position = position1.method_3() if(not bool_0) else position1.method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_5(PositionType.END)):
            position = self.method_1(PositionType.END).method_3() if(not bool_0) else self.method_1(PositionType.END).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_5(PositionType.SWY)):
            position = self.method_1(PositionType.SWY).method_3() if(not bool_0) else self.method_1(PositionType.SWY).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        if (self.method_5(PositionType.CWY)):
            position = self.method_1(PositionType.CWY).method_3() if(not bool_0) else self.method_1(PositionType.CWY).method_2()
            stringBuilder.AppendLine(String.Concat([string_0, PositionType.Items[position.Type - 1]]))
            stringBuilder.AppendLine(position.method_5(str0))
        return stringBuilder.ToString()

    def method_7(self, iwin32Window_0):
        distance = self.method_3(True)
        if (not distance.IsValid() or distance.Metres < 100):
            QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_INSUFFICIENT_RWY_LENGTH)
            return False
        direction = self.Direction
        point3dCollection = self.Point3dCollectionValue
        num = 0
        for i in range(1, point3dCollection.get_Count() - 1):
            item = point3dCollection.get_Item(i - 1)
            point3d = point3dCollection.get_Item(i)
            item1 = point3dCollection.get_Item(i + 1)
            num = max(MathHelper.smethod_84(item, point3d, item1, AngleUnits.Degrees), num)
        if (num < 10):
            return True
        if (num >= 45):
            QMessageBox.warning(iwin32Window_0, "Error", Messages.ERR_RWY_POSITIONS_TRACK_CHANGE_45)
            return False
        return QMessageBox.warning(iwin32Window_0, "Warning", Confirmations.RWY_POSITIONS_TRACK_CHANGE_INCORRECT, QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes

    def method_8(self, dataStream):
        ####### dataStream must be the instance of QDataStream.
        if not isinstance(dataStream, QDataStream):
            QMessageBox.warning(None, "Warning", "Please use the QDataStream")
            return
        # dataStream.writeInt(len(self.name))
        dataStream.writeQString(QString(self.name))
        # dataStream.writeInt(len(self.des1))
        dataStream.writeQString(QString(self.des1))
        # dataStream.writeInt(len(self.des2))
        dataStream.writeQString(QString(self.des2))
        dataStream.writeInt(len(self))
        # binaryWriter_0.Write(Encoding.Default.GetByteCount(self.name))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.name))
        # binaryWriter_0.Write(Encoding.Default.GetByteCount(self.des1))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.des1))
        # binaryWriter_0.Write(Encoding.Default.GetByteCount(self.des2))
        # binaryWriter_0.Write(Encoding.Default.GetBytes(self.des2))
        # binaryWriter_0.Write(base.Count)
        for position in self:
            dataStream.writeInt(position.Type)
            dataStream.writeBool(position.IsXY)
            dataStream.writeBool(position.IsValidIncludingAltitude)
            # binaryWriter_0.Write((byte)position.Type)
            # binaryWriter_0.Write(position.IsXY)
            # binaryWriter_0.Write(position.IsValidIncludingAltitude)
            if (not position.IsValidIncludingAltitude):
                continue
            dataStream.writeDouble(position.XLat)
            dataStream.writeDouble(position.YLon)
            dataStream.writeDouble(position.AltitudeValue.Metres)
            # binaryWriter_0.Write(position.XLat)
            # binaryWriter_0.Write(position.YLon)
            # binaryWriter_0.Write(position.Altitude.Metres)

    def ToString(self):
        return self.FullName

    def RemoveItem(self, index):
        self.pop(index)

    def SetItem(self, index, item):
        if (item != None):
            if (index == 0):
                item.Type = PositionType.START
            elif (index == 1):
                item.Type = PositionType.THR
            elif (index == 2):
                item.Type = PositionType.END
            elif (index == 3):
                item.Type = PositionType.SWY
            elif (index != 4):
                item.Type = PositionType.Position
            else:
                item.Type = PositionType.CWY
        self.__setitem__(index, item)

    @staticmethod
    def smethod_0(dataStream, byte_0 = 0):
        ####### dataStream must be the instance of QDataStream.
        if not isinstance(dataStream, QDataStream):
            QMessageBox.warning(None, "Warning", "Please use the QDataStream")
            return

        position = None
        runway = Runway()

        runway.name = dataStream.readQString()
        runway.des1 = dataStream.readQString()
        runway.des2 = dataStream.readQString()

        positionCount = dataStream.readInt()
        if byte_0 == 2:
            for i in range(positionCount):
                positionType = dataStream.writeInt()
                xyFlag = dataStream.readBool()
                validIncludingAltitude = dataStream.readBool()
                if validIncludingAltitude:
                    xLat = dataStream.readDouble()
                    yLon = dataStream.readDouble()
                    altitude = dataStream.readDouble()

                    if (positionType == 1):
                        runway[runway.method_2(PositionType.CWY)] = Position(PositionType.CWY, None, xLat, yLon, Altitude(altitude))
                    elif (positionType == 2):
                        runway[runway.method_2(PositionType.SWY)] = Position(PositionType.SWY, None, xLat, yLon, Altitude(altitude))
                    elif (positionType == 3):
                        runway[runway.method_2(PositionType.END)] = Position(PositionType.END, None, xLat, yLon, Altitude(altitude))
                    elif (positionType == 4):
                        runway[runway.method_2(PositionType.THR)] = Position(PositionType.THR, None, xLat, yLon, Altitude(altitude))
                    elif (positionType == 5):
                        runway.Add(Position(PositionType.Position, None, xLat, yLon, Altitude(altitude)))
                    elif (positionType == 6):
                        runway[runway.method_2(PositionType.START)] = Position(PositionType.START, None, xLat, yLon, Altitude(altitude))
        elif byte_0 == 3:
            for i in range(positionCount):
                positionType = dataStream.readInt()
                xyFlag = dataStream.readBool()
                validIncludingAltitude = dataStream.readBool()
                if validIncludingAltitude:
                    xLat = dataStream.readDouble()
                    yLon = dataStream.readDouble()
                    altitude = dataStream.readDouble()

                    position = Position(positionType, None, None, None, Altitude(altitude), Degrees.smethod_1(xLat), Degrees.smethod_5(yLon)) if(not xyFlag) else Position(positionType, None, xLat, yLon, Altitude(altitude))
                    if (i >= 5):
                        runway.Add(position)
                    else:
                        runway[i] = position
        return runway



    #     if (byte_0 == 2):
    #         runway.name = Encoding.Default.GetString(binaryReader_0.ReadBytes(25)).Trim()
    #         runway.des1 = Encoding.Default.GetString(binaryReader_0.ReadBytes(2)).Trim()
    #         runway.des2 = Encoding.Default.GetString(binaryReader_0.ReadBytes(1)).Trim()
    #         int num = binaryReader_0.ReadInt32()
    #         for (int i = 0 i < num i++)
    #         {
    #             byte num1 = binaryReader_0.ReadByte()
    #             bool flag = Convert.ToBoolean(binaryReader_0.ReadInt16())
    #             double[] numArray = new double[3]
    #             if (flag)
    #             {
    #                 numArray[0] = binaryReader_0.ReadDouble()
    #                 numArray[1] = binaryReader_0.ReadDouble()
    #                 numArray[2] = binaryReader_0.ReadDouble()
    #                 if (num1 == 1)
    #                 {
    #                     runway[runway.method_2(PositionType.CWY)] = new Position(PositionType.CWY, numArray[0], numArray[1], new Altitude(numArray[2]))
    #                 }
    #                 elif (num1 == 2)
    #                 {
    #                     runway[runway.method_2(PositionType.SWY)] = new Position(PositionType.SWY, numArray[0], numArray[1], new Altitude(numArray[2]))
    #                 }
    #                 elif (num1 == 3)
    #                 {
    #                     runway[runway.method_2(PositionType.END)] = new Position(PositionType.END, numArray[0], numArray[1], new Altitude(numArray[2]))
    #                 }
    #                 elif (num1 == 4)
    #                 {
    #                     runway[runway.method_2(PositionType.THR)] = new Position(PositionType.THR, numArray[0], numArray[1], new Altitude(numArray[2]))
    #                 }
    #                 elif (num1 == 5)
    #                 {
    #                     runway.Add(new Position(PositionType.Position, numArray[0], numArray[1], new Altitude(numArray[2])))
    #                 }
    #                 elif (num1 == 6)
    #                 {
    #                     runway[runway.method_2(PositionType.START)] = new Position(PositionType.START, numArray[0], numArray[1], new Altitude(numArray[2]))
    #                 }
    #             }
    #         }
    #     }
    #     elif (byte_0 == 3)
    #     {
    #         runway.name = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()))
    #         runway.des1 = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()))
    #         runway.des2 = Encoding.Default.GetString(binaryReader_0.ReadBytes(binaryReader_0.ReadInt32()))
    #         int num2 = binaryReader_0.ReadInt32()
    #         for (int j = 0 j < num2 j++)
    #         {
    #             PositionType positionType = (PositionType)binaryReader_0.ReadByte()
    #             bool flag1 = binaryReader_0.ReadBoolean()
    #             if (binaryReader_0.ReadBoolean())
    #             {
    #                 position = (!flag1 ? new Position(positionType, Degrees.smethod_1(binaryReader_0.ReadDouble()), Degrees.smethod_5(binaryReader_0.ReadDouble()), new Altitude(binaryReader_0.ReadDouble())) : new Position(positionType, binaryReader_0.ReadDouble(), binaryReader_0.ReadDouble(), new Altitude(binaryReader_0.ReadDouble())))
    #                 if (j >= 5)
    #                 {
    #                     runway.Add(position)
    #                 }
    #                 else
    #                 {
    #                     runway[j] = position
    #                 }
    #             }
    #         }
    #     }
    #     return runway
    # }



class RunwayList(list):

    fileName = None

    @staticmethod
    def RunwayList():
        path = ""
        if define.obstaclePath != None:
            path = define.obstaclePath
        elif define.xmlPath != None:
            path = define.xmlPath
        else:
            path = define.appPath
        RunwayList.fileName = path + "/phxasar.dat"

    def __init__(self):
        list.__init__(self)

        self.HEADER = "PHXASA"
        self.VERSION = 3
    def Add(self, runway):
        self.append(runway)
    def Remove(self, item):
        self.remove(item)
    def IndexOf(self, item):
        i = 0
        for runway in self:
            if item.FullName == runway.FullName:
                return i
            i += 1
        return -1
            # self.index(item)
    def method_0(self, iwin32Window_0):
            if QFile.exists(RunwayList.fileName):
                fl = QFile.remove(RunwayList.fileName)

                file0 = QFile(RunwayList.fileName)
                file0.open(QIODevice.WriteOnly)

                # f = open(RunwayList.fileName, 'w')
                # file0.flush()
                # file0.close()

            else:
                file0 = QFile(RunwayList.fileName)
                file0.open(QIODevice.WriteOnly)

                # f = open(RunwayList.fileName, 'w')
                # file0.flush()
                # file0.close()

            # file0 = QFile(RunwayList.fileName)
            # file0.open(QIODevice.WriteOnly)
            dataStream = QDataStream(file0)
            dataStream.writeQString(QString("PHXASA"))
            dataStream.writeInt(3)
            dataStream.writeInt(len(self))

            for runway in self:
                runway.method_8(dataStream)
    #         using (BinaryWriter binaryWriter = new BinaryWriter(File.Open(RunwayList.fileName, FileMode.Create, FileAccess.Write, FileShare.Read)))
    #         {
    #             binaryWriter.Write(Encoding.Default.GetBytes("PHXASA"))
    #             binaryWriter.Write((byte)3)
    #             binaryWriter.Write(base.Count)
    #             foreach (Runway runway in this)
    #             {
    #                 runway.method_8(binaryWriter)
    #             }
    #         }
    #     }
    #     catch (Exception exception1)
    #     {
    #         Exception exception = exception1
    #         ErrorMessageBox.smethod_0(iwin32Window_0, string.Format(Messages.ERR_FAILED_TO_SAVE_RWY_DATA_FILE, exception.Message))
    #     }
    # }
    def method_1(self):
        self.sort(RunwayList.smethod_1)


    @staticmethod
    def smethod_0(iwin32Window_0):
        RunwayList.RunwayList()
        runwayList = RunwayList()
        if (not QFile.exists(RunwayList.fileName)):
            return runwayList
        # try
        # {
        file0 = QFile(RunwayList.fileName)
        file0.open(QIODevice.ReadOnly)
        dataStream = QDataStream(file0)
            # using (BinaryReader binaryReader = new BinaryReader(File.Open(RunwayList.fileName, FileMode.Open, FileAccess.Read)))
            # {
        str0 = dataStream.readQString()#Encoding.Default.GetString(binaryReader.ReadBytes("PHXASA".Length))
        num = dataStream.readInt()#binaryReader.ReadByte()
        if (not str0 == "PHXASA" or (num != 2 and num != 3)):
            return runwayList
        num1 = dataStream.readInt()
        for i in range(num1):
            runwayList.Add(Runway.smethod_0(dataStream, num))
        # catch (Exception exception1)
        # {
        #     Exception exception = exception1
        #     ErrorMessageBox.smethod_0(iwin32Window_0, string.Format(Messages.ERR_FAILED_TO_LOAD_RWY_DATA_FILE, exception.Message))
        # }
        runwayList.method_1()
        return runwayList

    @staticmethod
    def smethod_1(runway_0, runway_1):
        return 1 if(runway_0.FullName == runway_1.FullName) else -1
