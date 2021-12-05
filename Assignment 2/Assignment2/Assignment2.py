# UJJWAl SHARMA
# BT18CSE021
# usharma@students.vnit.ac.in


# importing modules
# for priority queue
import heapq

INT_MAX = float('inf')

# Class to define a graph node of A*
class GraphNode:
    def __init__(self , name , parent , pathCost , augumentedGraph) -> None:
        self.name = name
        self.parent = parent
        self.pathCost = pathCost
        # graph which has all the cities removed which are visiter including current
        self.augumentedGraph = augumentedGraph
        # local set to check visited states(cities)
        self.visited = set()
        self.visited.add(name)
        if parent:
            self.visited = self.visited.union(parent.visited)
        # path to reach the current state
        self.path = []
        if parent:
            self.path = parent.path[:]
        self.path.append(name)
        
    def checkGoalNode(self , start , cities):
        if self.name == start:
            # print("Same Name")

            # to check the goal state starting city = end city and
            # all cities visited
            for city in cities:
                if city not in self.visited:
                    return False
            return True
        return False
    
    # for local checking if the city is already visited
    def isVisted(self , name):
        if name in self.visited:
            return True
        return False

    # for comparison b/w nodes . I have preferred low path cost
    # Note this is to break the tie when 2 states have same priority
    # i.e same f(n) = g(n) + h(n) value ..
    def __gt__(self , other):
        return self.pathCost > other.pathCost




# Utility function to make a graph
def makeGraph():
    graph = {}
    totalCities = int(input("Enter Total cities count : "))
    i = 0
    cities = []
    while i<totalCities:
        cityName = input("Enter City %d name : " %(i+1))
        if cityName in graph:
            print("City already exists . ")
            continue
        graph[cityName] = {}
        cities.append(cityName)
        i+=1

    for x in cities:
        # print(*cities)
        distances = input("Enter the distances from cities (space seperated and in order as shown) to %s , (enter inf for no edge) : \n" %(x)).split()
        for c,d in zip(cities,distances):
            if d != 'inf':
                graph[x][c] = int(d)

    return graph



# utility function to copy a graph removing all the edges of the specified city
def copyGraph(graph , city):
    ngraph = {}
    for x in graph:
        if x == city:
            continue
        ngraph[x] = {}
        for c in graph[x]:
            if c == city:
                continue
            ngraph[x][c] = graph[x][c]
    # print("Copied")
    return ngraph



# Utility for checking in edge in MST 
def isValidEdge(edge1, edge2, inMST):
	if edge1 == edge2:
		return False
	if inMST[edge1] == False and inMST[edge2] == False:
		return False
	elif inMST[edge1] == True and inMST[edge2] == True:
		return False
	return True




# function to calculate MST cost using Prim's Algorithm
def primMST(cost , Vertices):
    if len(cost)==0:
        return 0
    inMST = [False] * Vertices

    inMST[0] = True

    edgeCount = 0
    minimumCost = 0
    while edgeCount < Vertices - 1:
        mn = INT_MAX
        a = -1
        b = -1
        for i in range(Vertices):
            for j in range(Vertices):
                if cost[i][j] < mn:
                    if isValidEdge(i, j, inMST):
                        mn = cost[i][j]
                        a = i
                        b = j
        if a != -1 and b != -1:
            edgeCount += 1
            minimumCost += mn
            inMST[b] = inMST[a] = True
        
    return minimumCost


# utility for adjusting the graph as a adjacency matrix for MST calculation
def makeAdjacency(graph):
    vertices = list(graph.keys())
    adj = [[float('inf') for _ in range(len(vertices))] for _ in range(len(vertices))]
    i = 0
    for i1 , v in enumerate(vertices):
        for i2 , j in enumerate(vertices):
            if j in graph[v]:
                adj[i1][i2] = graph[v][j]
    cost = primMST(adj , len(vertices))
    return cost


# Wrapper Function for my ease
# return the mst cost of a graph
def MST(graph):
    return makeAdjacency(graph)


# Utility function to print the graph of cities
def printGraph(graph):

    print()
    print("\n\t\tThe Graph : \n")
    for e in graph:
        print(e , end=' : \t')
        lst = []
        for v in graph[e]:
            lst.append((v + ' ( ' + str(graph[e][v]) + ' ) '))
        print(*lst,sep=' --> ')



