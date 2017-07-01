class Camera:


    def __init__(self):
        self.vertical = 0
        self.horizontal = 0
        self.selectedVert = 0
        self.selectedHor = 0

    def movePosition(self, vertical, horizontal):
        self.vertical += vertical
        self.horizontal += horizontal

    def moveSelected(self, vertical, horizontal):
        self.selectedVert += vertical
        self.selectedHor += horizontal
