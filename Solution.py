class Solution(object):

    def __init__(self,array):
        self.array = array
        self.penalty = 0

    def __gt__(self, other):
        return self

    def __str__(self):
        return str(self.array) + " - Penalty -" +str(self.penalty)

    def getArray(self):
        return self.array

    def getPenalty(self):
        return self.penalty

    def addPenalty(self,penalty):
        self.penalty += penalty

    def checkAndUpdatePenalty(self,penalty,isAnd,leftValue,rightValue):
        if(isAnd):
            try:
                if(self.array.index(leftValue) and self.array.index(rightValue)):
                    return self
            except ValueError:
                self.penalty += penalty
                return self
        else:
            try:
                if(self.array.index(leftValue)):
                    return self
            except ValueError:
                try:
                    if (self.array.index(rightValue)):
                        return self
                except ValueError:
                    self.penalty += penalty
                    return self
