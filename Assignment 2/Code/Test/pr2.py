INT_MAX = float('inf')


def isValidEdge(u, v, inMST):
	if u == v:
		return False
	if inMST[u] == False and inMST[v] == False:
		return False
	elif inMST[u] == True and inMST[v] == True:
		return False
	return True

def primMST(cost , V):
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
            print("Edge %d: (%d, %d) cost: %d" %
                (edge_count, a, b, minn))
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
    print(cost)
