#!/usr/bin/python
import pygame
import Minion

class MinionSource(pygame.sprite.Sprite):
    """Minion generator"""

    def __init__(self, player):
        self.player = player
        self.level = 1

    def showUpgrade(self):
        raise NotImplemented

    def upgrade(self, type, option):
        cost = 2500
        if self.player.energy > cost:
            self.player.energy -= cost
            self.level += 1

    def generateMinions(self):
        minion = Minion.Minion()



        return minion