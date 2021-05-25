import copy
from random import randint


class DFSController:
    def __init__(self, drone, detectedMap):
        self.__drone = drone
        self.__dMap = detectedMap
        self.__visited = []
        self.__prev = {}
        self.__stack = []
        self.__can_dig = True
        self.__deepest = None
        self.start = True

    def positionDrone(self,environment):
        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)
        while str(environment)[x * 20 + y + x] == '1':  # we cannot position the drone on a wall
            x = randint(0, 19)
            y = randint(0, 19)
        self.__drone.setPosition(x,y)
        self.__visited.append((x,y))
        self.__stack.append((x,y))
        return x,y

    def getDrone(self):
        return self.__drone

    def getDetectedMap(self):
        return self.__dMap

    def moveDFS(self, env):
        if len(self.__stack):

            if self.__can_dig:
                c = self.__stack.pop()
                self.__drone.setPosition(c[0],c[1])
                self.__dMap.markDetectedWalls(env, c[0], c[1])
                neighbors = get_neighbors(c)
                self.__can_dig = False

                for n in neighbors:
                    if (n not in self.__visited) and (0 <= n[0] <= 19) and (0 <= n[1] <= 19) \
                                               and (self.__dMap.surface[n[0]][n[1]] == 0):
                        self.__stack.append(n)
                        self.__visited.append(n)
                        self.__prev[n] = copy.deepcopy(c)
                        self.__can_dig = True

                if not self.__can_dig:
                    self.__deepest = copy.deepcopy(c)

            else:
                # check if the top of the stack is a neighbor of the current deepest position reached by DFS
                # if it's not, we trace back until it is, because the drone cannot teleport :)
                if self.__stack[-1] not in get_neighbors(self.__deepest):
                    parent = self.__prev[self.__deepest]
                    self.__drone.setPosition(parent[0],parent[1])
                    self.__dMap.markDetectedWalls(env, parent[0],parent[1])
                    self.__deepest = parent
                else:
                    self.__can_dig = True
        else:
            self.__drone.setPosition(None,None)


def get_neighbors(c):
    return [(c[0] - 1, c[1]), (c[0] + 1, c[1]), (c[0], c[1] - 1), (c[0], c[1] + 1)]