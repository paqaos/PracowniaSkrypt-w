import Player
class Mine:
    def __init__(self, x,y, player, playerRef):
        self.x = x
        self.y = y
        self.player = player
        self.income = 0.05
        self.level = 1
        self.cost = 400
        self.maxLevel = 4
        self.type = 3
        self.playerRef = playerRef
        self.order = 0

    def update(self):
        self.playerRef.gold += (self.income * self.playerRef.goldMultiplier)

    def upgrade(self):
        self.income *= 2
        self.cost = self.cost ( 1 + 1.5 * self.level) / (self.level)
        self.level += 1