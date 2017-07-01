import Tower
import Beacon

class PlayerArea:
    """Player's area"""

    def __init__(self, player):
        self.__beacons__ = []
        self.__towers__ = []

    def addTower(self,x,y,player):
        self.__towers__.append(Tower.Tower((0,0),x,y,player))

    def addBeacon(self,x,y,player):
        self.__beacons__.append(Beacon.Beacon(x,y,player))

    def update(self):
        pass

    def getBase(self):
        pass