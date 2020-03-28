import tsp
import tsp_algorithms.Ants_python as ant
import tsp_algorithms.tsp_genetic as gene

def ant_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm
    """

    # ant algorithm configuration
    max_it = 100
    num_ants = 10
    decay = 0.1
    c_heur = 2.5
    c_local_phero = 0.1
    c_greed = 0.9

    best = ant.search(cities, max_it, num_ants, decay, c_heur, c_local_phero, c_greed)

    ant_route = [cities[i] for i in best['vector']]

    return ant_route

def genetic_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm
    """
    citylist = []

    for city in cities:
        citylist.append(gene.City(x=city[0], y=city[1]))

    # geneticAlgorithmPlot(population=cityList, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
    node_path = gene.geneticAlgorithm(population=citylist, popSize=100, eliteSize=20, mutationRate=0.01,
                                      generations=500)

    path = []
    # the path is actually made up of "Node" objects
    # so extract the information into a list
    for node in node_path:
        path.append((node.x, node.y))

    return path

def exact_tsp(cities):
    """
    :param cities : cities to run TSP on
    :return       : path calculated by this algorithm

    * this uses the python tsp package - exact algorithm
    """
    path = tsp.tsp(cities)[1]

    exact_route = [cities[i] for i in path]

    return exact_route
