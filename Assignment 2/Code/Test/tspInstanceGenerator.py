from random import randint as ri





def tspinstanceGen(n):
	matrix = [[0 for _ in range(n)] for _ in range(n)]
	for i in range(n):
		matrix[i][i] = 0
		for j in range(i+1,n):
			a = ri(1,10*n)
			matrix[i][j] = a
			matrix[j][i] = a
	return matrix


def printMA(n):
    ma = tspinstanceGen(n)
    print(ma)

    print('\n\n\n\n')
    for e in ma:
        print(*e)


n = int(input("Enter n : " ))
printMA(n)