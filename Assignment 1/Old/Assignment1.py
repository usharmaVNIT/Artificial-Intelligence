from _typeshed import Self


class State:
    def __init__(self , arraignment = None , currentCoords = None , parent = None , cost = 0):
        self.arraignment = arraignment
        self.parent = parent
        self.currentCoords = currentCoords
        self.cost = cost



    def setArraignment(self , arraignment):
        self.arraignment = arraignment

    def getArraignment(self):
        return self.arraignment


    def getArraignmentString(self):
        # to make it as string
        elements = ','.join([','.join(rows) for rows in self.arraignment])
        arraignment = '[' + elements + ']'
        return arraignment

    def GlobalActions(self):
        left = [0,-1]
        right = [0,1]
        up = [-1,0]
        down = [1,0]
        return [left , right , up , down]

    def isSafeAction(self , action , emptyCoords):
        coords = emptyCoords[0]+action[0] , emptyCoords[1]+action[1]
        return 0<=coords[0]<=len(self.arraignment) and 0<=coords[1]<=len(self.arraignment[0])

    def getSuccessors(self):
        successors = []
        for action in self.GlobalActions():
            if self.isSafeAction(action , self.currentCoords):
                intermediate = self.getArraignment()[:]
                coords = self.currentCoords[0]+action[0] , self.currentCoords[1]+action[1]

                intermediate[coords[0]][coords[1]] , intermediate[self.currentCoords[0]][self.currentCoords[1]] = intermediate[self.currentCoords[0]][self.currentCoords[1]] , intermediate[coords[0]][coords[1]]
                successor = State(intermediate , coords , self , self.cost+1)

                successors.append(successor)
        return successors

    







