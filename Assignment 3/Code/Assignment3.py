# Assignment 3 Artificial Intelligence
# T.S.P with Genetic Algorithm

# Ujjwal Sharma
# BT18CSE021
# usharma@students.vnit.ac.in


from random import randint , shuffle , random , choice
import time

# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


class OffSpring:
    def __init__(self , path , graph) -> None:
        # To store the path
        self.path = path
        # Path Cost is the sum of distances b/w cities in path
        self.pathCost = self.pathCostOfOffspring(graph)
        # fitness is 1/pathCost
        self.fitness = self.fitnessOfOffspring()

    def pathCostOfOffspring(self, graph):
        pathCost = 0
        path = self.path
        parent = path[0]
        i = 1
        while i<len(path):
            pathCost+=graph[parent][path[i]]
            parent = path[i]
            i+=1
        return pathCost

    def fitnessOfOffspring(self):
        return 1/ (self.pathCost + 1)


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def PartialMappedCrossover(parent1 , parent2 , graph):
    path1 = parent1.path[1:-1] # because start state and end state are fixed
    path2 = parent2.path[1:-1] # because start state and end state are fixed
    start = parent1.path[0]

    # selecting 1/3 of the path
    oneThirdLength = len(path1)//3 + 1
    startIndex = randint(0 , len(path1) - oneThirdLength )
    endIndex = startIndex + oneThirdLength - 1

    # print(startIndex , endIndex)

    pathOffspring1 = [-1]*len(path1)
    pathOffspring2 = [-1]*len(path2)
    
    # Exchanging the slices
    for i in range(startIndex , endIndex + 1):
        pathOffspring1[i] = path2[i]
        pathOffspring2[i] = path1[i]
    
    # Completing the path of offspring 1 i.e corresponding mapping of parent 1
    path1set = set(pathOffspring1)
    i = 0
    j = 0
    while i<len(path1) and j<len(pathOffspring1):
        if path1[i] in path1set:
            i+=1
            continue
        if pathOffspring1[j] != -1:
            j+=1
            continue
        pathOffspring1[j] = path1[i]
        path1set.add(path1[i])
        i+=1
        j+=1
    
    # Completing the path of offspring 2 i.e corresponding mapping of parent 2
    path2set = set(pathOffspring2)
    i = 0
    j = 0
    while i<len(path2) and j<len(pathOffspring2):
        if path2[i] in path2set:
            i+=1
            continue
        if pathOffspring2[j] != -1:
            j+=1
            continue
        pathOffspring2[j] = path2[i]
        path2set.add(path2[i])
        i+=1
        j+=1
    


    # print(pathOffspring1)
    # print(pathOffspring2)



    # Adding the start cities to offsprings' paths
    pathOffspring1.insert(0 , start)
    pathOffspring2.insert(0,start)
    pathOffspring1.append(start)
    pathOffspring2.append(start)
    
    # making the offsprings with specified paths
    OffSpring1 = OffSpring(pathOffspring1 , graph)
    OffSpring2 = OffSpring(pathOffspring2 , graph)
    return OffSpring1 , OffSpring2


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def orderCrossOverFunction(parent1 , parent2 , graph):
    path1 = parent1.path[1:-1] # because start state and end state are fixed
    path2 = parent2.path[1:-1] # because start state and end state are fixed
    start = parent1.path[0]

    # selecting 1/3 of the path
    oneThirdLength = len(path1)//3 + 1
    startIndex = randint(0 , len(path1) - oneThirdLength )
    endIndex = startIndex + oneThirdLength - 1


    pathOffspring1 = [-1]*len(path1)
    pathOffspring2 = [-1]*len(path2)

    # Keeping the slices
    for i in range(startIndex , endIndex + 1):
        pathOffspring1[i] = path1[i]
        pathOffspring2[i] = path2[i]
    
    # Completing the path of offspring 1 by exchanging the mapping of parent 2 in cyclic order
    j = (endIndex+1) % (len(path2))
    i = j
    set1 = set(path1[startIndex:endIndex+1])
    while len(set1)!=len(path1):
        if path2[j] in set1:
            j = (j+1) % len(path1)
            continue
        pathOffspring1[i] = path2[j]
        set1.add(path2[j])
        j = (j+1) % len(path2)
        i = (i+1) % len(path2)
        

    # Completing the path of offspring 2 by exchanging the mapping of parent 1 in cyclic order
    j = (endIndex+1) % (len(path2))
    i = j
    set2 = set(path2[startIndex:endIndex+1])
    while len(set2)!=len(path1):
        if path1[j] in set2:
            j = (j+1) % len(path1)
            continue
        pathOffspring2[i] = path1[j]
        set2.add(path1[j])
        j = (j+1) % len(path2)
        i = (i+1) % len(path2)
        
    # print(pathOffspring1)
    # print(pathOffspring2)

    # Adding the start cities to offsprings' paths
    pathOffspring1.insert(0 , start)
    pathOffspring2.insert(0,start)
    pathOffspring1.append(start)
    pathOffspring2.append(start)
    
    # making the offsprings with specified paths
    OffSpring1 = OffSpring(pathOffspring1 , graph)
    OffSpring2 = OffSpring(pathOffspring2 , graph)
    return OffSpring1 , OffSpring2


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************

