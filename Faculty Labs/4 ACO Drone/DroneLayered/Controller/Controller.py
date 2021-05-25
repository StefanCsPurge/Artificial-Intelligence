
import numpy as np
import heapq

from Model.Ant import Ant
from Model.Sensor import Sensor


def get_neighbors(c):
    return [(c[0] - 1, c[1]), (c[0] + 1, c[1]), (c[0], c[1] - 1), (c[0], c[1] + 1)]


# calculate our H metric
def heuristic_distance(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def reconstructPath(start,goal,came_from):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


class Controller:
    def __init__(self, mapM, dronePos, droneEnergy, sensorsPos):
        self.__mapM = mapM
        self.__dronePos = dronePos
        self.__droneEnergy = droneEnergy
        self.__sensorsPos = sensorsPos
        self.__sensors = [Sensor(pos) for pos in sensorsPos]
        self.__sensors.insert(0, Sensor(dronePos))  # add drone start
        self.__problemSize = len(self.__sensors)
        self.__sensorsPaths = dict()
        self.__noEpoch = 0
        self.__noAnts = 0
        self.__alpha = 0.0
        self.__beta = 0.0
        self.__rho = 0.0
        self.__q0 = 0.0
        self.__pheromoneTrails = dict()

    def setACOParameters(self, noEpoch, noAnts, alpha, beta, rho, q0):
        self.__noEpoch = noEpoch
        self.__noAnts = noAnts
        self.__alpha = alpha
        self.__beta = beta
        self.__rho = rho
        self.__q0 = q0

    def epoch(self):
        # initialize ant population
        for s in self.__sensors[1:]:
            s.setGoodEnergyArea()
        ants = [Ant(self.__sensors, self.__sensorsPaths, self.__droneEnergy) for _ in range(self.__noAnts)]

        # While the no. of steps required to identify the optimal solution is not performed
        for i in range(self.__problemSize):
            for ant in ants:
                ant.addMove(self.__q0, self.__pheromoneTrails, self.__alpha, self.__beta)

        fitnesses = [ants[i].fitness() for i in range(len(ants))]
        deltaTrace = [1.0 / (fitnesses[i] if fitnesses[i] > 0 else 1) for i in range(len(ants))]

        for key in self.__pheromoneTrails.keys():
            self.__pheromoneTrails[key] = (1 - self.__rho) * self.__pheromoneTrails[key]

        for i in range(len(ants)):
            currentAntPath = ants[i].getPath()
            for j in range(len(currentAntPath)-1):
                s1 = currentAntPath[j]
                s2 = currentAntPath[j+1]
                self.__pheromoneTrails[s1,s2] = self.__pheromoneTrails[s1,s2] + deltaTrace[i]

        f = [[ants[i].fitness(), i] for i in range(len(ants))]
        bestAntIndex = max(f, key=lambda el: el[0])[1]
        return ants[bestAntIndex]

    def runACO(self):
        # set intensity and quantity of pheromone of every path between the sensors to 0 at time 0
        # self.__pheromoneTrails[sensor1,sensor2] = [intensity]  deltaTrace = quantity = 0
        for path_key in self.__sensorsPaths.keys():
            self.__pheromoneTrails[path_key] = 1   # trace ?
        # print(self.__pheromoneTrails)

        best_ant = Ant([Sensor()],{},0)
        for i in range(self.__noEpoch):
            solution = self.epoch()
            if solution.fitness() > best_ant.fitness():
                best_ant = solution
        print("Left energy:", best_ant.droneEnergy)
        return best_ant.getPath()  # get the best path

    def getSensorsPositions(self):
        return self.__sensorsPos

    def getDroneEnergy(self):
        return self.__droneEnergy

    def calcSensorsSquaresPerEnergy(self):
        for s in self.__sensors[1:]:
            s.computeSquaresPerEnergy(self.__mapM)

    def calculateMinDistanceBetweenSensors(self):
        for s1 in self.__sensors:
            for s2 in self.__sensors:
                posS1 = s1.getPosition()
                posS2 = s2.getPosition()
                if (s1,s2) not in self.__sensorsPaths.keys():
                    self.__sensorsPaths[(s1,s2)] = self.searchAStar(posS1[0],posS1[1],posS2[0],posS2[1])

    def getMinDistanceSensorsPaths(self):
        return self.__sensorsPaths

    # returns a list of moves as a list of pairs [x,y]
    def searchAStar(self, initialX, initialY, finalX, finalY):
        frontier = []  # priority queue
        heapq.heappush(frontier, (0, (initialX, initialY)))
        came_from = dict()
        cost_so_far = dict()  # g(n) <-> g score
        came_from[(initialX,initialY)] = None
        cost_so_far[(initialX,initialY)] = 0

        while len(frontier):
            current = heapq.heappop(frontier)[1]

            if current == (finalX, finalY):
                return reconstructPath((initialX, initialY), (finalX, finalY), came_from)

            for neighbor in get_neighbors(current):
                new_cost = cost_so_far[current] + 1   # graph.cost(current, neighbor) = 1
                if (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]) and \
                        self.__mapM.checkValidMapPosition(neighbor[0], neighbor[1]):
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic_distance(neighbor, (finalX, finalY))  # h(n)
                    heapq.heappush(frontier, (priority, neighbor))
                    came_from[neighbor] = current
        return None

