import Player
class Mine:
    def __init__(self, player):
        self.__player__ = player
        self.income = 0.05
        self.__level = 1
        self.__cost = 1000

    def update(self):
        self.__player__.energy += self.income
        print self.__player__.energy

    def upgrade(self):
        if(self.__player__.energy >= self.__cost):
            self.__player__.energy -= self.__cost
            self.__level += 1
            self.income *= 2
            self.__cost = self.__cost*4
            print "update"
        else:
            print "not update"