def randomCrossover(parent1 , parent2 , graph):
    path1 = parent1.path[1:-1] # because start state and end state are fixed
    path2 = parent2.path[1:-1] # because start state and end state are fixed
    start = parent1.path[0]

    # randomly selecting the index 
    randomIndex = randint(1 , len(path1) - 2)

    pathOffspring1 = [-1]*len(path1)
    pathOffspring2 = [-1]*len(path2)

    # exchanging the information
    pathOffspring1[randomIndex:] = path2[randomIndex:]
    pathOffspring2[randomIndex:] = path1[randomIndex:]


    # Completing the path of offspring 1 i.e corresponding mapping of parent 1
    path1set = set(pathOffspring1)
    i = 0
    j = 0
    while i<len(path1) and j<len(pathOffspring1):
        if path1[i] in path1set:
            i+=1
            continue
        if pathOffspring1[j] != -1:
            j+=1
            continue
        pathOffspring1[j] = path1[i]
        path1set.add(path1[i])
        i+=1
        j+=1
    
    # Completing the path of offspring 2 i.e corresponding mapping of parent 2
    path2set = set(pathOffspring2)
    i = 0
    j = 0
    while i<len(path2) and j<len(pathOffspring2):
        if path2[i] in path2set:
            i+=1
            continue
        if pathOffspring2[j] != -1:
            j+=1
            continue
        pathOffspring2[j] = path2[i]
        path2set.add(path2[i])
        i+=1
        j+=1
    

    # Adding the start cities to offsprings' paths
    pathOffspring1.insert(0 , start)
    pathOffspring2.insert(0,start)
    pathOffspring1.append(start)
    pathOffspring2.append(start)
    
    # making the offsprings with specified paths
    OffSpring1 = OffSpring(pathOffspring1 , graph)
    OffSpring2 = OffSpring(pathOffspring2 , graph)
    return OffSpring1 , OffSpring2


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def mutate(path , graph):
    start = path[0]
    newPath = path[1:-1]
    # randomly selecting 2 indexces that are not equal
    i = randint(0 , len(newPath)-1)
    j = randint(0 , len(newPath)-1)
    while i == j:
        j = randint(0 , len(newPath)-1)

    # Mutating the path i.e exchanging the city
    newPath[i] , newPath[j] = newPath[j] , newPath[i]
    # inserting the starting city to the mutated path
    newPath.insert(0 , start)
    newPath.append(start)
    # making mutated Offspring
    mutatedOffSpring = OffSpring(newPath , graph)
    return mutatedOffSpring
    

# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def GeneticAlgorithm(graph , Time = 1000 , populationSize = 100 , crossOverFunction = orderCrossOverFunction , mutationRate = 0.01 , selectionPercentage = 25):
    print("\n\n\n\n")

    print("Cross Over Function Used :" , crossOverFunction.__name__)

    print("\n\n\n\n")

    # Making the initial population by randomly sampling the paths with specidfied start city
    cities = list(graph.keys())
    start = cities[0]
    cities.pop(0)
    population = []
    for i in range(populationSize):
        shuffle(cities)
        offSpringPath = [start] + cities[:] + [start]
        offSpring = OffSpring(offSpringPath , graph)
        population.append(offSpring)
    
    # Now only selecting the population that have high fitness i.e elimination of the weak .. ;)
    # i have choosen the default to 25% best Offsprings from the total population
    # one can specify any value

    # here i have sorted the population on the bases of fitness (decreasing) i.e 
    # in the pathCost are in increasing order

    selectionRate = 100/selectionPercentage 

    population = sorted(population , key= lambda x : x.fitness , reverse=True)[0:int(populationSize//selectionRate)+1]

    epochs = Time
    avgFitnessScore = []
    minPathScore = []
    minPathCost = float('inf')
    MinOffspring : OffSpring
    MinOffspringGeneration = 0
    printLimit = epochs // 4


    # this is to measure the performance of the algorithm
    startTime = time.time()


    for epoch in range(epochs):
        newPopulation = []
        # this set is to make sure that the offsprings doesnot have same path i.e no duplicates
        newPopulationSet = set()
        if epoch%printLimit == 0:
            print(epoch/epochs*100)
        # this loop is to generate offsprings that are to be added in the newPopulation
        for i in range(populationSize):
            # randomly selecting the parents that are different
            parent1 = choice(population)
            parent2 = choice(population)
            while parent1 == parent2:
                parent2 = choice(population)

            # Creating the offsprings by the specified crossover function
            offSpring1 , offSpring2 = crossOverFunction(parent1 , parent2 , graph)

            # mutating the offspring with a  mutation probability of 1% (default)
            # this is the mutation rate . Mutation Probability = mutation rate * 100
            if random() <= mutationRate:
                offSpring1 = mutate(offSpring1.path , graph)
            if random() <= mutationRate:
                offSpring2 =  mutate(offSpring2.path , graph)

            # checking for duplicate paths in the new Population and if not found
            # add to the new population

            p1 = ','.join([str(x) for x in offSpring1.path])
            if p1 not in newPopulationSet:
                newPopulation.append(offSpring1)
                newPopulationSet.add(p1)
            
            p2 = ','.join([str(x) for x in offSpring2.path])
            if p2 not in newPopulationSet:
                newPopulation.append(offSpring2)
                newPopulationSet.add(p2)
        
        avgFitness = 0
        minPathCostPopulation = float('inf')

        # again selecting selectionPercentage of the new population
        newPopulation = sorted(newPopulation , key= lambda x : x.fitness , reverse=True)[0:int(populationSize//selectionRate) +1]
        population = newPopulation[:]
        if epoch%printLimit == 0:
            print([x.pathCost for x in newPopulation])
        
        # calculating the average fitness of the new Population
        for offSpring in newPopulation:
            avgFitness += offSpring.fitness

        avgFitness/=len(newPopulation)
        
        
        # minPathCostPopulation = float('inf')
        # ind = -1
        # for i,offspring in enumerate(newPopulation):
        #     if offspring.pathCost < minPathCostPopulation:
        #         minPathCostPopulation = offspring.pathCost
        #         ind = i

        minPathCostPopulation = newPopulation[0].pathCost
    
        if minPathCostPopulation < minPathCost:
            minPathCost = minPathCostPopulation
            MinOffspring = newPopulation[0]   
            MinOffspringGeneration = epoch+1 

        # keeping track of average fitness and minimum path cost for every generation
        avgFitnessScore.append([epoch+1 , avgFitness])
        minPathScore.append([epoch+1  , minPathCostPopulation])

    endTime = time.time() 

    # Total time taken by the algorithm
    totalTimeTaken = endTime - startTime

    print('\n\n')
    print("Total Time Taken for %d generations using %s crossover is %f seconds " %(Time , crossOverFunction.__name__ , totalTimeTaken))


    print('\n\n\n')
    return MinOffspring ,MinOffspringGeneration, avgFitnessScore , minPathScore


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************

# Function to plot the graph
def drawPlot(XAxis , XAxisName , YAxis , YAxisName):
    import matplotlib.pyplot as plt

    plt.plot(XAxis , YAxis)
    plt.xlabel(XAxisName)
    plt.ylabel(YAxisName)

    plt.show()

# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


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


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************

# utility to pring the path
def printPath(path , graph):
    import networkx as nx
    
    import matplotlib.pyplot as plt

    g = nx.DiGraph()

    i = 1
    edges = []
    while i<len(path):
        g.add_edge(path[i-1] , path[i] , weight = graph[path[i-1]][path[i]])
        # edges.append([path[i-1] , path[i]])
        i+=1
    pos = nx.circular_layout(g)
    plt.figure(figsize=(len(path)//2,len(path)//2)) 
    nx.draw_networkx(g,pos , with_labels = True , node_size=len(path)*30 ,edge_color="tab:red" , node_color='black' , font_color='white')
    labels = nx.get_edge_attributes(g,'weight')
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels , font_color='green')


# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def drawGraph(graph):
    import networkx as nx
    
    import matplotlib.pyplot as plt

    g = nx.Graph()
    nodes = list(graph.keys())
    for node1 in graph:
        for node2 in graph[node1]:
            g.add_edge(node1 , node2 , weight = graph[node1][node2])
        
    pos = nx.random_layout(g)
    plt.figure(figsize=(len(nodes),len(nodes))) 
    nx.draw_networkx(g,pos , with_labels = True , node_size=len(nodes)*40 ,edge_color="tab:red" , node_color='red' , font_color='black')
    labels = nx.get_edge_attributes(g,'weight')
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels , font_color='green')

   
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************
# ******************************************************************************************************************************************


def main():
    graph = makeGraph()

    #  Order CrossOver Function

    MinOffspring ,MinOffSpringGeneration, avgFitnessScore , minPathScore = GeneticAlgorithm(graph , Time=1000 , populationSize=100 ,crossOverFunction=orderCrossOverFunction , mutationRate=0.01 , selectionPercentage=25)
    XAxis = [x[0] for x in avgFitnessScore]
    YAxis = [x[1] for x in avgFitnessScore]
    drawPlot(XAxis , "Generations" , YAxis ,"Average Fitness ( i.e 1/pathCost )" )
    XAxis = [x[0] for x in minPathScore]
    YAxis = [x[1] for x in minPathScore]
    drawPlot(XAxis , "Generations" , YAxis , "Minimum Path Cost")

    print("Minimum Path Cost : " , MinOffspring.pathCost)
    print("Minimum Path Cost Generation : " , MinOffSpringGeneration)

    print("Path : " , MinOffspring.path)

    printPath(MinOffspring.path , graph)




    # Partial Mapping Crossover function

    MinOffspring ,MinOffSpringGeneration, avgFitnessScore , minPathScore = GeneticAlgorithm(graph , Time=1000 , populationSize=100 ,crossOverFunction=PartialMappedCrossover , mutationRate=0.01 , selectionPercentage=25)
    XAxis = [x[0] for x in avgFitnessScore]
    YAxis = [x[1] for x in avgFitnessScore]
    drawPlot(XAxis , "Generations" , YAxis ,"Average Fitness ( i.e 1/pathCost )" )
    XAxis = [x[0] for x in minPathScore]
    YAxis = [x[1] for x in minPathScore]
    drawPlot(XAxis , "Generations" , YAxis , "Minimum Path Cost")

    print("Minimum Path Cost : " , MinOffspring.pathCost)
    print("Minimum Path Cost Generation : " , MinOffSpringGeneration)

    print("Path : " , MinOffspring.path)

    printPath(MinOffspring.path , graph)




    # Random Crossover Function
    
    MinOffspring ,MinOffSpringGeneration, avgFitnessScore , minPathScore = GeneticAlgorithm(graph , Time=1000 , populationSize=100 ,crossOverFunction=randomCrossover , mutationRate=0.01 , selectionPercentage=25)
    XAxis = [x[0] for x in avgFitnessScore]
    YAxis = [x[1] for x in avgFitnessScore]
    drawPlot(XAxis , "Generations" , YAxis ,"Average Fitness ( i.e 1/pathCost )" )
    XAxis = [x[0] for x in minPathScore]
    YAxis = [x[1] for x in minPathScore]
    drawPlot(XAxis , "Generations" , YAxis , "Minimum Path Cost")

    print("Minimum Path Cost : " , MinOffspring.pathCost)
    print("Minimum Path Cost Generation : " , MinOffSpringGeneration)

    print("Path : " , MinOffspring.path)

    printPath(MinOffspring.path , graph)





if __name__ == "__main__":
    main()