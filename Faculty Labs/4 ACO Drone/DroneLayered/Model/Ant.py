from random import *
from Model.Sensor import Sensor


class Ant:
    def __init__(self, sensors: list, shortestPathsDict: dict, droneEnergy):
        self.__sensors = sensors
        self.__shortestPathsDict = shortestPathsDict
        self.__n = len(sensors)
        self.__path = [sensors[0]]
        # self.__visited = []  # visited will keep track of the nodes visited in the current graph
        self.droneEnergy = droneEnergy

    def fitness(self):  # the no. of squares a sensor scans
        # if len(self.__path) != self.__n:
        #     return 1
        fitness = 0
        for sensor in self.__path:
            fitness += sensor.goodArea
        return fitness

    def distMoveHeuristic(self, s: Sensor):
        # energy, area = s.getOptimalEnergyArea()
        return s.goodArea / (len(self.__shortestPathsDict[self.__path[-1],s]) + s.goodEnergy)

    def distMove(self, nextSensor: Sensor):
        currentSensor = self.__path[-1]
        shortestPathLen = len(self.__shortestPathsDict[currentSensor,nextSensor])
        goodEnergy = nextSensor.goodEnergy   # .getOptimalEnergyArea()[0]
        return shortestPathLen + goodEnergy

    def nextMoves(self):
        # returns a list of possible moves from current state
        possible_moves = []
        for sensor in self.__sensors:
            if sensor not in self.__path and self.distMove(sensor) <= self.droneEnergy:
                possible_moves.append(sensor)
        return possible_moves.copy()

    def addMove(self, q0, trace, alpha, beta):
        # add a new position to the ant solution if possible
        p = {}  # probabilities
        for s in self.__sensors:
            p[s] = 0

        # positions that are no good are marked with 0
        nextSteps = self.nextMoves().copy()

        if len(nextSteps) == 0:
            return False

        for sensor in nextSteps:
            p[sensor] = self.distMoveHeuristic(sensor)

        lastSensor = self.__path[-1]
        # calc product trace^alpha and visibility^beta
        p = [(p[s] ** beta) * (trace[lastSensor,s] ** alpha) for s in self.__sensors]

        if random() < q0:
            # add the best move from the possible moves
            p = [[self.__sensors[i], p[i]] for i in range(len(p))]
            maxP = max(p, key=lambda el: el[1])
            self.droneEnergy -= self.distMove(maxP[0])
            self.__path.append(maxP[0])
        else:
            # add with a probability a possible road
            s = sum(p)
            if s == 0:
                # print("Sum of products is 0 :(")
                nextStep = choice(nextSteps)
                self.droneEnergy -= self.distMove(nextStep)
                self.__path.append(nextStep)
                return True
            p = [p[i] / s for i in range(len(p))]
            p = [sum(p[0:i+1]) for i in range(len(p))]
            r = random()
            i = 0
            while r > p[i]:
                i = i + 1

            self.droneEnergy -= self.distMove(self.__sensors[i])
            self.__path.append(self.__sensors[i])
        return True

    def getPath(self):
        return self.__path
