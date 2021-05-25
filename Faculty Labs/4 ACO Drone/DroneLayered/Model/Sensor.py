from random import *

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3


class Sensor:
    def __init__(self, position=(0,0)):
        self.__position = position
        self.__squaresPerEnergy = [0,0,0,0,0,0]
        self.goodEnergy = 0
        self.goodArea = 0

    def getPosition(self):
        return self.__position

    def getSquaresPerEnergy(self):
        return self.__squaresPerEnergy

    def computeSquaresPerEnergy(self, theMap):
        readings = theMap.readUDMSensors(self.__position[0],self.__position[1])
        for direction in [UP,DOWN,LEFT,RIGHT]:
            if readings[direction] >= 1:  # e_1
                for i in range(1, 6):
                    self.__squaresPerEnergy[i] += 1
            if readings[direction] >= 2:  # e_2
                for i in range(2, 6):
                    self.__squaresPerEnergy[i] += 1
            if readings[direction] >= 3:  # e_3
                for i in range(3, 6):
                    self.__squaresPerEnergy[i] += 1
            if readings[direction] >= 4:  # e_4
                for i in range(4, 6):
                    self.__squaresPerEnergy[i] += 1
            if readings[direction] >= 5:  # e_5
                for i in range(5, 6):
                    self.__squaresPerEnergy[i] += 1

    def getOptimalEnergyArea(self):
        # get the lowest energy level with the max scanned territory
        maxNoScannedSquares = max(self.__squaresPerEnergy)
        for i in range(6):
            if self.__squaresPerEnergy[i] == maxNoScannedSquares:
                return i, maxNoScannedSquares

    def setGoodEnergyArea(self):
        maxIdx, maxScannedArea = self.getOptimalEnergyArea()
        self.goodEnergy = randint(1,maxIdx)
        self.goodArea = self.__squaresPerEnergy[self.goodEnergy]

    def __str__(self):
        return "Sensor at {}".format(self.__position)


