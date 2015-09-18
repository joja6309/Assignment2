import heapq
import sys
import random
from grid import *
from squares import *
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



C_linearguments = []
C_linearguments.append(str(sys.argv[1]))
C_linearguments.append(str(sys.argv[2]))
instance = Grid(C_linearguments)
instance.generate_grid( C_linearguments )
instance.search_driver()
