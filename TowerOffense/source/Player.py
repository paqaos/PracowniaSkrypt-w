import MinionSource
import PlayerArea
import UnitPath
import Minion

class Player:
    def __init__(self, playerType):
        self.__minions__ = []
        self.__playerType = playerType
        self.__area = PlayerArea.PlayerArea(self)
        self.energy = 0
        self.__unitPath__ = UnitPath.UnitPath()
        self.gold = 0
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
        minion = Minion.Minion(self.__unitPath__.steps[0].x, self.__unitPath__.steps[0].x, self.__unitPath__)
        self.__minions__.append(minion)

class CpuPlayer(Player):
    def __init__(self):
        Player.__init__(self,"CPU")


class HumanPlayer(Player):
    def __init__(self):
        Player.__init__(self,"Human")

    def upgradeSource(self):
        print "human"