

class GraphNode:
    def __init__(self , name):
        self.name = name
        self.neghibours = []

    def addNeghibour(self , neghibour):
        self.neghibours.append(neghibour)
    
    def addNeghibours(self , neghibours):
        self.neghibours = self.neghibours + neghibours

    def __eq__(self , node):
        return self.name == node.name

def makeGraph():
    totalCities = int(input("Enter Number of cities : "))
    cities = []
    for x in range(totalCities):
        cityName = input("Enter name of %d city : " %(x+1))
        city = GraphNode(cityName)
        cities.append(city)
    for x,city in enumerate(cities):
        neghibourCount = int(input("Enter the count of neghibours of %s : " %(city.name)))
        for t in range(neghibourCount):
            cityName = input("Enter the city name of %d neghibour : " %(t+1))
            index = -1
            for i in range(totalCities):
                if cities[i].name == cityName:
                    index = i
                    break
            if index == -1:
                print("No city with specified name .")
                t-=1
                continue
            if index == i:
                print("Cannot have loop . ")
                t-=1
                continue
            neghibourCost = float(input("Enter the cost of %s from %s" %(cities[index].name , city.name)))
            neghibour = [cities[index] , neghibourCost]
            city.addNeghibour(neghibour)

    return cities






    


    

        