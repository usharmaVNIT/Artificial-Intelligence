# BT18CSE021
# UJJWAL SHARMA
# usharma@students.vnit.ac.in



import copy

# class to represent a state
class State:
    def __init__(self , configuration , parent=None , action_taken = None ):
        self.configuration = configuration
        self.parent = parent
        # action taken to get to this state
        self.action = action_taken
    
    # getter function to get the configuration of the state
    def getConfiguration(self):
        return self.configuration

    # This function will be used to hash the states as in python lists ( mutable ) are not hashable
    def getConfigurationInString(self):
        return '[' + ','.join([ ','.join(x) for x in self.configuration]) + ']'



# This is a utility function to print the steps to be taken to solve the problem

def getSteps(state1 , state2):
    steps = []
    state = state1
    while state.parent != None:
        steps = [state] + steps
        state = state.parent
    steps = [state] + steps

    # this will help to complement the actions because these actions will be taken w.r.t
    # goal state so we need the reverse of those steps
    actionComplement = {}
    actionComplement['left'] = 'right'
    actionComplement['right'] = 'left'
    actionComplement['up'] = 'down'
    actionComplement['down'] = 'up'

    # this is some utility logic i have written print the steps to be taken in a state
    # as we have the action taken to reach the state 
    i = 0
    while i<len(steps)-1:
        steps[i].action = steps[i+1].action
        i+=1

    opposite_Steps = []
    state = state2
    while state.parent!= None:
        # here i am complementing the actions taken w.r.t goal state
        state.action = actionComplement[state.action]
        opposite_Steps.append(state)
        state = state.parent
    opposite_Steps.append(state)
    
    
    finalSteps = steps[:-1] + opposite_Steps


    for e in finalSteps:
        conf = e.getConfiguration()
        # printing the state and action to be taken in that state
        print("State : ")
        for n in conf:
            print('\t' , *n)
        print('ACTION to be taken : ' , e.action)
        print()
    return True


#  both are utility functions
def isSafe(i , j , n):
    return 0<=i<n and 0<=j<n

def findCoords(state , n):
    arr = state.getConfiguration()
    for i in range(n):
        for j in range(n):
            if arr[i][j]=='0':
                return i,j


# this is the bidirectional search
def bidirectional(initialConfiguration , finalConfiguration , N):
    initialState = State(initialConfiguration)
    finalState = State(finalConfiguration)
    
    # queues for bfs

    frontierFront = []
    frontierBack = []

    # constant time lookup for explored states
    exploredFront = set()
    exploredBack = set()

    # here i have used dictionary instead of sets because i will hash it using the 
    # string representation but i need a state so i will simply map the hash 
    # to the state  ;)
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

    # actions to be taken ..

    Actions = {}
    Actions['left'] = [0,-1]
    Actions['right'] = [0,1]
    Actions['up'] = [-1,0]
    Actions['down'] = [1,0]
    print("Actions : ")
    for action in Actions:
        print('\t',action)
    print('\n')
    # main loop
    while frontierFront and frontierBack :
        # taking the 1st state from both the frontiers
        front = frontierFront.pop(0)
        back = frontierBack.pop(0)
        # print()
        # print('front , ' ,front.getConfigurationInString())
        # print('back , ' ,back.getConfigurationInString())
        
        # Check if there is any intersection between the frontiers 
        if front.getConfigurationInString() in frontierBackSet:
            intersectingNode = frontierBackSet[front.getConfigurationInString()]
            # if found return the steps ...
            return getSteps(front , intersectingNode )
        
        if back.getConfigurationInString() in frontierFrontSet:
            intersectingNode = frontierFrontSet[back.getConfigurationInString()]
            # if found return the steps ...
            return getSteps(intersectingNode , back)
        
        # remove the states from the corresponding frontiers
        del frontierFrontSet[front.getConfigurationInString()]
        del frontierBackSet[back.getConfigurationInString()]

        # Note i am checking the intersection while expanding . one can also
        # check it while the node is discovered 1st time like in line 169 to 175 . this will
        # help in making the solution converge faster but overall complexity remains same so ..


        # Now check for all actions possible in the current state
        i,j = findCoords(front , N)

        for action in Actions:
            iN , jN = i+Actions[action][0] , j+Actions[action][1]
            if isSafe(iN , jN , N):
                config = copy.deepcopy(front.getConfiguration())
                config[i][j] , config[iN][jN] = config[iN][jN] , config[i][j]
                # making a new state . 
                newState = State(config , front , action)
                
                if newState.getConfigurationInString() not in exploredFront:
                    # print('front')
                    # print(newState.getConfigurationInString())
                    exploredFront.add(newState.getConfigurationInString())
                    frontierFront.append(newState)
                    frontierFrontSet[newState.getConfigurationInString()] = newState
                    # Note the check for intersection can be done here
        
        
        # similar logic for backward expansion
        i , j = findCoords(back , N)
        for action in Actions:
            iN , jN = i+Actions[action][0] , j+Actions[action][1]
            if isSafe(iN , jN , N):
                config = copy.deepcopy(back.getConfiguration())
                config[i][j] , config[iN][jN] = config[iN][jN] , config[i][j]
                newState = State(config , back , action)
                
                if newState.getConfigurationInString() not in exploredBack:
                    # print('back')
                    # print(newState.getConfigurationInString())
                    exploredBack.add(newState.getConfigurationInString())
                    frontierBack.append(newState)
                    frontierBackSet[newState.getConfigurationInString()] = newState

    # if no intersection state is found then no solution exists
    return False



# Note that i have expanded only 1 node from both frontiers each time but this can also
# be implemented using threads.
# thread 1 will expand from front while checking for intersection
# thread 2 will expand from back again while checking for intersection
# and once the intersection is found then exit the threads and print the solution
# else no solution exists



def main():
    # for 8 puzzle
    N = 3
    initialConfiguration = []
    finalConfiguration = []
    for i in range(N):
        row = input('Enter %s row for initial configuration : \n' %i).split()
        initialConfiguration.append(row)
    print()
    for i in range(N):
        row = input('Enter %s row for final configuration : \n' %i).split()
        finalConfiguration.append(row)
    
    print("Initial Configuration : ")
    print()
    for e in initialConfiguration:
        print('\t' , *e)

    print()
    print("Final Configuration : ")
    for e in finalConfiguration:
        print('\t' , *e)
    print()
    
    # Call the Search Strategy ( Bidirectional Search )
    if bidirectional(initialConfiguration , finalConfiguration,N) == False:
        print("Cannot Be Solved")


if __name__=="__main__":
    main()


# All the functions are named according to the working
# and the code is easy to understand as variables are also named so .
# logical structure is also easily understandable and as python is easily readable
# so understanding the code is fairly easy . I have also incorporated comments to
# make the reader understand the basic functionality and logical connections ..