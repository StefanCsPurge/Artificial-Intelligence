# -*- coding: utf-8 -*-

# imports
from gui import *
from controller import *
from repository import *
# from domain import *
import matplotlib.pyplot as plt
import threading
import random

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d. visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATTENTION! the function doesn't check if the path passes trough walls


def window_worker(repo_map):
    guiScreen = initPyGame((400, 400))
    guiScreen.blit(image(repo_map), (0, 0))
    pygame.display.flip()
    closePyGame()


class Console:
    def __init__(self, ctrl):
        self.__controller = ctrl
        self.__guiScreen = None
        self.__menuText = "\n1. map options: \n" \
            "\ta. create random map\n" \
            "\tb. load a map\n" \
            "\tc. save a map\n" \
            "\td. visualise map\n" \
            "2. EA options:\n" \
            "\ta. parameters setup\n" \
            "\tb. run the solver\n" \
            "\tc. visualise the statistics\n" \
            "\td. view the drone moving on a path\n" \
            "3. Validate algorithm (30 runs)\n" \
            "(use example: 1a , 2b , etc / 0 to exit)"
        self.__startCell = None
        self.__populationSize = None
        self.__m = None
        self.__noOfIterations = None
        self.__currentGeneration = None
        self.__avgFitnesses = None
        self.__times = None

    def run(self):
        running = True

        while running:
            print(self.__menuText)
            try:
                option = input().strip()
                if option == "0":
                    running = False
                    continue
                elif option == "1a":
                    self.__controller.makeRandomMap()
                    if self.__startCell is not None:
                        self.__startCell = self.__controller.getDroneStartPosition()
                elif option == "1b":
                    self.__controller.loadMap()
                    if self.__startCell is not None:
                        self.__startCell = self.__controller.getDroneStartPosition()
                elif option == "1c":
                    self.__controller.saveMap()
                elif option == "1d":
                    # print(self.__controller.getRepoMap())
                    setGuiRunning(False)
                    print("Launching window...")
                    time.sleep(1)
                    t = threading.Thread(target=window_worker,
                                         args=(self.__controller.getRepoMap(),))
                    t.start()
                    continue
                elif option == "2a":
                    self.__startCell = self.__controller.getDroneStartPosition()
                    print("Drone start position is: " + str(self.__startCell))
                    self.__m = int(input("No. of steps until the battery depletes: "))  # individual/path size
                    self.__populationSize = int(input("Population size: "))
                    self.__noOfIterations = int(input("Number of population iterations: "))
                elif option == "2b":
                    if self.__startCell is None or self.__m is None or self.__populationSize is None \
                            or self.__noOfIterations is None:
                        raise Exception("Set the parameters first!")
                    self.__currentGeneration, self.__avgFitnesses, self.__times = self.__controller.solver(
                                                                                            self.__m,
                                                                                            self.__populationSize,
                                                                                            self.__startCell,
                                                                                            self.__noOfIterations)

                elif option == "2c":
                    if self.__currentGeneration is None:
                        raise Exception("Run the solver first!")
                    plt.plot(self.__times, self.__avgFitnesses)
                    plt.ylabel('average iteration fitness')
                    plt.xlabel('time (s)')
                    plt.draw()  # draw the plot
                    plt.pause(99)  # show it for 99 seconds
                    continue

                elif option == "2d":
                    if self.__currentGeneration is None:
                        raise Exception("Run the solver first!")
                    selectedIndividual = self.__currentGeneration[0]
                    print("Best fitness score:", selectedIndividual.get_fitness())
                    theMap = self.__controller.getRepoMap()
                    path = selectedIndividual.getPath(self.__startCell, theMap)
                    setGuiRunning(False)
                    print("Launching window...")
                    time.sleep(1)
                    print("Check out the moving drone!")
                    movingDrone(theMap, path)
                    # continue
                elif option == "3":  # algorithm validation
                    if self.__startCell is None or self.__m is None or self.__populationSize is None \
                            or self.__noOfIterations is None:
                        raise Exception("Set the parameters first!")

                    f = []
                    for i in range(30):
                        print("Run",i+1)
                        random.seed(i+1)
                        self.__currentGeneration, self.__avgFitnesses, self.__times = self.__controller.solver(
                                                                                            self.__m,
                                                                                            self.__populationSize,
                                                                                            self.__startCell,
                                                                                            self.__noOfIterations)
                        solution = self.__currentGeneration[0]
                        f.append(solution.get_fitness())
                    print("30 test runs done")
                    print("Solution fitness average:", np.average(f))
                    print("Solution standard deviation:", np.std(f))

                else:
                    raise Exception("Non-existent option!")
            except Exception as ex:
                print("Error: " + str(ex))
            else:
                print("Done. ")
                input("Press Enter to continue...")


if __name__ == "__main__":
    repo = Repository()
    controller = Controller(repo)
    console = Console(controller)
    console.run()
