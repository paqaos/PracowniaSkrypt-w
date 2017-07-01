import Tower
import Beacon
import Mine
import MinionSource

class PlayerArea:
    """Player's area"""

    def __init__(self, player):
        self.__beacons__ = []
        self.__towers__ = []
        self.__mines__ = []
        self.__sources__ = []
        self.__player = player

    def addTower(self,x,y,player):
        self.__towers__.append(Tower.Tower((0,0),x,y,player))

    def addBeacon(self,x,y,player):
        self.__beacons__.append(Beacon.Beacon(x,y,player))

    def addMine(self,x,y, player):
        self.__mines__.append(Mine.Mine(x,y,player,self.__player))

    def addSource(self,x,y, player):
        self.__sources__.append(MinionSource.MinionSource(x,y, player, self.__player))

    def update(self):
        pass

    def getBase(self):
        pass