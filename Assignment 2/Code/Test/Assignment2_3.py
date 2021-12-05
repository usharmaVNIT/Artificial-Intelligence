
import heapq

INT_MAX = float('inf')


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


        
    
        # i = 0
        # while True:
        #     neghibourName = input('Enter %s\'s %d neghibour else enter done to exit : ' %(x , i+1))
        #     if neghibourName=='done':
        #         break
        #     if neghibourName not in graph:
        #         print("Enter valid city ")
        #         continue
        #     if neghibourName==x:
        #         print("Cannot contain Loops ")
        #         continue
        #     if neghibourName in graph[x]:
        #         print("City Already is a neghibour ")
        #         continue
        #     neghibourCost = float(input("Enter cost of %s from %s : " %(x , neghibourName)))
        #     graph[x][neghibourName] = neghibourCost
        #     i+=1


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






def isValidEdge(u, v, inMST):
	if u == v:
		return False
	if inMST[u] == False and inMST[v] == False:
		return False
	elif inMST[u] == True and inMST[v] == True:
		return False
	return True

def primMST(cost , V):
    if len(cost)==0:
        return 0
    inMST = [False] * V

    inMST[0] = True

    edge_count = 0
    mincost = 0
    while edge_count < V - 1:
        minn = INT_MAX
        a = -1
        b = -1
        for i in range(V):
            for j in range(V):
                if cost[i][j] < minn:
                    if isValidEdge(i, j, inMST):
                        minn = cost[i][j]
                        a = i
                        b = j
        if a != -1 and b != -1:
            edge_count += 1
            mincost += minn
            inMST[b] = inMST[a] = True
        
    return mincost



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










def MinimumSpanningTree(graph):
    return makeAdjacency(graph)


# def printSolution(cityList):
#     lst = [ x[0]+' ( ' + str(x[1]) + ' ) ' for x in cityList]
#     print(*lst , sep=" ---->  ")
#     return True

def printSolution(child , start):
    lst = []
    while child.parent and child.parent != start :
        lst.append((child.name , child.cost))
        child = child.parent
    lst.append((start,0))
    lst = lst[::-1]
    print(*lst)
    return True


# def AStar():
#     graph = makeGraph()
#     print(graph)
#     cities = list(graph.keys())
#     totalCities = len(cities)
#     start = cities[0]
#     MSTCost = MinimumSpanningTree(graph)
#     frontier = []
#     copiedGraph = copyGraph(graph , start)
#     heapq.heappush(frontier , (MSTCost , (start , 0 , copiedGraph)))
#     exploredSet = set()
#     cityList = []
#     while frontier:
#         # print([[tmp[0],tmp[1][0]] for tmp in frontier])
#         MSTcost , (city ,cost , copiedGraph) = heapq.heappop(frontier)
#         cityList.append((city , cost))
#         exploredSet.add(city)
#         print("neghibour of ", city)
#         print(*list(graph[city].keys()))
#         for neghibour in graph[city]:
#             if neghibour == city :
#                 continue
#             if neghibour in exploredSet:
#                 # goal test
#                 # print(cityList)
#                 if len(cityList) == totalCities and neghibour == cities[0]:
#                     return printSolution(cityList)
#             else:
#                 neghibourCopiedGraph = copyGraph(copiedGraph , neghibour)
#                 mstCost = MinimumSpanningTree(neghibourCopiedGraph)
#                 pathCost = cost + graph[city][neghibour]
#                 totalCost = mstCost + pathCost
#                 heapq.heappush(frontier , (totalCost , (neghibour , pathCost , neghibourCopiedGraph)))
#                 print([[tmp[0],tmp[1][0]] for tmp in frontier])
#                 # exploredSet.add(neghibour)

#     return False

class Child:
    def __init__(self , name , cost=0 , parent=None , augumentedGraph = None , pathLength = 0 ) -> None:
        self.name = name
        self.cost = cost
        self.parent = parent
        self.augumentedGraph = augumentedGraph
        self.pathLength = pathLength
    
    def getCost(self):
        return self.cost
    
    def getParent(self):
        return self.parent
    
    def getName(self):
        return self.name

    def getAugumentedGraph(self):
        return self.augumentedGraph


def goalTest(child , cities):
    ptr = child
    cit = set(cities)
    while ptr:
        cit.remove(ptr.name)
        ptr = ptr.parent
    if cit:
        return False
    return



def AStar():
    graph = makeGraph()
    # print(graph)
    cities = list(graph.keys())
    totalCities = len(cities)
    start = cities[0]
    MSTCost = MinimumSpanningTree(graph)
    frontier = []
    copiedGraph = copyGraph(graph , start)
    child = Child(start , 0 , None , copiedGraph , 1)

    exploredSet = set()
    frontierSet = {}


    for neghibour in graph[start]:
        neghibourAugGraph = copyGraph(copiedGraph , neghibour)
        neghibourPathCost = graph[start][neghibour]
        neghibourMSTCost = MinimumSpanningTree(neghibourAugGraph)
        neghibourCost = neghibourPathCost + neghibourMSTCost
        neghibourChild = Child(neghibour , neghibourPathCost , child , neghibourAugGraph )
        heapq.heappush(frontier , (neghibourMSTCost , neghibourCost))
        frontierSet[neghibour] = neghibourPathCost
    
    while frontier:
        print([(x[0],x[1].name) for x in frontier ])
        _ , child  = heapq.heappop(frontier)
        cities.append(child)
        cparent = child.parent
        if cparent != None:
            cparent = cparent.name
        print(child.name , cparent)
        city = child.name
        augGraph = child.augumentedGraph
        cost = child.cost
        pathLength = child.pathLength
        # check for goal state
        if goalTest(child):
            return printSolution(child , start)
        exploredSet.add(city)
        del frontierSet[city]
        for neghibour in graph[city]:
            if neghibour==city:
                continue
            neghibourPathCost = cost + graph[city][neghibour]
            neghibourAugGraph = copyGraph(augGraph , neghibour)
            neghibourMSTCost = MinimumSpanningTree(neghibourAugGraph)
            neghibourCost = neghibourPathCost + neghibourMSTCost
            neghibourChild = Child(neghibour , neghibourPathCost , child , neghibourAugGraph , pathLength + 1)
            if neghibour not in exploredSet and neghibour not in frontierSet:
                heapq.heappush(frontier , (neghibourCost , neghibourChild))
                frontierSet[neghibour] = neghibourCost
            elif neghibour in frontierSet and frontierSet[neghibour] > neghibourCost:
                frontierSet[neghibour] = neghibourCost
                ind = 0
                while ind<len(frontier):
                    if frontier[ind][1].name == neghibour:
                        break
                    ind+=1
                frontier[ind] = (neghibourCost, neghibourChild)
                print([(x[0],x[1].name) for x in frontier ])
                heapq.heapify(frontier)
            elif neghibour in exploredSet and exploredSet[neghibour] > neghibourCost :
                del exploredSet[neghibourCost]
                heapq.heappush(frontier , (neghibourCost , neghibourChild))
    return False


                



def main():
    if AStar() == False:
        print("Cannnot Find The MST")


if __name__=="__main__":
    main()








