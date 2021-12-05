
import copy


class State:
    def __init__(self , configuration , parent=None , action_taken = None ):
        self.configuration = configuration
        self.parent = parent
        self.action = action_taken
    
    def getConfiguration(self):
        return self.configuration

    def getConfigurationInString(self):
        return '[' + ','.join([ ','.join(x) for x in self.configuration]) + ']'





def getSteps(state1 , state2):
    steps = []
    state = state1
    while state.parent != None:
        steps = [state] + steps
        state = state.parent
    steps = [state] + steps

    
    actionComplement = {}
    actionComplement['left'] = 'right'
    actionComplement['right'] = 'left'
    actionComplement['up'] = 'down'
    actionComplement['down'] = 'up'

    i = 0
    while i<len(steps)-1:
        steps[i].action = steps[i+1].action
        i+=1

    opposite_Steps = []
    state = state2
    while state.parent!= None:
        state.action = actionComplement[state.action]
        opposite_Steps.append(state)
        state = state.parent
    opposite_Steps.append(state)

    intersection = State(['0'])
    
    finalSteps = steps[:-1] + [intersection] +  opposite_Steps
    for e in finalSteps:
        conf = e.getConfiguration()
        print("State : ")
        for n in conf:
            print('\t' , *n)
        print('ACTION to be taken : ' , e.action)
        print()
    return True



def isSafe(i , j , n):
    return 0<=i<n and 0<=j<n

def findCoords(state , n):
    arr = state.getConfiguration()
    for i in range(n):
        for j in range(n):
            if arr[i][j]=='0':
                return i,j

def bidirectional(initialConfiguration , finalConfiguration , N):
    initialState = State(initialConfiguration)
    finalState = State(finalConfiguration)
    frontierFront = []
    frontierBack = []

    exploredFront = set()
    exploredBack = set()

    frontierFrontSet = {}
    frontierBackSet={}

    # add initial state
    frontierFront.append(initialState)
    exploredFront.add(initialState.getConfigurationInString())
    frontierFrontSet[initialState.getConfigurationInString()] = initialState

    # add final state
    frontierBack.append(finalState)
    exploredBack.add(finalState.getConfigurationInString())
    frontierBackSet[finalState.getConfigurationInString()] = finalState



    Actions = {}
    Actions['left'] = [0,-1]
    Actions['right'] = [0,1]
    Actions['up'] = [-1,0]
    Actions['down'] = [1,0]
    print(Actions)


    while frontierFront and frontierBack :
        front = frontierFront.pop(0)
        back = frontierBack.pop(0)
        print()
        print('front , ' ,front.getConfigurationInString())
        print('back , ' ,back.getConfigurationInString())

        if front.getConfigurationInString() in frontierBackSet:
            intersectingNode = frontierBackSet[front.getConfigurationInString()]
            return getSteps(front , intersectingNode )
        
        if back.getConfigurationInString() in frontierFrontSet:
            intersectingNode = frontierFrontSet[back.getConfigurationInString()]
            return getSteps(intersectingNode , back)
        
        del frontierFrontSet[front.getConfigurationInString()]
        del frontierBackSet[back.getConfigurationInString()]

        i,j = findCoords(front , N)

        for action in Actions:
            iN , jN = i+Actions[action][0] , j+Actions[action][1]
            if isSafe(iN , jN , N):
                config = copy.deepcopy(front.getConfiguration())
                config[i][j] , config[iN][jN] = config[iN][jN] , config[i][j]
                newState = State(config , front , action)
                
                if newState.getConfigurationInString() not in exploredFront:
                    print('front')
                    print(newState.getConfigurationInString())
                    exploredFront.add(newState.getConfigurationInString())
                    frontierFront.append(newState)
                    frontierFrontSet[newState.getConfigurationInString()] = newState

                    if newState.getConfigurationInString() in frontierBackSet:
                        intersectingNode = frontierBackSet[newState.getConfigurationInString()]
                        return getSteps(newState , intersectingNode )
        
        
        
        i , j = findCoords(back , N)
        for action in Actions:
            iN , jN = i+Actions[action][0] , j+Actions[action][1]
            if isSafe(iN , jN , N):
                config = copy.deepcopy(back.getConfiguration())
                config[i][j] , config[iN][jN] = config[iN][jN] , config[i][j]
                newState = State(config , back , action)
                
                if newState.getConfigurationInString() not in exploredBack:
                    print('back')
                    print(newState.getConfigurationInString())
                    exploredBack.add(newState.getConfigurationInString())
                    frontierBack.append(newState)
                    frontierBackSet[newState.getConfigurationInString()] = newState

                    if newState.getConfigurationInString() in frontierFrontSet:
                        intersectingNode = frontierFrontSet[newState.getConfigurationInString()]
                        return getSteps(intersectingNode , newState)


        print()

    return False


def main():
    # for 8 puzzle
    N = 3
    initialConfiguration = []
    finalConfiguration = []
    for i in range(N):
        row = input('Enter %s row for initial configuration : \n' %i).split()
        initialConfiguration.append(row)

    for i in range(N):
        row = input('Enter %s row for final configuration : \n' %i).split()
        finalConfiguration.append(row)
    
    print(initialConfiguration)
    print(finalConfiguration)
    if bidirectional(initialConfiguration , finalConfiguration,N) == False:
        print("Cannot Be Solved")


if __name__=="__main__":
    main()

                







    