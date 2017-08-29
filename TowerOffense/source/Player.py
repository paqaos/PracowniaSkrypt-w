import MinionSource
import PlayerArea
import UnitPath
import Minion
import math

class Player:
    def __init__(self, playerType, playerId):
        self.__minions__ = []
        self.__playerType = playerType
        self.__area = PlayerArea.PlayerArea(self)
        self.energy = 0
        self.__unitPath__ = UnitPath.UnitPath()
        self.gold = 0
        self.playerId = playerId
        # towers

    def upgradeSource(self):
        print "upgrade source"

    def update(self):
        for mine in self.getMines():
            mine.update()

        for min in self.__minions__:
            min.update()

        for source in self.getSources():
            source.update()

        self.__area.update()

    def getArea(self):
        return self.__area

    def getTowers(self):
        return self.__area.__towers__

    def getBeacons(self):
        return self.__area.__beacons__

    def getMines(self):
        return self.__area.__mines__

    def getMinions(self):
        return self.__minions__

    def getSources(self):
        return self.__area.__sources__

    def setPath(self, unitPath):
        self.__unitPath__ = unitPath

    def addMinion(self, strength):
        minion = Minion.Minion(self.__unitPath__.steps[0].x, self.__unitPath__.steps[0].x, self.__unitPath__, self.playerId)
        self.__minions__.append(minion)
        return minion

    def processDead(self):
        toDel = []
        for minion in self.__minions__:
            if not minion.alive():
                toDel.append(minion)

        cost = len(toDel)
        for minion in toDel:
            cost += minion.power
            self.__minions__.remove(minion)

        return cost

class CpuPlayer(Player):
    def __init__(self):
        Player.__init__(self,"CPU",2)

    def ai(self):

        if len(self.aiorder) > 0:
            curElement = self.aiorder[0]
            if self.gold > curElement.cost:
                self.gold -= curElement.cost
                self.aiorder.remove(curElement)
                curElement.upgrade()
                curElement.order *= 1.5
                print "upgrade"

                if curElement.maxLevel != curElement.level:
                    self.aiorder.append(curElement)

                self.reorderAi()

    def prepareAi(self):

        self.aiorder = []
        count = 0

        for tow in self.getTowers():
            tow.order = tow.cost * pow(2, 5 - count)
            count += 1
            self.aiorder.append(tow)

        for min in self.getSources():
            min.order = min.cost / 2.0
            self.aiorder.append(min)

        for min in self.getMines():
            min.order = min.cost
            self.aiorder.append(min)
        
        self.reorderAi()

    def reorderAi(self):
        self.aiorder = sorted(self.aiorder, key=lambda element: element.order)
        
        curElement = self.aiorder[0]
        print curElement.cost

class HumanPlayer(Player):
    def __init__(self):
        Player.__init__(self,"Human",1)

    def upgradeSource(self):
        print "human"