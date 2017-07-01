#!/usr/bin/python
import pygame
import Minion

class MinionSource:
    """Minion generator"""

    def __init__(self, x,y,player, playerRef):
        self.player = player
        self.level = 1
        self.x = x
        self.y = y
        self.type = 4
        self.playerRef = playerRef
        self.globalDelta = 0
        self.getTicksLastFrame = 0
        self.cost = 250
        self.maxLevel = 3

    def showUpgrade(self):
        raise NotImplemented

    def upgrade(self):
        self.level += 1
        self.cost = (self.cost + 2 * self.level * self.cost) / (self.level)

    def update(self):
        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t

        self.globalDelta += deltaTime

        if self.globalDelta > 5.0:
            self.generateMinions()
            self.globalDelta = 0.0

    def generateMinions(self):
        minion = self.playerRef.addMinion(1.0)
        minion.totalHitpoints = 3 + self.level * 2
        minion.hitpoints = 3 + self.level * 2
        minion.power = 1 + self.level