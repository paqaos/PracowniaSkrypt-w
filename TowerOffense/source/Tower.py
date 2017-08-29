# Tower.py

import pygame
import pygame.sprite
import math
import os
import pygame.image

class Tower(pygame.sprite.Sprite):
    """Basic tower"""

    def __init__(self, vector,x,y,player):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('..\\resources\\tower.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.x = x
        self.y = y
        self.level = 1
        self.type = 1
        self.player = player
        self.maxLevel = 5
        self.cost = 10
        self.areaRange = 2
        self.order = 0

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)

    def upgrade(self):
        self.level += 1
        self.areaRange *= 1.1
        self.cost = (self.cost + 2 * self.level * self.cost) / (self.level)

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