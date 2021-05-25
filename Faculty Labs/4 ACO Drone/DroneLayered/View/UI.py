import time
import pygame

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

        # 1. Determine for each sensor the number of squares that can be seen for each value from 0 to 5
        self.__controller.calcSensorsSquaresPerEnergy()

        # 2. Determine the minimum distance between each pair of sensors
        self.__controller.calculateMinDistanceBetweenSensors()

        # 3. Determine using ACO the shortest path between the sensors
        # 4. Determine the quantity of energy that is left at each sensor
        print("\nACO is now running, please wait...")
        ACO_sensors_path = self.__controller.runACO()
        self.logDronePath(ACO_sensors_path)

        path = []
        for i in range(len(ACO_sensors_path)-1):
            chosenSensors = ACO_sensors_path[i], ACO_sensors_path[i+1]
            path.extend(self.__controller.getMinDistanceSensorsPaths()[chosenSensors])

        # create a surface on screen that has the size of 400 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)
        screen.blit(self.__env.image(), (0, 0))
        running = True   # define a variable to control the main loop

        if path is None or len(path) == 0:
            print("No possible path was found between the above start and finish points.")
            running = False

        i = 0
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
            if len(path) > 0:
                i+=1
                droneCurrentPosition = path.pop(0)
                # print(i,droneCurrentPosition)
            else:
                droneCurrentPosition = None

            if droneCurrentPosition is not None:
                self.__drone.setPosition(droneCurrentPosition[0], droneCurrentPosition[1])
                screen.blit(self.__env.image(droneCurrentPosition[0], droneCurrentPosition[1]), (0, 0))
                pygame.display.flip()
                time.sleep(0.1)
                self.__env.markVisited(droneCurrentPosition[0], droneCurrentPosition[1])

        # time.sleep(11)
        pygame.quit()

    def logDronePath(self, sensorsPath):
        energy = self.__controller.getDroneEnergy()
        print("Drone started with energy: ", energy)

        for i in range(1, len(sensorsPath)):
            chosenSensors = sensorsPath[i-1], sensorsPath[i]
            pathLen = len(self.__controller.getMinDistanceSensorsPaths()[chosenSensors])
            energy -= pathLen - 1
            print("Path of length",pathLen,"was traversed")
            sEnergy = sensorsPath[i].goodEnergy
            self.__env.saveSensorDetection(sensorsPath[i].getPosition(),sEnergy)
            energy -= sEnergy
            print(sensorsPath[i], "was reached and charged with:", sEnergy, "units of energy")

        # print("Drone ended with energy: ", energy)
        print("No. of sensors reached:", len(sensorsPath)-1)
