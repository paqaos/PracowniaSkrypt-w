import Player
class Mine:
    def __init__(self, x,y, player, playerRef):
        self.x = x
        self.y = y
        self.player = player
        self.income = 0.025
        self.level = 1
        self.cost = 500
        self.maxLevel = 2
        self.type = 3
        self.playerRef = playerRef


    def update(self):
        self.playerRef.gold += self.income

    def upgrade(self):
        self.level += 1
        self.income *= 2
        self.cost = (self.cost + 2 * self.level * self.cost) / (self.level)