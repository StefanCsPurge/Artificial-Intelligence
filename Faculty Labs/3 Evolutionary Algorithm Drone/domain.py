# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np
import copy


# the class gene can be replaced with int or float, or other types
# depending on your problem's representation
class Gene:  # direction
    def __init__(self):
        # random initialise the gene according to the representation
        self.direction = choice(v)

    def changeDirection(self):
        d = choice(v)
        while d == self.direction:
            d = choice(v)
        self.direction = d


class Individual:  # path
    def __init__(self, size=0):
        self.__size = size
        self.__x = [Gene() for _ in range(self.__size)]
        self.__f = None

    def get_fitness(self):
        return self.__f

    def get_gene(self, index):
        return self.__x[index]

    def set_gene(self, index, newGene):
        self.__x[index] = newGene

    def getPath(self, startCell, mapNxN):
        path = [(startCell[0], startCell[1])]
        currentCell = copy.deepcopy(startCell)
        for g in self.__x:
            currentCell[0] += g.direction[0]
            currentCell[1] += g.direction[1]
            if not mapNxN.checkValidMapPosition(currentCell):
                break
            path.append((currentCell[0], currentCell[1]))
        return path

    def fitness(self, startCell, mapNxN):
        # compute the fitness for the individual
        # and save it in self.__f
        cells_discovered = {(startCell[0], startCell[1])}
        currentCell = copy.deepcopy(startCell)
        lastCell = copy.deepcopy(startCell)
        for g in self.__x:
            cells_discovered = cells_discovered.union(mapNxN.readUDMSensors(currentCell))
            currentCell[0] += g.direction[0]
            currentCell[1] += g.direction[1]
            if not mapNxN.checkValidMapPosition(currentCell):
                break
            lastCell = copy.deepcopy(currentCell)
        # print(startCell,lastCell)
        if lastCell[0] == startCell[0] and lastCell[1] == startCell[1]:   # make drone return to its starting position
            self.__f = len(cells_discovered)
            # print("End of path; cells explored: ", self.__f)
        else:
            self.__f = 1
        # self.__f = len(cells_explored)

    def mutate(self, mutateProbability=0.07):
        for g in self.__x:
            if random() < mutateProbability:
                g.changeDirection()
            # perform a mutation with respect to the representation

    """
        For crossover we can take the genes values from the two parents, and add them to the children like this: 
            -parent1 gene to child1 and parent2 gene to child2
            OR 
            -parent2 gene to child1 and parent1 gene to child2
        this way we ensure that each child gets something from each of the two parents
    """
    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size) 
        for i in range(self.__size):
            if random() < crossoverProbability:
                # perform the crossover between the self and the otherParent
                offspring1.set_gene(i, copy.deepcopy(otherParent.get_gene(i)))
                offspring2.set_gene(i, copy.deepcopy(self.__x[i]))
            else:
                offspring1.set_gene(i, copy.deepcopy(self.__x[i]))
                offspring2.set_gene(i, copy.deepcopy(otherParent.get_gene(i)))
        
        return offspring1, offspring2

    
class Population:  # several paths
    def __init__(self, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for _ in range(populationSize)]
        
    def evaluate(self, startCell, mapNxN):
        # evaluates the population
        for x in self.__v:
            x.fitness(startCell, mapNxN)
            
    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        if k < 0:
            self.__v = []
            k = 0
        else:
            self.__v = sorted(self.__v, key=lambda x: x.get_fitness(), reverse=True)[:k]
        self.__populationSize = k
        return self.__v

    def getIndividual(self, idx):
        return self.__v[idx]

    def addIndividual(self, individual):
        self.__v.append(individual)
        self.__populationSize += 1

    def getAllIndividuals(self):
        return self.__v

    def getPopulationSize(self):
        return self.__populationSize

    def getFitnessList(self):
        return [x.get_fitness() for x in self.__v]


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1
                
    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, currentCell):
        x = currentCell[0]
        y = currentCell[1]
        scanned_cells = {(x,y)}
        # UP
        xf = x - 1
        while (xf >= 0) and (self.surface[xf][y] == 0):
            xf = xf - 1
            scanned_cells.add((xf,y))
        # DOWN
        xf = x + 1
        while (xf < self.n) and (self.surface[xf][y] == 0):
            xf = xf + 1
            scanned_cells.add((xf,y))
        # LEFT
        yf = y + 1
        while (yf < self.m) and (self.surface[x][yf] == 0):
            yf = yf + 1
            scanned_cells.add((x,yf))
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.surface[x][yf] == 0):
            yf = yf - 1
            scanned_cells.add((x,yf))
        return scanned_cells

    def checkValidMapPosition(self, cell):
        x = cell[0]
        y = cell[1]
        if x is None or y is None:
            return False
        return 0 <= x < self.n and 0 <= y < self.m and self.surface[x][y] != 1

    def markVisited(self, cell):
        x = cell[0]
        y = cell[1]
        if self.checkValidMapPosition(cell):
            self.surface[x][y] = 2

    def getRandomEmptyPosition(self):
        x = randint(0, self.n-1)
        y = randint(0, self.m-1)
        while self.surface[x][y] == 1:
            x = randint(0, self.n-1)
            y = randint(0, self.m-1)
        return [x, y]
