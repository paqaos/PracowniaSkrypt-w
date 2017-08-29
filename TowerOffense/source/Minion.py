#!/usr/bin/python

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class Minion:
    """Basic enemy"""
    def __init__(self, x,y, path, player):
        self.totalHitpoints = 1
        self.hitpoints = 1
        self.power = 1
        self.powerrange = 1
        self.bonusPower = 0
        self.bonusDefense = 0
        self.x = x
        self.y = y
        self.path = path
        self.step = 1
        self.active = 1
        self.max = len(self.path.steps)
        self.stepLength = 0.02
        self.player = player
        self.stepId = 0
        self.win = 0
        pass

    def interact(self):
        pass

    def alive(self):
        return self.hitpoints > 0

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

        self.stepId += 1
        if isclose(self.x,target.x) and isclose(self.y, target.y):
            self.step += 1
            self.stepId = 0
            if self.step == self.max :
                self.active = 0
                self.win = 1
