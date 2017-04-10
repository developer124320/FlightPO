

from Type.String import String

class Convert:
    @staticmethod
    def ToString(num, n):
        if n == 2:
            return bin(num).replace("0b", "")

    @staticmethod
    def ToBoolean(obj):
        if obj == None:
            return False
        else:
            return True