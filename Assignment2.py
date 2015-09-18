import heapq
import sys
import random
class Squares(object):
    def __init__(self, x, y, value ,passable):

        
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param passable is cell passable? not a wall?
        """
        self.passable = passable
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0
        self.estimate = 0
        self.sum = 0
        self.value = value 

class AStar(object):
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
            if height == 5: 
                width = len(Aline)
            
        height = height -1 
        
        #print height
       # print width
        self.grid_height = height
        self.grid_width = width

    def init_grid(self, C_linearguments ):
        
        tuple_dic = {}
        row_count = 0;
        f = open(C_linearguments[0])
        for line in f:
            Aline = line.split()
            tuple_temp = ()
            line_ints = [int(l[0]) for l in Aline]
            for i in range(len(Aline)):
                tuple_temp = (i,row_count)
                tuple_dic.update({(tuple_temp):Aline[i]})
            if i == (len(Aline)-1):
                row_count += 1 
        #print tuple_dic
       # print tuple_dic[(0,0)]
       
        passable = True
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in tuple_dic:
                    value = tuple_dic[(x,y)]
                    if value == 2: 
                        passable = False               
                    self.squares.append(Squares(x, y,value, passable))
       # print self.squares
        self.start = self.get_cell(0, 0)
        self.end = self.get_cell(5, 5)
       # print self.start
       # print self.end

    def Asharp_heuristic(self, cell):
        """
        Compute the heuristic passable H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic passable H
        """
        return  (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))
    def random_heuristic(self,cell): 
        """
            Returns random number below straight line estimate to calculate next 
            movement 

        """
        straightLineEstimate  = abs(cell.x - self.end.x) + abs(cell.y - self.end.y)
        if straightLineEstimate == 0:
            straightLineEstimate = 2

        randomHeuristic = random.randint(1,straightLineEstimate)
        if randomHeuristic == 0:
            randomHeuristic = 2
        return (randomHeuristic)
    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.squares[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list 
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
            if cell.y+1 < self.grid_height -1:
                cells.append(self.get_cell(cell.x+1,cell.y+1))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
                
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print 'path: cell: %d,%d' % (cell.x, cell.y)

    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values

        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.sum < cell2.sum:
            return -1
        elif cell1.sum > cell2.sum:
            return 1
        return 0
    
    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        int_value = 0
        x1 = cell.x 
        x2 = adj.x
        y1 = cell.y
        y2 = adj.y 

        Xdif = (x1 - x2)
        if Xdif != 0:
            slope = (y1 - y2)/Xdif
            if slope != 0: 
              int_value = int_value + 14 
                #print "Diagnol"

        if adj.value == 0:
            int_value = int_value + 10
        else:
            int_value = int_value + 20
        adj.cost = cell.cost + int_value
        if (self.heuristic == True):
            adj.estimate = self.Asharp_heuristic(adj)
            adj.parent = cell
            adj.sum = adj.estimate + adj.cost
        else:
            adj.estimate = self.random_heuristic(adj)
            adj.parent = cell
            adj.sum = adj.estimate + adj.cost

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.sum, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.passable and adj_cell not in self.closed:
                    if (adj_cell.sum, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.cost > cell.cost + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.sum, adj_cell))

C_linearguments = []

C_linearguments.append(str(sys.argv[1]))
C_linearguments.append(str(sys.argv[2]))
    

a = AStar(C_linearguments)
a.init_grid( C_linearguments )
a.process()

