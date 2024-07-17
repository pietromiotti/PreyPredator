import numpy as np
import math

class Map:
    
    X = 0
    Y = 1
    Type = 2
    XLETTER = 'x'
    YLETTER = 'y'
    coordLetter = ['E','W','N','S','SE','SW','NE','NW']
    E = 0
    W = 1
    N = 2
    S = 3
    SE = 4
    SW = 5
    NE = 6
    NW = 7

    coords = {
        'E':{'x': 0, 'y': 1},
        'W':{'x': 0, 'y':-1},
        'N':{'x':-1, 'y':0},
        'S':{'x':1, 'y':0},
        'SE':{'x':1, 'y':1},
        'SW':{'x':1, 'y':-1},
        'NE':{'x':-1, 'y':1},
        'NW':{'x':-1, 'y':-1},
    }

    #COmpute the map
    def init(self, rows, columns):
        self.map = np.ndarray(shape=(rows,columns), dtype=int)
        self.rows = rows
        self.columns = columns
        self.size = rows*columns
        self.cells = {}
        self.coords = np.ndarray(shape=(rows*columns, 2), dtype=int)
        self.neighbours = np.ndarray(shape=(rows*columns, 8), dtype=int)

        #Populate the map with it's id
        for i in range(0, rows):
            for j in range(0, columns):
                self.map[i,j] = i*rows+j
                self.cells[i*rows+j] = []
                self.coords[i*rows+j] = [i,j]
        #Populate the neihbours
        for key in self.cells:
            X = self.coords[key][0]
            Y = self.coords[key][1]
            e = self.map[X, (Y+1)%self.columns]
            w = self.map[X, (Y-1)%self.columns]
            s = self.map[(X+1)%self.rows, Y]
            n = self.map[(X-1)%self.rows, Y]
            se = self.map[(X+1)%self.rows, (Y+1)%self.columns]
            sw = self.map[(X+1)%self.rows, (Y-1)%self.columns]
            ne = self.map[(X-1)%self.rows, (Y+1)%self.columns]
            nw = self.map[(X-1)%self.rows, (Y-1)%self.columns]
            self.neighbours[key] = np.array([e, w, n, s, se, sw, ne, nw])


    #Get the corresponding ID
    def retreiveId(self, i, j):
        return math.trunc(i)*self.rows+math.trunc(j)