# Utility for printing the answer
# When A* search fulfills the goalTest this will print the cost , path(s) and expanded nodes
def printAnswer(node , graph , ExpandedNode , TotalNodes , frontierNodes):
    print('\n\n\n')
    print("**\n\t Cost : " , node.pathCost , " ( Note this is the cost of the loop ) ")
    print()
    print("\t -----  Path  -----  \n")
    path = node.path
    i = 1
    newArr = []
    while i<len(path):
        cst = graph[path[i]][path[i-1]]
        cstnew = path[i-1] + ' ( ' + str(cst) + ' ) '
        newArr.append(cstnew)
        i+=1
    newArr.append(path[-1] + ' ( 0 ) ')
    print(*newArr  , sep=' ---> ')
    print('\n')
    
    l1 = node.path[-1]
    l2 = node.path[-2]
    cost = node.pathCost - graph[l1][l2]

    print("**\n\tCost for visiting without loop : " , cost)
    print('\n\t -----  Path  -----  \n')
    newArr.pop(-1)
    newArr[-1] = (l2 + ' ( 0 ) ')
    print(*newArr, sep=' ---> ')
    print('\n\n')

    print("Total Nodes Expanded : ", ExpandedNode )
    print()
    print('Total Nodes Generated : ' , TotalNodes)
    print()
    print("Total Node in frontier : " , frontierNodes)
    print('\n\n\n\n')
    return True


# A* Search Algorithm
def AStar():
    graph = makeGraph()
    if input("Do you want to print the graph : 'y'es or 'n'o : ") == 'y':
        printGraph(graph)
    cities = list(graph.keys())

    totalNode = 0
    expandedNodes = 0

    frontier = []
    start = cities[0]
    # Augumented graph i.e after removing start city
    copiedGraph = copyGraph(graph , start)
    startNode = GraphNode(start , None , 0 , copiedGraph)
    # MST cost of augumented graph
    mstCost = MST(startNode.augumentedGraph)
    # the total estimated cost of the node 
    totalCost = startNode.pathCost + mstCost #  <----- f(n) = g(n) + h(n) 
    heapq.heappush(frontier , (totalCost , startNode))
    totalNode+=1

    exploredSet = set() # global explored set for global checking

    while frontier:
        # remove the least estimated cost node from the frontier priority queue
        totalCost , node  = heapq.heappop(frontier)
        
        # print([ (x[0],x[1].name) for x in frontier ])
        # print(node.name)

        # Check for the goal Node ( specified in the GraphNode Class)
        if node.checkGoalNode(start , cities):
            # If passed then return the answer
            return printAnswer(node , graph , expandedNodes , totalNode , len(frontier))
        name = node.name
        pathCost = node.pathCost
        augGraph = node.augumentedGraph
        expandedNodes+=1
        # print('path of %s : ' %node.name , *node.path)


        # If goal test fails then generate successor states
        for neghibour in graph[name]:
            if neghibour==name:
                continue
            # this is the local check ( within the graph ) that was menntioned earlier
            if node.isVisted(neghibour) == False:
                # if the neghibor is not visited then
                # generate path cost
                newNodePathCost = pathCost + graph[name][neghibour]
                # generate augumented graph (removing neghibour )
                newNodeAugGraph = copyGraph(augGraph , neghibour)
                # create successor state
                newNode = GraphNode(neghibour , node , newNodePathCost , newNodeAugGraph)
                # calculate mst cost of the augumented graph ( after removing all visited cities)
                newNodeMSTCost = MST(newNodeAugGraph)
                # total estimated cost of the node
                newNodeTotalCost = newNodePathCost+newNodeMSTCost


                # print([ (x[0],x[1].name) for x in frontier ])
                # print((newNodeTotalCost , newNode.name))


                # This is a global check to identify if the path is not repeated
                if tuple(newNode.path) not in exploredSet:
                    # if not repeated then push it into the frontier proprity queue
                    heapq.heappush(frontier , (newNodeTotalCost , newNode))
                    totalNode+=1
                    exploredSet.add(tuple(newNode.path))
            elif neghibour == start and len(node.path) == len(cities):
                # else if the neghibour is the start city and
                # all cities are visited ( path lenght of the node = total cities)
                # then add this to frontier priority queue for the goal state test
                # note goal test is done after removing node from the frontier

                # generate augumented graph which will be empty ..
                newNodeAugGraph = copyGraph(augGraph , neghibour)
                # calculate mst cost which will be 0 ..
                newNodeMSTCost = MST(newNodeAugGraph)
                # calculate path cost as mst will be 0 therefore same as estimated cost
                newNodePathCost = pathCost + graph[name][neghibour] + newNodeMSTCost
                newNode = GraphNode(neghibour , node , newNodePathCost , {})
                # estimated cost = path cost
                newNodeTotalCost = newNodePathCost


                # print([ (x[0],x[1].name) for x in frontier ])
                # print((newNodeTotalCost , newNode.name))


                # Add the node to frontier priority queue
                heapq.heappush(frontier , (newNodeTotalCost , newNode))
                totalNode+=1

        # print([ (x[0],x[1].name) for x in frontier ])
        
    # If frontier becomes empty then there is no solution to tsp instance ..
    return False


# Main Function
def main():
    if AStar() == False:
        print('\n\n')
        print("THIS INSTANCE DOESNOT HAVE ANY SOLUTION")
        print('\n\n')

if __name__ == "__main__":
    main()

