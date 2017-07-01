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

    def showUpgrade(self):
        raise NotImplemented

    def upgrade(self, type, option):
        cost = 2500
        if self.player.energy > cost:
            self.player.energy -= cost
            self.level += 1

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
        self.playerRef.addMinion(1.0)