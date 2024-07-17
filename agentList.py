import numpy as np

class AgentList:
    def init(self, n):
        #TYPE, ID, TTL, IDCELL, DEAD/NOTDEAD
        self.list = np.ndarray(shape=(n, 5), dtype=np.int64)
        #POSX, POSY
        self.coords = np.ndarray(shape=(n,2), dtype=float)
        #set all to -1
        self.list.fill(-1)
        #set all to -1
        self.coords.fill(-1)
        #Add all ids to empty cells
        self.emptycells = [x for x in range(0,n)]
        self.n = n
        #Times that the list needed to be expanded
        self.times = 0

    def firstEmpty(self):
        #If there is not any place in the list available anymore
        if(len(self.emptycells)==0):
            #increase time
            self.times = self.times + 1
            #Create an equal sized list
            newlist = np.ndarray(shape=(self.n*self.times, 5), dtype=float)
            newcoords = np.ndarray(shape=(self.n*self.times, 2), dtype=float)
            newlist.fill(-1)
            newcoords.fill(-1)
            #Concate the matrices
            self.list = np.concatenate([self.list, newlist])
            self.coords =  np.concatenate([self.coords, newcoords])
            #Add to emptycells the new available position
            self.emptycells = [x for x in range(self.n*self.times,self.n*self.times+self.n*self.times)]
        #Pick the first empty id
        x = self.emptycells.pop(0)
        return x

    def nonZero(self):
        #Return the list of all non-zeros elements
        x = np.nonzero(self.list != -1)[0][0::5]
        #It shuffle the ids (in order to not add rabbits and wolve all one consequent to the other nor moving than following some order)
        #np.random.shuffle(x)
        return x

    def clean(self, id):
        #Clean the coords
        self.coords[id] = -1
        #Clean the lists
        self.list[id] = -1
        #Add the id to empty cells in a way that be re-assigned
        self.emptycells.append(id)
