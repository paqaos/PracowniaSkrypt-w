import Player
import pygame
from pygame.locals import *
import Camera
import GameMap
import UnitPath

class GameManager:
    """Game manager"""

    def __init__(self):

        self.path = self.preparePaths()
        self.__cpuPlayer__ = Player.CpuPlayer()
        self.__humanPlayer__ = Player.HumanPlayer()
        self.__players__ = [self.__humanPlayer__, self.__cpuPlayer__]
        self.__camera__ = Camera.Camera()
        self.__gamemap__ = GameMap.GameMap(self.__camera__)


        # human
        self.__humanPlayer__.getArea().addTower(2,1,1)
        self.__humanPlayer__.getArea().addTower(6,2,1)
        self.__humanPlayer__.getArea().addTower(5,5,1)
        self.__humanPlayer__.getArea().addTower(6,10,1)
        self.__humanPlayer__.getArea().addBeacon(4,9,1)
        # cpu
        self.__cpuPlayer__.getArea().addTower(12,14,2)
        self.__cpuPlayer__.getArea().addTower(12,10,2)
        self.__cpuPlayer__.getArea().addTower(12,7,2)
        self.__cpuPlayer__.getArea().addTower(9,8,2)
        self.__cpuPlayer__.getArea().addBeacon(9,9,2)

        self.__gamemap__.setPlayers(self.__humanPlayer__, self.__cpuPlayer__)
        self.selected = None
        self.__gamemap__.setPath(self.path)

        self.__humanPlayer__.setPath(self.path)
        self.__humanPlayer__.addMinion()

    def preparePaths(self):
        path = UnitPath.UnitPath()

        path.addStep(0.5, 0.5)
        path.addStep(7.5, 0.5)
        path.addStep(7.5, 3.5)
        path.addStep(4.5, 3.5)
        path.addStep(4.5, 8.5)
        path.addStep(5.5, 8.5)
        path.addStep(5.5, 11.5)
        path.addStep(8.5, 11.5)
        path.addStep(8.5, 6.5)
        path.addStep(10.5, 6.5)
        path.addStep(10.5, 8.5)
        path.addStep(13.5, 8.5)
        path.addStep(13.5, 11.5)
        path.addStep(11.5, 11.5)
        path.addStep(11.5, 15.5)
        path.addStep(15.5, 15.5)

        return path

    def player(self):
        return self.__humanPlayer__

    def process_input(self, event):
        if event.key == pygame.K_ESCAPE:
            return False

        if event.key == pygame.K_a:
            if self.__camera__.selectedVert > 0:
                self.__camera__.moveSelected(-1,0)

        if event.key == pygame.K_d:
            if self.__camera__.selectedVert < 4:
                self.__camera__.moveSelected(1,0)

        if event.key == pygame.K_w:
            if self.__camera__.selectedHor > 0:
                self.__camera__.moveSelected(0,-1)

        if event.key == pygame.K_s:
            if self.__camera__.selectedHor < 7:
                self.__camera__.moveSelected(0,1)

        if event.key == pygame.K_DOWN:
            if self.__camera__.horizontal < 15:
                self.__camera__.movePosition(0,1)

        if event.key == pygame.K_UP:
            if self.__camera__.horizontal > 0:
                self.__camera__.movePosition(0, -1)

        if event.key == pygame.K_RIGHT:
            if self.__camera__.vertical < 15:
                self.__camera__.movePosition(1,0)

        if event.key == pygame.K_LEFT:
            if self.__camera__.vertical > 0:
                self.__camera__.movePosition(-1, 0)

        if event.key == pygame.K_RETURN:
            self.__gamemap__.setSelected()
            self.selected = self.__gamemap__.selectedItem

        if event.key == pygame.K_u and self.selected != None:
            if hasattr(self.selected, "upgrade") and self.selected.player == 1:
                self.selected.upgrade()

        return True

    def update(self):
        self.__humanPlayer__.update()
        self.__cpuPlayer__.update()

    def render(self,screen):
        self.__gamemap__.draw(screen)
        screen.blit(self.surface, (0, 576))

        if self.selected != None:
            playerColor = None

            if self.selected.player == 1:
                playerColor = (10, 10, 10)
            else:
                playerColor = (240,240,240)

            if self.selected.type == 1:
                text = self.font.render("Wieza", 1, playerColor)
                screen.blit(text, (0,581))

            if self.selected.type == 2:
                text = self.font.render("Beacon", 1, playerColor)
                screen.blit(text, (0, 581))

            text = self.font.render(str(self.selected.level), 1, playerColor)
            screen.blit(text, (100,581))

    def setFont(self,font):
        self.__gamemap__.setFont(font)
        self.font = font

    def setGuiSurface(self,surface):
        self.surface = surface