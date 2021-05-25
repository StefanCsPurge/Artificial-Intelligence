from repository import *
import numpy as np
import time


class Controller:
    def __init__(self, repo):
        # args - list of parameters needed in order to create the controller
        self.__repo = repo
        self.__currentPopulation = None

    def getDroneStartPosition(self):
        return self.__repo.getMap().getRandomEmptyPosition()

    def iteration(self, popSize):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parents - random
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors
        self.__currentPopulation.selection(popSize-2)  # natural selection
        popSize = popSize - 2

        i1 = randint(0, popSize - 1)  # select 2 random parents from those who survived
        i2 = randint(0, popSize - 1)
        while i1 == i2:
            i2 = randint(0, popSize - 1)
        parent1 = self.__currentPopulation.getIndividual(i1)
        parent2 = self.__currentPopulation.getIndividual(i2)

        offspring1, offspring2 = parent1.crossover(parent2)  # crossover the 2 selected parents
        offspring1.mutate()   # apply some random mutations to the solutions
        offspring2.mutate()
        self.__currentPopulation.addIndividual(offspring1)
        self.__currentPopulation.addIndividual(offspring2)

    def run(self, start_time, startCell, noOfIterations):
        # args - list of parameters needed in order to run the algorithm
        iterationCount = 0
        # until stop condition
        #    perform an iteration
        #    save the information needed for the statistics
        avgFitnesses = []
        times = []

        self.__currentPopulation.evaluate(startCell, self.__repo.getMap())
        while iterationCount <= noOfIterations:   # big enough so it can evolve
            avgFitnesses.append(np.average(self.__currentPopulation.getFitnessList()))
            times.append(time.time() - start_time)
            self.iteration(self.__currentPopulation.getPopulationSize())
            # evaluate the fitness score of the new generation
            self.__currentPopulation.evaluate(startCell, self.__repo.getMap())
            iterationCount += 1

        # return the results and the info for statistics
        return self.__currentPopulation.getAllIndividuals(), avgFitnesses, times
    
    def solver(self, m, popSize, startCell, noOfIterations):
        # args - list of parameters needed in order to run the solver
        
        # create the population
        self.__currentPopulation = self.__repo.createPopulation(popSize, m)
        print("Initial population created.")
        # self.__currentPopulation = self.__repo.getPopulation(0)

        # run the algorithm
        print("Executing population evolution, please wait...")
        start_time = time.time()
        individuals, avgF, times = self.run(start_time, startCell, noOfIterations)
        print("Evolutionary algorithm execution time:", time.time() - start_time, "s")

        # return the results and the statistics
        return individuals, avgF, times

    def makeRandomMap(self):
        self.__repo.getMap().randomMap()

    def getRepoMap(self):
        return self.__repo.getMap()

    def loadMap(self, file="map.in"):
        self.__repo.loadMapFromFile(file)

    def saveMap(self, file="map.in"):
        self.__repo.saveMapToFile(file)
