import Player
import pygame
from pygame.locals import *
from random import randint

import Camera
import GameMap
import UnitPath

class GameManager:
    """Game manager"""

    def __init__(self):
        self.isSelected = 0
        self.path = self.preparePaths()
        self.__cpuPlayer__ = Player.CpuPlayer()
        self.__humanPlayer__ = Player.HumanPlayer()
        self.__players__ = [self.__humanPlayer__, self.__cpuPlayer__]
        self.__camera__ = Camera.Camera()
        self.__gamemap__ = GameMap.GameMap(self.__camera__)
        self.difficulty = 0


        # human
        self.__humanPlayer__.getArea().addTower(2,1,1)
        self.__humanPlayer__.getArea().addTower(6,2,1)
        self.__humanPlayer__.getArea().addTower(5,5,1)
        self.__humanPlayer__.getArea().addTower(6,10,1)
        self.__humanPlayer__.getArea().addBeacon(4,9,1)
        self.__humanPlayer__.getArea().addMine(2,3,1)
        self.__humanPlayer__.getArea().addSource(1,3,1)

        # cpu
        self.__cpuPlayer__.getArea().addTower(12,14,2)
        self.__cpuPlayer__.getArea().addTower(12,10,2)
        self.__cpuPlayer__.getArea().addTower(12,7,2)
        self.__cpuPlayer__.getArea().addTower(9,8,2)
        self.__cpuPlayer__.getArea().addBeacon(9,9,2)
        self.__cpuPlayer__.getArea().addSource(13,13,2)
        self.__cpuPlayer__.getArea().addMine(12,5,2)

        self.__cpuPlayer__.prepareAi()

        self.__gamemap__.setPlayers(self.__humanPlayer__, self.__cpuPlayer__)
        self.selected = None
        self.__gamemap__.setPath(self.path)

        self.__humanPlayer__.setPath(self.path)

        revPathtmp = reversed(self.path.steps)

        revPath = UnitPath.UnitPath()
        for step in revPathtmp:
            revPath.addStep(step.x, step.y)

        self.__cpuPlayer__.setPath(revPath)
        self.newTowerCost = (len(self.__humanPlayer__.getTowers()) + 1 ) * 20

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

        if event.key == pygame.K_i and self.difficulty < 5:
            print 'dodano AI+1'
            self.difficulty += 1
        
        if event.key == pygame.K_k and self.difficulty > 0:
            print 'usunieto AI-1'
            self.difficulty -= 1

        if event.key == pygame.K_RETURN:
            self.__gamemap__.setSelected()
            self.selected = self.__gamemap__.selectedItem

        if event.key == pygame.K_b and self.selected == None:
            if self.newTowerCost <= self.__humanPlayer__.gold:
                self.__humanPlayer__.gold -= self.newTowerCost
                self.__gamemap__.buildTower()
                self.newTowerCost = (len(self.__humanPlayer__.getTowers()) + 1 ) * 20

        if event.key == pygame.K_u and self.selected != None:
            if hasattr(self.selected, "upgrade") and self.selected.player == 1 and self.selected.level < self.selected.maxLevel:
                if self.selected.cost <= self.__humanPlayer__.gold:
                    self.__humanPlayer__.gold -= self.selected.cost
                    self.selected.upgrade()

        return True

    def process_ai(self):
        self.__cpuPlayer__.ai()

    def update(self):
        self.__humanPlayer__.update()
        self.__cpuPlayer__.update()
        self.process_ai()
        self.__cpuPlayer__.setDifficulty(self.difficulty)

        minions = self.__cpuPlayer__.getMinions() + self.__humanPlayer__.getMinions()
        towers = self.__cpuPlayer__.getTowers() + self.__humanPlayer__.getTowers()
        beacons = self.__cpuPlayer__.getBeacons() + self.__humanPlayer__.getBeacons()

        minionsCount = len(minions)
        towersCount = len(towers)
        beaconsCount = len(beacons)

        for i in range(minionsCount):
            minions[i].bonusPower = 0
            minions[i].bonusDefense = 0

        for i in range(towersCount):
            for j in range(minionsCount):
                self.rangeTower(towers[i], minions[j])

        for i in range(beaconsCount):
            for j in range(minionsCount):
                self.rangeBeacon(beacons[i], minions[j])

        for i in range(minionsCount):
            for j in range(i):
                self.checkCollision(minions[i], minions[j])

        deadHuman = self.__humanPlayer__.processDead()
        deadCpu = self.__cpuPlayer__.processDead()

        self.__humanPlayer__.gold += deadCpu
        self.__cpuPlayer__.gold += deadHuman

        # next minions

        minions = self.__cpuPlayer__.getMinions() + self.__humanPlayer__.getMinions()

        for minion in minions:
            if minion.win == 1:
                return minion.player

    def rangeTower(self, tower, minion):
        distance = pow(pow(minion.x - tower.x, 2.0) + pow(minion.y - tower.y, 2.0), 0.5)

        if distance < tower.areaRange and minion.player == tower.player:
            minion.bonusPower += tower.level

    def rangeBeacon(self, beacon, minion):
        distance = pow(pow(minion.x - beacon.x, 2.0) + pow(minion.y - beacon.y, 2.0), 0.5)

        if distance < beacon.areaRange and minion.player == beacon.player:
            minion.bonusDefense += beacon.level

    def checkCollision(self, minionA, minionB):
        if abs(minionA.x - minionB.x) + abs(minionA.y - minionB.y) > 0.8:
            return

        sameTeam = minionA.player == minionB.player

        if sameTeam:
            if minionA.step > minionB.step or (minionA.step == minionB.step and minionA.stepId > minionB.stepId):
                minionB.active = 0
        else:
            bonusA = randint(0,int(minionA.powerrange)+1)
            bonusB = randint(0,int(minionB.powerrange)+1)
            atkB = ((minionB.power + minionB.bonusPower + bonusB) - minionA.bonusDefense)
            atkA = ((minionA.power + minionA.bonusPower + bonusA) - minionB.bonusDefense)
            if atkB > 0:
                minionA.hitpoints -= atkB
            if atkA > 0:
                minionB.hitpoints -= atkA

            if minionA.alive(): # enemy is alive so i have to fight
                minionB.active = 0
            else: # enemy is dead, i can run now
                minionB.active = 1

            if minionB.alive():
                minionA.active = 0
            else:
                minionA.active = 1

    def render(self,screen):
        self.__gamemap__.draw(screen)
        screen.blit(self.surface, (0, 576))

        if self.selected != None:
            playerColor = None

            if self.selected.player == 1:
                playerColor = (10, 10, 10)
            else:
                playerColor = (240,240,240)

            textContent = ""
            if self.selected.type == 1:
                textContent = "Wieza"

            if self.selected.type == 2:
                textContent = "Beacon"

            if self.selected.type == 3:
                textContent = "Kopalnia"

            if self.selected.type == 4:
                textContent = "Garnizon"

            textContent += " " + str(self.selected.level)
            text = self.font.render(textContent, 1, playerColor)
            screen.blit(text, (0,581))

            if hasattr(self.selected, "cost") and self.selected.player == 1:
                text = self.font.render("koszt [u] " + str(self.selected.cost), 1, playerColor)
                screen.blit(text, (0,610))

        text = self.font.render("gold: " + str(self.__humanPlayer__.gold), 1, (10, 10, 10))
        screen.blit(text, (300, 581))

        content = "buduj wieze " 
        if self.__gamemap__.canBuild:
            content += "[b] "
        content += str(self.newTowerCost)
        text = self.font.render(content,1,(10, 10, 10))
        screen.blit(text, (300,610))

    def setFont(self,font):
        self.__gamemap__.setFont(font)
        self.font = font

    def setGuiSurface(self,surface):
        self.surface = surface