import pygame
import time

BLUE = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class UI:
    def __init__(self, controller, environment):
        self.__controller = controller
        self.__env = environment

        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("View/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Drone exploration")

        # create a surface on screen that has the size of 800 x 480
        self.__screen = pygame.display.set_mode((800, 400))
        self.__screen.fill(WHITE)
        self.__screen.blit(self.__env.image(), (0, 0))

    def run(self):
        # define a variable to control the main loop
        running = True
        print(str(self.__env))
        dronePosition = self.__controller.positionDrone(self.__env)

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
            if dronePosition != (None,None):
                detectedMap = self.__controller.getDetectedMap()
                self.__screen.blit(detectedMap.image(dronePosition[0], dronePosition[1]), (400, 0))
                pygame.display.flip()
                time.sleep(0.03)

                self.__controller.moveDFS(self.__env)

                dronePosition = self.__controller.getDrone().getPosition()

        # time.sleep(11)
        pygame.quit()
