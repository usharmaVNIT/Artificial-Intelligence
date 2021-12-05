# Python3 implementation to find minimum
# spanning tree for adjacency representation.
INT_MAX = float('inf')


# Returns true if edge u-v is a valid edge to be
# include in MST. An edge is valid if one end is
# already included in MST and other is not in MST.
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

	# Include first vertex in MST
	inMST[0] = True

	# Keep adding edges while number of included
	# edges does not become V-1.
	edge_count = 0
	mincost = 0
	while edge_count < V - 1:

		# Find minimum weight valid edge.
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

	print("Minimum cost = %d" % mincost)

# # Driver Code
# if __name__ == "__main__":
# 	''' Let us create the following graph
# 		2 3
# 	(0)--(1)--(2)
# 	| / \ |
# 	6| 8/ \5 |7
# 	| /	 \ |
# 	(3)-------(4)
# 			9		 '''

# 	cost = [[INT_MAX, 2, INT_MAX, 6, INT_MAX],
# 			[2, INT_MAX, 3, 8, 5],
# 			[INT_MAX, 3, INT_MAX, INT_MAX, 7],
# 			[6, 8, INT_MAX, INT_MAX, 9],
# 			[INT_MAX, 5, 7, 9, INT_MAX]]

# 	# Print the solution
# 	primMST(cost)

# # This code is contributed by
# # sanjeev2552


def makeAdjacency(graph):
	vertices = list(graph.keys())
	adj = [[float('inf') for _ in range(len(vertices))] for _ in range(len(vertices))]
	i = 0
	for i1 , v in enumerate(vertices):
		for i2 , j in enumerate(vertices):
			if j in graph[v]:
				adj[i1][i2] = graph[v][j]
	primMST(adj , len(vertices))
