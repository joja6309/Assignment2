class Squares(object):
    def __init__(self, x, y, value ,passable):
        self.passable = passable
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0
        self.estimate = 0
        self.sum = 0
        self.value = value
        self.evaluation_number = 0 
