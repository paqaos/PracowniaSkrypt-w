class UnitPath:
    def __init__(self):
        self.steps = []

    def addStep(self,x,y):
        step = UnitPathStep(x,y)
        self.steps.append(step)

class UnitPathStep:
    def __init__(self,x,y):
        self.x = x
        self.y = y