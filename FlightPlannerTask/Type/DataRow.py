


class DataRow(dict):
    def __init__(self, nameList0 = []):
        dict.__init__(self)
        self.nameList = []
        if len(nameList0) != 0:
            for name in nameList0:
                self.update({name:""})
            self.nameList = nameList0
    def setItem(self, index, data):
        self[self.nameList[index]] = data
    def get_Length(self):
        return len(self)
    Length = property(get_Length, None, None, None)

    def __eq__(self, other):
        if other == None:
            return 0
        if len(self) == len(other):
            for nameSlef in self:
                count = 0
                for nameOther in other:
                    if nameSlef == nameOther:
                        count += 1
                if count == 1:
                    if self[nameSlef] == other[nameSlef]:
                        continue
                    else:
                        return 0
                else:
                    return 0
            return 1
        return 0
