import numpy as np
from Map import Map
import math
import random
from random import seed
from random import randint
from datetime import datetime
import time
import matplotlib.pyplot as plt
from agentList import AgentList
import signal


class Particles:
    #Define Environmental VARIABLEs
    mean = 0
    variance = 0.5
    timetoliveWolf = 50
    timetoliveRabbit = 100
    probToReproduce = 0.02
    probToEat = 0.02

    RABBIT = 0
    WOLF = 1

    TYPE = 0
    ID = 1
    TTL = 2
    IDCELL = 3
    DEATH = 4

    POSX = 0
    POSY = 1
    NEWPOSX = 2
    NEWPOSY = 3

    EMPTY = -1
    DEAD = 1
    NOTDEAD = 0

    def init(self, map, rabbits, wolves, maxiteration):

        #Initialize variables
        self.map = map
        self.totalRabbits = rabbits
        self.totalWolves = wolves
        self.totalNumParticles = self.totalRabbits + self.totalWolves
        self.maxiteration = maxiteration
        self.toBeRemoved = []
        self.totalAgents = AgentList()
        self.totalAgents.init(self.totalNumParticles)

        #RAbbits initializations
        for i in range(0, rabbits):
            pos = [np.round(random.uniform(0, map.rows),3) , np.round(random.uniform(0, map.columns),3)]
            ttl = random.randint(1, self.timetoliveRabbit)

            #Get the first Empty ID where to place the agent
            id = self.totalAgents.firstEmpty()

            #Normalize the coords, just to avoid "border cells"
            pos[0] = pos[0]%self.map.rows
            pos[1] = pos[1]%self.map.columns

            #Compute the cell ID where to place the agent
            x = math.trunc(pos[0])%self.map.rows
            y = math.trunc(pos[1])%self.map.columns
            idcell = self.map.map[x,y];

            #init agents list and coords
            self.totalAgents.list[id] = np.array([self.RABBIT, id, ttl, idcell, self.NOTDEAD])
            self.totalAgents.coords[id] = np.array([pos])

            #Add the agent to the map, in the corresponding map -cell
            self.map.cells[idcell].append(id)

        #Same steps as rabbits are followed
        for i in range(0, wolves):
            pos = np.array([np.round(random.uniform(0, map.rows),3), np.round(random.uniform(0, map.columns),3)])

            ttl = self.timetoliveWolf
            id = self.totalAgents.firstEmpty()

            pos[0] = pos[0]%self.map.rows
            pos[1] = pos[1]%self.map.columns

            x = math.trunc(pos[0])%self.map.rows
            y = math.trunc(pos[1])%self.map.columns

            idcell = self.map.map[x,y];

            self.totalAgents.list[id] = np.array([self.WOLF, id, ttl, idcell, self.NOTDEAD])
            self.totalAgents.coords[id] = np.array([pos])

            self.map.cells[idcell].append(id)

    #Moving means compute new movements and then update the current position, and the cell-list itself
    def moveRabbit(self, idrabbit):
        x_1 = np.random.normal(self.mean, self.variance)
        y_1 = np.random.normal(self.mean, self.variance)

        #Remove from old cellList
        self.map.cells[int(self.totalAgents.list[idrabbit,self.IDCELL])].remove(idrabbit)

        #compute new positions
        self.totalAgents.coords[idrabbit,self.POSX] = (self.totalAgents.coords[idrabbit,self.POSX]+ x_1)%self.map.rows
        self.totalAgents.coords[idrabbit,self.POSY] = (self.totalAgents.coords[idrabbit,self.POSY]+ y_1)%self.map.columns

        #compute truncate x and y, necessary to compute the new celllist
        x = math.trunc(self.totalAgents.coords[idrabbit,self.POSX])%self.map.rows
        y = math.trunc(self.totalAgents.coords[idrabbit,self.POSY])%self.map.columns

        #Compute new cell list
        newcellID = self.map.map[x,y];

        self.map.cells[newcellID].append(idrabbit)
        self.totalAgents.list[idrabbit,self.IDCELL] = newcellID

    #Moving means compute new movements and then update the current position, and the cell-list itself
    def moveWolf(self, idwolf):
        x_1 = np.random.normal(self.mean, self.variance)
        y_1 = np.random.normal(self.mean, self.variance)

        #Remove from old cellList
        self.map.cells[int(self.totalAgents.list[idwolf,self.IDCELL])].remove(idwolf)

        #Compute new positions
        self.totalAgents.coords[idwolf,self.POSX] = (self.totalAgents.coords[idwolf,self.POSX]+ x_1)%self.map.rows
        self.totalAgents.coords[idwolf,self.POSY] = (self.totalAgents.coords[idwolf,self.POSY]+ y_1)%self.map.columns

        #compute truncate x and y, necessary to compute the new celllist
        x = math.trunc(self.totalAgents.coords[idwolf,self.POSX])%self.map.rows
        y = math.trunc(self.totalAgents.coords[idwolf,self.POSY])%self.map.columns

        newcell = self.map.map[x,y];

        #Append to the map
        self.map.cells[newcell].append(idwolf)
        #Update the celllist
        self.totalAgents.list[idwolf,self.IDCELL] = newcell


    #Check the expiration of ttl
    def updatettl(self, agentid):
        if(self.totalAgents.list[agentid,self.DEATH] == self.NOTDEAD):
            if(self.totalAgents.list[agentid,self.TTL] <= 0):
                #Decrease the global countes
                if(self.totalAgents.list[agentid,self.TYPE]==self.RABBIT):
                    self.totalRabbits=self.totalRabbits-1
                elif(self.totalAgents.list[agentid,self.TYPE]==self.WOLF):
                    self.totalWolves=self.totalWolves-1

                #Mark the agent as DEAD
                self.totalAgents.list[agentid,self.DEATH] = self.DEAD
                #Append the agent to the list of agents that need to be removed at the end of the turn
                self.toBeRemoved.append(agentid)
            else:
                self.totalAgents.list[agentid,self.TTL] = self.totalAgents.list[agentid,self.TTL]-1


    #Reproduce means create a new agent in the same position
    def reproduceRabbit(self, rabbitid):
        prob = random.uniform(0, 1)
        if prob<self.probToReproduce:
            rabbit = self.totalAgents.list[rabbitid]
            rabbitCoords = self.totalAgents.coords[rabbitid]

            #Get the first empty id where to place
            newid = self.totalAgents.firstEmpty()

            #Populate the new agent
            self.totalAgents.list[newid] = np.array([self.RABBIT, newid, self.timetoliveRabbit, rabbit[self.IDCELL], self.NOTDEAD])

            #Update the values in the list of coords
            self.totalAgents.coords[newid] =  np.array([rabbitCoords])

            self.map.cells[int(self.totalAgents.list[newid,self.IDCELL])].append(newid)


    def eatWolf(self, wolfid, rabbitid):
        prob = random.uniform(0, 1)
        eat = 0
        if prob<self.probToEat:
            #Reset the ttl of the wold
            self.totalAgents.list[wolfid,self.TTL] = self.timetoliveWolf
            #Reproduce
            self.reproduceWolf(wolfid)
            eat =1
        return eat

    #Same steps for the corresponding rabbit reproduction funciton are followed
    def reproduceWolf(self, wolfid):
        prob = random.uniform(0, 1)
        if prob<self.probToReproduce:
            wolf = self.totalAgents.list[wolfid]
            wolfCoords = self.totalAgents.coords[wolfid]

            #GET NEW WOLF ID
            newid = self.totalAgents.firstEmpty()

            #UPDATE THE LIST
            self.totalAgents.list[newid] = np.array([self.WOLF, newid, self.timetoliveWolf, wolf[self.IDCELL], self.NOTDEAD])
            self.totalAgents.coords[newid] = np.array([wolfCoords])

            #UPDATE TO THE MAP
            self.map.cells[int(self.totalAgents.list[newid,self.IDCELL])].append(newid)

    #Main iteration
    def lifeCycle(self):
        iter = 1

        #Plotting varibales
        fig,ax = plt.subplots()
        # Initial plot setup
        line_rabbits, = ax.plot([], [], 'r', label='Rabbits')
        line_wolves, = ax.plot([], [], 'b', label='Wolves')

        # Plot the legend only once
        plt.legend()

        plt.show(block=False)
        axis=[0]
        #Extra variables needed for plotting purpose
        rabbits= [self.totalRabbits]
        wolves = [self.totalWolves]

        #While finished iterations
        while(iter < self.maxiteration):

            for agentId in self.totalAgents.nonZero():
                agent = self.totalAgents.list[agentId]

                if(agent[self.DEATH] == self.NOTDEAD):

                    #If rabbit
                    if(agent[self.TYPE] == self.RABBIT):
                        #move
                        self.moveRabbit(agentId)
                        #Reproduce
                        self.reproduceRabbit(agentId)

                    elif(agent[self.TYPE] == self.WOLF):
                        self.moveWolf(agentId)
                        #Add the current cell to its neighbour cell list
                        list = self.map.neighbours[int(self.totalAgents.list[agentId,self.IDCELL])]
                        list = np.append(list,int(self.totalAgents.list[agentId,self.IDCELL]))

                        #Check if the wolf has a rabbit in his neighbourhood and try to eat it.
                        for neighbourCell in list:
                            for agentNeighID in self.map.cells[neighbourCell]:
                                agentNeigh = self.totalAgents.list[agentNeighID]
                                if(agentNeigh[self.TYPE] == self.RABBIT):
                                    if(np.linalg.norm(self.totalAgents.coords[agentNeighID] - self.totalAgents.coords[agentId]) < 0.5):
                                        if(self.eatWolf(agentId,agentNeighID)):
                                            self.totalAgents.list[agentNeighID,self.DEATH] = self.DEAD




            #Compute Live Cells
            notDeadCells = np.argwhere(self.totalAgents.list[:,self.DEATH] == self.NOTDEAD)
            #Update the Time to leave (the age of the particles)
            self.totalAgents.list[notDeadCells,self.TTL] = self.totalAgents.list[notDeadCells,self.TTL]-1
            #compute the particles that need to be removed
            deadCells = np.argwhere(self.totalAgents.list[:,self.TTL] == 0)
            #Concatenate this list to all the rabbits that have been eaten during this iteration
            deadCells = np.append(deadCells, np.argwhere(self.totalAgents.list[:,self.DEATH] == self.DEAD))

            #Remove everybody from the lists
            for id in deadCells:
                #id = int(self.toBeRemoved.pop(0))
                if(self.totalAgents.list[id,self.TYPE] != self.EMPTY):
                    #remove from the map
                    self.map.cells[int(self.totalAgents.list[id,self.IDCELL])].remove(id)
                    #clean the lists (both attribute list and coordinates one)
                    self.totalAgents.clean(id)

            self.totalRabbits = len(np.argwhere(self.totalAgents.list[:,self.TYPE] == self.RABBIT))
            self.totalWolves= len(np.argwhere(self.totalAgents.list[:,self.TYPE] == self.WOLF))

            
            #REAL TIME PLOTTING
            ax.plot(axis,rabbits, 'r')
            ax.plot(axis,wolves, 'b')
            fig.canvas.draw()
            plt.pause(0.00001)
            plt.show(block=False)
            

            axis.append(iter)
            rabbits.append(self.totalRabbits)
            wolves.append(self.totalWolves)
            print("ITER", iter, "RABBITS:", self.totalRabbits, "WOLVES: ", self.totalWolves)
            iter = iter+1

            #If you want to plot and do not want to wait until the max iteration. Press Control C
            def handler(signum, frame):
                plt.plot(axis, rabbits)
                plt.plot(axis, wolves)
                plt.show(block=True)
                exit(1)

            signal.signal(signal.SIGINT, handler)

        plt.plot(axis, rabbits)
        plt.plot(axis, wolves)
        plt.show(block=True)
