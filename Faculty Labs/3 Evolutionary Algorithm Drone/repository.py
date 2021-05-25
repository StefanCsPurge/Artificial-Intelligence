# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self):
        self.__populations = []
        self.cmap = Map()
        
    def createPopulation(self, populationSize, individualSize):
        # args = [populationSize, individualSize] -- you can add more args
        p = Population(populationSize, individualSize)
        self.__populations.append(p)
        return p

    #    load and save from file, etc
    def loadPopulationsFromFile(self, popFile):
        file_handler = open(popFile, 'r')
        self.__populations = pickle.load(file_handler)
        file_handler.close()

    def savePopulationsToFile(self, popFile):
        file_handler = open(popFile, 'w')
        pickle.dump(self.__populations, file_handler)
        file_handler.close()

    def getAllPopulations(self):
        return self.__populations

    def getPopulation(self, idx):
        return self.__populations[idx]

    def getMap(self):
        return self.cmap

    def setMap(self, newMap):
        self.cmap = newMap

    def loadMapFromFile(self, mapFile):
        file_handler = open(mapFile, 'rb')
        self.cmap = pickle.load(file_handler)
        file_handler.close()

    def saveMapToFile(self, mapFile):
        file_handler = open(mapFile, 'wb')
        pickle.dump(self.cmap, file_handler)
        file_handler.close()
