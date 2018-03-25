class Attribute(object):

    def __init__(self,name,index,value,inverseValue):
        self.name = name
        self.index = index
        self.value = value
        self.inverseValue = inverseValue

    def __str__(self):
        return str(self.index)+" - "+self.name + ": " + self.value + ", "+self.inverseValue

    def getInverse(self,value):
        if value == self.value:
            return self.inverseValue
        elif value == self.inverseValue:
            return self.value
        else:
            return None

    def getInverseAsIndex(self,value):
        if value == self.value:
            return -1*self.index
        elif value == self.inverseValue:
            return self.index
        else:
            return None

    def __gt__(self, other):
        return self

    def getIndex(self):
        return self.index
    def getValue(self):
        return self.value
    def getInverseValue(self):
        return self.inverseValue