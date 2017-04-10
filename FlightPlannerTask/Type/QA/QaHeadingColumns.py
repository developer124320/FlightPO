


class QaHeadingColumns(list):
    def __init__(self):
        list.__init__()
    def Add(self, qaHeadingColumn):
        self.append(qaHeadingColumn)
    def method_0(self):
        qaHeadingColumn = QaHeadingColumns();
        for qaHeadingColumn1 in self:
            qaHeadingColumn.Add(qaHeadingColumn1.method_0());
        return qaHeadingColumn;