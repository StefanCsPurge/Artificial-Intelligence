import pygame
import time

BLUE = (0, 0, 255)
GRAYBLUE = (50, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class UI:
    def __init__(self, controller, environment, drone):
        self.__controller = controller
        self.__env = environment
        self.__drone = drone

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("View/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

    def run(self):
        # print(str(self.__env))
        droneStartPosition = (14, 0)    # self.__controller.positionDrone() # for random positioning
        droneFinishPosition = (0, 3)
        print("\nStart and finish points:", droneStartPosition, droneFinishPosition)

        choice = int(input("Choose 1 for A* or 2 for Greedy: "))
        if choice == 1:
            start_time = time.time()
            path = self.__controller.searchAStar(droneStartPosition[0], droneStartPosition[1],
                                                 droneFinishPosition[0], droneFinishPosition[1])
            print("A* pathfinding execution time:", time.time() - start_time)
        else:
            start_time = time.time()
            path = self.__controller.searchGreedy(droneStartPosition[0], droneStartPosition[1],
                                                  droneFinishPosition[0], droneFinishPosition[1])
            print("Greedy pathfinding execution time:", time.time() - start_time)

        if path is None:
            print("No possible path was found between the above start and finish points. \nDummy path was selected.")
            path = self.__controller.dummysearch()

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)
        screen.blit(self.__env.image(), (0, 0))
        running = True   # define a variable to control the main loop

        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                    '''
                if event.type == KEYDOWN:
                    d.move(m)
                    '''
            if len(path) > 0:
                droneCurrentPosition = path.pop(0)
                print(droneCurrentPosition)
            else:
                droneCurrentPosition = None

            if droneCurrentPosition is not None:
                self.__drone.setPosition(droneCurrentPosition[0], droneCurrentPosition[1])
                screen.blit(self.__env.image(droneCurrentPosition[0], droneCurrentPosition[1]), (0, 0))
                pygame.display.flip()
                time.sleep(0.3)
                self.__env.markVisited(droneCurrentPosition[0], droneCurrentPosition[1])

        # time.sleep(11)
        pygame.quit()
