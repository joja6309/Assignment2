import heapq
import sys
import random
from squares import *

class Grid(object):
    def __init__(self,  C_linearguments ):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.squares = []
        if C_linearguments[1] == "1":
            self.heuristic = True 
        else: 
            self.heuristic = False
        height = 0
        width = 0
        f = open(C_linearguments[0])
        for line in f:
            Aline = line.split()
            height += 1
           # print height
            if height == 5: 
                width = len(Aline)
            
       
        
        #print height
       # print width
        self.grid_height = height
        self.grid_width = width
    def generate_grid(self, C_linearguments ):
        tuple_dic = {}
        row_count = 0;
        f = open(C_linearguments[0])
        for line in f:
            Aline = line.split()
            tuple_temp = ()
            line_ints = [int(l[0]) for l in Aline]
            for i in range(self.grid_width):
                
                tuple_temp = (i,row_count)
                
                tuple_dic.update({(tuple_temp):Aline[i]})
            row_count += 1 
            
        passable = True
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in tuple_dic:
                    value = tuple_dic[(x,y)]
                    if value == 2: 
                        passable = False   
                    
                    self.squares.append(Squares(x, y,value, passable))
                    
         
        self.start = self.get_Square(0, self.grid_height)
        self.end = self.get_Square(self.grid_width-1, 0)
       
    def random_heuristic(self,square): 
        straightLineEstimate  = abs(square.x - self.end.x) + abs(square.y - self.end.y)
        if straightLineEstimate == 0:
            straightLineEstimate = 2
        randomHeuristic = random.randint(1,straightLineEstimate)
        if randomHeuristic == 0:
            randomHeuristic = 2
        return (randomHeuristic)
    def Asharp_heuristic(self, square):
        return  (abs(square.x - self.end.x) + abs(square.y - self.end.y))
    def get_Square(self, x, y):
       
        return self.squares[x * self.grid_height + y]
    def addEdges(self, square):
        squares = []
        if square.x < self.grid_width-1:
            squares.append(self.get_Square(square.x+1, square.y))
            if square.y+1 < self.grid_height -1:
                squares.append(self.get_Square(square.x+1,square.y+1))
        if square.y > 0:
            squares.append(self.get_Square(square.x, square.y-1))
        if square.x > 0:
            squares.append(self.get_Square(square.x-1, square.y))
        if square.y < self.grid_height-1:
            squares.append(self.get_Square(square.x, square.y+1))  
        return squares
    def display_path(self):
        square = self.end


        print "Start: ", (0,self.grid_height)
        print "End: ", (self.grid_width, 0)
        i = True
        print "Printing Calculated Path: "
        print "========================"
        while square.parent is not self.start:
            if i == True:
                print "Cost of Path: ", square.sum
                i = False
            square = square.parent
            print 'square: %d,%d' % (square.x, square.y)
           
        print 'evaluations: %d'%(self.evaluation_number)


    def compare(self, square1, square2):
        if square1.sum < square2.sum:
            return -1
        elif square1.sum > square2.sum:
            return 1
        return 0
    
    def update_square(self, adjacent, square):
        self.evaluation_number +=1

        int_value = 0
        x1 = square.x 
        x2 = adjacent.x
        y1 = square.y
        y2 = adjacent.y 
        Xdif = (x1 - x2)
        if Xdif != 0:
            slope = (y1 - y2)/Xdif
            if slope != 0: 
              int_value = int_value + 14         
        if adjacent.value == 0:
            int_value = int_value + 10
        else:
            int_value = int_value + 20
        adjacent.cost = square.cost + int_value
        if (self.heuristic == True):
            adjacent.estimate = self.Asharp_heuristic(adjacent)
            adjacent.parent = square
            adjacent.sum = adjacent.estimate + adjacent.cost
        else:
            adjacent.estimate = self.random_heuristic(adjacent)
            adjacent.parent = square
            adjacent.sum = adjacent.estimate + adjacent.cost

    def search_driver(self):
        self.evaluation_number = 0
        heapq.heappush(self.opened, (self.start.sum, self.start))
        while len(self.opened):
            
            f, square = heapq.heappop(self.opened)
            self.closed.add(square)
            if square is self.end:
                self.display_path()
                break
            adjacent_squares = self.addEdges(square)
            for adjacent_square in adjacent_squares:
                if adjacent_square.passable and adjacent_square not in self.closed:
                    if (adjacent_square.sum, adjacent_square) in self.opened:
                        if adjacent_square.cost > square.cost + 10:
                            self.evaluation_number +=1
                            self.update_square(adjacent_square, square)
                    else:
                        self.update_square(adjacent_square, square)
                        heapq.heappush(self.opened, (adjacent_square.sum, adjacent_square))
