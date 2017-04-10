# __author__ = 'Administrator'
class ComboBox:
    def __init__(self):
        pass

    @staticmethod
    def method_11(comboBoxObject,labelObject, string_0):
        if comboBoxObject.currentText() == "":
            return string_0 + labelObject.text() + "\t"
        captionAndUnit = labelObject.text()
        index = captionAndUnit.indexOf("(")
        caption = captionAndUnit
        unit = None
        if index >= 0:
            caption.remove(index, caption.length() - 1)
            captionAndUnit.remove(0, index)
            unit = captionAndUnit.remove(1, captionAndUnit.length() - 1)
        else:
            unit = ""

        return "%s%s\t%s %s"%(string_0, caption, comboBoxObject.currentText(), unit)

class LineEdit:
    def __init__(self):
        pass

    @staticmethod
    def method_7(lineEditObject,labelObject, string_0):
        captionAndUnit = labelObject.text()
        index = captionAndUnit.indexOf("(")
        caption = captionAndUnit
        if index >= 0:
            caption.remove(index, caption.length() - 1)
            captionAndUnit.remove(0, index)
            unit = captionAndUnit.remove(1, captionAndUnit.length() - 1)
            return "%s%s\t%s %s"%(string_0, caption, lineEditObject.text(), unit)
        return "%s%s\t%s"%(string_0, caption, lineEditObject.text() )
class AltitudeObject:
    def __init__(self):
        pass

    @staticmethod
    def method_8(AltitudeObject,labelObject, string_0, unit):

        return "%s%s\t%s %s"%(string_0, labelObject.text(), AltitudeObject.text(), unit)