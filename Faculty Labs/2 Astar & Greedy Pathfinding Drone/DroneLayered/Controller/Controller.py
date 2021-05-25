from random import randint
import numpy as np
import heapq


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
    def __init__(self, mapM):
        self.__visited = []
        self.__mapM = mapM

    def positionDrone(self):
        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)
        while str(self.__mapM)[x * 20 + y + x] == '1' or (x,y) in self.__visited:
            x = randint(0, 19)
            y = randint(0, 19)
        self.__visited.append((x,y))
        return x,y

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

    # returns a list of moves as a list of pairs [x,y]
    def searchGreedy(self, initialX, initialY, finalX, finalY):
        frontier = []  # priority queue
        heapq.heappush(frontier, (0, (initialX, initialY)))
        came_from = dict()
        came_from[(initialX,initialY)] = None

        while len(frontier):
            current = heapq.heappop(frontier)[1]

            if current == (finalX, finalY):
                return reconstructPath((initialX, initialY), (finalX, finalY), came_from)

            for neighbor in get_neighbors(current):
                if neighbor not in came_from and self.__mapM.checkValidMapPosition(neighbor[0], neighbor[1]):
                    priority = heuristic_distance(neighbor, (finalX, finalY))
                    heapq.heappush(frontier, (priority,neighbor))
                    came_from[neighbor] = current
        return None

    def dummysearch(self):
        self.__visited = []
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]
