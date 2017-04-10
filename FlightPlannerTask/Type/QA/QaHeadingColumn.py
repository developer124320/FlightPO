

class QaHeadingColumn:
    def __init__(self, string_0 = "", int_0 = -1, bool_0 = False, iobstacleTableColumnFormatProvider_0 = None):
        self.caption = string_0;
        self.selected = bool_0;
        self.index = int_0;
        self.provider = iobstacleTableColumnFormatProvider_0;
    def method_0(self):
        return QaHeadingColumn(self.caption, self.index, self.selected, self.provider);
    def ToString(self):
        return self.caption

    def getCaption(self):
        return self.caption
    def setCaption(self, val):
        self.caption = val
    Caption = property(getCaption, setCaption, None, None)

    def getFormatProvider(self):
        return self.provider
    def setFormatProvider(self, val):
        self.provider = val
    FormatProvider = property(getFormatProvider, setFormatProvider, None, None)

    def getIndex(self):
        return self.index
    def setIndex(self, val):
        self.index = val
    Index = property(getIndex, setIndex, None, None)

    def getSelected(self):
        return self.selected
    def setSelected(self, val):
        self.selected = val
    Selected = property(getSelected, setSelected, None, None)