from random import random
import pickle
import pygame
import numpy as np

BLUE = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3


class Map:
    def __init__(self):
        self.n = 20
        self.m = 20
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

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while (xf >= 0) and (self.surface[xf][y] == 0):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while (xf < self.n) and (self.surface[xf][y] == 0):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while (yf < self.m) and (self.surface[x][yf] == 0):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while (yf >= 0) and (self.surface[x][yf] == 0):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def checkValidMapPosition(self, x, y):
        if x is None or y is None:
            return False
        return 0 <= x< self.n and 0 <= y < self.m and self.surface[x][y] != 1

    def markVisited(self, x, y):
        if self.checkValidMapPosition(x,y):
            self.surface[x][y] = 2

    def image(self, x=None, y=None, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        visited = pygame.Surface((20, 20))
        visited.fill(GREEN)
        brick.fill(colour)
        imagine.fill(background)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.surface[i][j] == 2:
                    imagine.blit(visited, (j * 20, i * 20))

        if self.checkValidMapPosition(x,y):
            drona = pygame.image.load("View/drona.png")
            imagine.blit(drona, (y * 20, x * 20))
        return imagine
