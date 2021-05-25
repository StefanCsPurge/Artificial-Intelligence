# -*- coding: utf-8 -*-

import pygame
import time
from pygame.locals import *

from domain import *

GUI_RUNNING = False


def setGuiRunning(bool_val):
    global GUI_RUNNING
    GUI_RUNNING = bool_val


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame(given_running = True):
    # closes the pygame
    # loop for events
    global GUI_RUNNING
    GUI_RUNNING = given_running
    while GUI_RUNNING:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == QUIT:
                # change the value to False, to exit the main loop
                GUI_RUNNING = False
    pygame.quit()
    

def movingDrone(currentMap, path, speed=1,  markSeen=True):
    # animation of a drone on a path
    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))

    drona = pygame.image.load("drona.png")
    visited = []

    screen.blit(image(currentMap), (0, 0))
    scannedBrick = pygame.Surface((20, 20))
    visitedBrick = pygame.Surface((20, 20))
    scannedBrick.fill(GREEN)
    visitedBrick.fill(RED)

    for i in range(len(path)):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                pass
        if markSeen:
            for j in range(i+1):
                for var in v:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + var[0] < currentMap.n and  
                            0 <= y + var[1] < currentMap.m) and 
                           currentMap.surface[x + var[0]][y + var[1]] != 1):
                        x = x + var[0]
                        y = y + var[1]
                        if (y,x) not in visited:
                            screen.blit(scannedBrick, (y * 20, x * 20))
        
        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        if i:
            screen.blit(visitedBrick, (path[i-1][1] * 20, path[i-1][0] * 20))
            visited.append((path[i-1][1],path[i-1][0]))
        pygame.display.flip()
        print(i,path[i])
        time.sleep(0.5 * speed)            
    closePyGame()


def image(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20,20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))
    pygame.display.flip()
    return imagine        
