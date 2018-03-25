class Constraint(object):

    def __init__(self, leftSide ,rightSide ,comparator):
        self.leftSide = leftSide
        self.rightSide = rightSide
        self.comparator = comparator

    def __str__(self):
        return self.leftSide + " "+self.comparator+" "+self.rightSide
