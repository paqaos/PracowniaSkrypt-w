#!/usr/bin/python
import UnitType

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class Minion:
    """Basic enemy"""
    def __init__(self, x,y, path, player):
        self.totalHitpoints = 1
        self.hitpoints = 1
        self.power = 0
        self.x = x
        self.y = y
        self.path = path
        self.step = 1
        self.active = 1
        self.max = len(self.path.steps)
        self.stepLength = 0.02
        self.player = player
        pass

    def interact(self):
        pass

    def update(self):
        if self.active == 0:
            return

        target = self.path.steps[self.step]

        if self.x > target.x :
            self.x -= self.stepLength
        elif self.x < target.x:
            self.x += self.stepLength

        if self.y > target.y :
            self.y -= self.stepLength
        elif self.y < target.y:
            self.y += self.stepLength

        if isclose(self.x,target.x) and isclose(self.y, target.y):
            self.step += 1
            if self.step == self.max :
                self.active = 0
