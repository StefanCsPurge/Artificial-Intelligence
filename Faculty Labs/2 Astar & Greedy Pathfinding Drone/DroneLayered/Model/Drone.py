import pygame


class Drone:
    def __init__(self):
        self.__x = None
        self.__y = None

    def getPosition(self):
        return self.__x, self.__y

    def setPosition(self,newX,newY):
        self.__x = newX
        self.__y = newY

    '''
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1
    '''

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("../View/drona.png")
        mapImage.blit(drona, (self.__y * 20, self.__x * 20))

        return mapImage
