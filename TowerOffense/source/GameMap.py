import pygame
import pygame.sprite
import pygame.draw
import math
import os
import pygame.image
import Player
import Camera

class GameMap:
    def __init__(self,camera):
        self.size = 16
        self.towers = []
        self.path  = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(1,7),(2,7),(3,7),
                      (3,6),(3,5),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(8,5),(9,5),(10,5),(11,5),
                      (11,6),(11,7),(11,8),(10,8),(9,8),(8,8),(7,8),(6,8),(6,9),(6,10),
                      (7,10),(8,10), (8,11),(8,12),(8,13),(9,13),(10,13),(11,13),(11,12),(11,11),
                      (12,11),(13,11),(14,11),(15,11),(15,12),(15,13),(15,14),(15,15)]
        self.__camera__ = camera

        self.grass = load_png('..\\resources\\grass.png')
        self.water = load_png('..\\resources\\water.png')
        self.road = load_png('..\\resources\\road.png')
        self.towerA = load_png('..\\resources\\towerBlack.png')
        self.towerB = load_png('..\\resources\\towerWhite.png')
        self.beaconA = load_png('..\\resources\\beaconBlack.png')
        self.beaconB = load_png('..\\resources\\beaconWhite.png')
        self.mineA = load_png('..\\resources\\mineBlack.png')
        self.mineB = load_png('..\\resources\\mineWhite.png')
        self.minionSourceA = load_png('..\\resources\\minionSourceBlack.png')
        self.minionSourceB = load_png('..\\resources\\minionSourceWhite.png')
        self.selected = load_png('..\\resources\\selected.png')
        self.minionWhite = load_png('..\\resources\\minionWhite.png')
        self.minionBlack = load_png('..\\resources\\minionBlack.png')
        self.selectedItem = None
        self.canBuild = False

    def setPlayers(self, playerA, playerB):
        self.playerA = playerA
        self.playerB = playerB

    def drawUnitPath(self,screen):

        lastPos = ((self.unitPath.steps[0].x - self.__camera__.selectedVert) *64, (self.unitPath.steps[0].y - self.__camera__.selectedHor) *64)

        for step in self.unitPath.steps:
            pos = ((step.x - self.__camera__.selectedVert) * 64, (step.y - self.__camera__.selectedHor) * 64)

            pygame.draw.line(screen, (40,40,40), lastPos, pos, 1 )
            lastPos = pos


    def draw(self,screen):
        self.drawPath(screen)

        if self.selectedItem != None and hasattr(self.selectedItem, "areaRange"):
            pygame.draw.circle(screen, (60,60,60),
                               ((self.selectedItem.x - self.__camera__.selectedVert) * 64 + 32, (self.selectedItem.y - self.__camera__.selectedHor) * 64 + 32)
                               , int(self.selectedItem.areaRange * 64),3)


        self.drawTowers(screen)
        self.drawBeacons(screen)
        self.drawMines(screen)
        self.drawMinionSources(screen)

        self.drawUnitPath(screen)
        self.drawMinions(screen)
        self.drawSelected(screen)

    def drawMinions(self,screen):
        for minion in self.playerA.getMinions():
            screen.blit(self.minionBlack[0], ((minion.x - self.__camera__.selectedVert) * 64 - 32, (minion.y - self.__camera__.selectedHor) * 64 - 32))

            textContent = str(minion.hitpoints) + " / " + str(minion.totalHitpoints)
            text = self.font.render(textContent, 1, (0,0,0))
            screen.blit(text, ((minion.x - self.__camera__.selectedVert) * 64 - 16, (minion.y - self.__camera__.selectedHor) * 64 - 48))

        for minion in self.playerB.getMinions():
            screen.blit(self.minionWhite[0], ((minion.x - self.__camera__.selectedVert) * 64 - 32, (minion.y - self.__camera__.selectedHor) * 64 - 32))

            textContent = str(minion.hitpoints) + " / " + str(minion.totalHitpoints)
            text = self.font.render(textContent, 1, (250, 250, 250))
            screen.blit(text, ( (minion.x - self.__camera__.selectedVert) * 64 - 16, (minion.y - self.__camera__.selectedHor) * 64 - 48))

    def drawSelected(self,screen):
        screen.blit(self.selected[0], ((self.__camera__.vertical - self.__camera__.selectedVert) *64, (self.__camera__.horizontal - self.__camera__.selectedHor) * 64))

    def drawTowers(self, screen):
        for tow in self.playerA.getTowers():
            screen.blit(self.towerA[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

        for tow in self.playerB.getTowers():
            screen.blit(self.towerB[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

    def drawMinionSources(self, screen):
        for tow in self.playerA.getSources():
            screen.blit(self.minionSourceA[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

        for tow in self.playerB.getSources():
            screen.blit(self.minionSourceB[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))


    def drawMines(self, screen):
        for tow in self.playerA.getMines():
            screen.blit(self.mineA[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

        for tow in self.playerB.getMines():
            screen.blit(self.mineB[0], ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))


    def drawBeacons(self,screen):
        for tow in self.playerA.getBeacons():
            screen.blit(self.beaconA[0],
                        ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

        for tow in self.playerB.getBeacons():
            screen.blit(self.beaconB[0],
                        ((tow.x - self.__camera__.selectedVert) * 64, (tow.y - self.__camera__.selectedHor) * 64))

    def drawPath(self, screen):
        for y in range(0,16):
            for x in range(0,16):
                screen.blit(self.getTexture(x,y), ((x - self.__camera__.selectedVert) * 64, (y - self.__camera__.selectedHor) * 64))

    def getTexture(self,x,y):
        for element in self.path:
            if element[0] == y and element[1] == x:
                return self.road[0]
        if x == (15 - y):
            return self.water[0]
        return self.grass[0]

    def setFont(self,font):
        self.font = font

    def setPath(self,unitpath):
        self.unitPath = unitpath

    def setSelected(self):
        tmpSelect = self.__findSelected__()
        self.selectedItem = tmpSelect
        self.selX = self.__camera__.vertical
        self.selY = self.__camera__.horizontal

        onPath = False
        for tow in self.path:
            if tow[1] == self.selX and tow[0] == self.selY:
                onPath = True

        self.canBuild = self.selX != 15 - self.selY and self.selectedItem == None and not onPath

    def buildTower(self):
        self.playerA.getArea().addTower(self.selX, self.selY, 1)
        tmpSelect = self.__findSelected__()
        self.selectedItem = tmpSelect
        self.canBuild = False

    def __findSelected__(self):
        for tow in self.playerA.getTowers():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerB.getTowers():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerA.getBeacons():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerB.getBeacons():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerA.getMines():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerB.getMines():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerA.getSources():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow

        for tow in self.playerB.getSources():
            if tow.x == self.__camera__.vertical and tow.y == self.__camera__.horizontal:
                return tow


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()