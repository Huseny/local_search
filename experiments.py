from graph import Graph
import random
from time import time
from searches import Search
from matplotlib import pyplot as plt
import numpy as np


##################################### Number 1 #######################################
graph = Graph()
file_path = "Cities.txt"

with open(file_path, 'r') as txt_file:
    file_contents = txt_file.readlines()
    location = {}
    for line in file_contents:
        cur = line.split()
        city = {
            "name": cur[0],
            'Latitude': cur[1],
            "Longitude": cur[2]
        }
        location[cur[0]] = city

Neamt = graph.create_node(location["Neamt"])
Iasi = graph.create_node(location["Iasi"])
Vaslui = graph.create_node(location["Vaslui"])
Urziceni = graph.create_node(location["Urziceni"])
Hirsova = graph.create_node(location["Hirsova"])
Eforie = graph.create_node(location["Eforie"])
Bucharest = graph.create_node(location["Bucharest"])
Giurgiu = graph.create_node(location["Giurgiu"])
Craiova = graph.create_node(location["Craiova"])
Pitesti = graph.create_node(location["Pitesti"])
Fagaras = graph.create_node(location["Fagaras"])
Rimnicu_Vilcea = graph.create_node(location["RimnicuVilcea"])
Sibiu = graph.create_node(location["Sibiu"])
Drobeta = graph.create_node(location["Drobeta"])
Mehadia = graph.create_node(location["Mehadia"])
Lugoj = graph.create_node(location["Lugoj"])
Timisoara = graph.create_node(location["Timisoara"])
Arad = graph.create_node(location["Arad"])
Zerind = graph.create_node(location["Zerind"])
Oradea = graph.create_node(location["Oradea"])


graph.insert_edge(Neamt, Iasi, 87)
graph.insert_edge(Iasi, Vaslui, 92)
graph.insert_edge(Vaslui, Urziceni, 142)
graph.insert_edge(Hirsova, Urziceni, 98)
graph.insert_edge(Hirsova, Eforie, 86)
graph.insert_edge(Bucharest, Urziceni, 85)
graph.insert_edge(Bucharest, Giurgiu, 90)
graph.insert_edge(Bucharest, Pitesti, 101)
graph.insert_edge(Craiova, Pitesti, 138)
graph.insert_edge(Bucharest, Fagaras, 211)
graph.insert_edge(Rimnicu_Vilcea, Pitesti, 97)
graph.insert_edge(Rimnicu_Vilcea, Craiova, 146)
graph.insert_edge(Sibiu, Fagaras, 99)
graph.insert_edge(Sibiu, Rimnicu_Vilcea, 80)
graph.insert_edge(Craiova, Drobeta, 120)
graph.insert_edge(Mehadia, Drobeta, 75)
graph.insert_edge(Mehadia, Lugoj, 70)
graph.insert_edge(Timisoara, Lugoj, 111)
graph.insert_edge(Timisoara, Arad, 118)
graph.insert_edge(Sibiu, Arad, 140)
graph.insert_edge(Zerind, Arad, 75)
graph.insert_edge(Zerind, Oradea, 71)
graph.insert_edge(Sibiu, Oradea, 151)


####################################### Number 2 #######################################
def get_average_time(func, sample, max_iteration=100):
    start = time()
    for i in range(max_iteration):
        func(random.sample(sample, 1)[0],
             random.sample(sample, 1)[0])
    return (time() - start)/max_iteration


search = Search(graph)
random_cities = random.sample(graph.nodes, 10)
iterations = [10, 20, 40, 60, 80, 100, 200, 400]
bfs_times = []
dfs_times = []
ucs_times = []
iterative_deepening_time = []
bi_directional_time = []
a_star_time = []
# uncomment this to see the chart


# for iteration in iterations:
#     bfs_times.append(get_average_time(search.BFS,random_cities, max_iteration=iteration))
#     dfs_times.append(get_average_time(search.DFS,random_cities, max_iteration=iteration))
#     ucs_times.append(get_average_time(search.UCS,random_cities, max_iteration=iteration))
#     iterative_deepening_time.append(get_average_time(
#         search.iterative_deepening,random_cities, max_iteration=iteration))
#     bi_directional_time.append(get_average_time(
#         search.bi_directional,random_cities, max_iteration=iteration))
#     a_star_time.append(get_average_time(search.Astar,random_cities, max_iteration=iteration))


# plt.plot(iterations, bfs_times, label="BFS")
# plt.plot(iterations, dfs_times, label="DFS")
# plt.plot(iterations, ucs_times, label="UCS")
# plt.plot(iterations, iterative_deepening_time, label="Iterative deepening")
# plt.plot(iterations, bi_directional_time, label="Bidirectional")
# plt.plot(iterations, a_star_time, color="#000000", label="A*")

# plt.xlabel("Number of Iterations")
# plt.ylabel("Average Time Taken")
# plt.title("Average Time taken by Search Alghorithms")

# plt.legend()
# plt.tight_layout()
# plt.show()


######################################### Creating 16 graphs #########################################
n_values = [10, 20, 30, 40]
p_values = [0.2, 0.4, 0.6, 0.8]
graphs = []

for n in n_values:
    for p in p_values:
        graph = Graph()
        for i in range(n):
            x = random.uniform(0, 180)
            y = random.uniform(0, 180)
            node = graph.create_node(
                {"name": n, "p": p, "Latitude": x, "Longitude": y})
        for i, node1 in enumerate(graph.nodes):
            for j, node2 in enumerate(graph.nodes):
                if i < j and random.random() < p:
                    graph.insert_edge(node1, node2)
        graphs.append(graph)

results = {}
for single_graph in graphs:
    nodes = random.sample(single_graph.nodes, 10)
    bfs_time = get_average_time(search.BFS, random_cities)
    dfs_time = get_average_time(search.DFS, random_cities)
    ucs_time = get_average_time(search.UCS, random_cities)
    iterative_deepening_time = get_average_time(
        search.iterative_deepening, random_cities)
    bi_directional_time = get_average_time(
        search.bi_directional, random_cities)
    a_star_time = get_average_time(search.Astar, random_cities)
    results[single_graph] = {"bfs": bfs_time, "dfs": dfs_time, "ucs": ucs_time,
                             "iterative": iterative_deepening_time, "bidirectional": bi_directional_time, "a*": a_star_time}


x = []
bfs = []
dfs = []
ucs = []
iter = []
bidir = []
astar = []
for result in results:
    n = result.nodes[1].value["name"]
    p = result.nodes[1].value["p"]
    x.append(f"n={n},p={p}")
    bfs.append(results[result]["bfs"])
    dfs.append(results[result]["dfs"])
    ucs.append(results[result]["ucs"])
    iter.append(results[result]["iterative"])
    bidir.append(results[result]["bidirectional"])
    astar.append(results[result]["a*"])

bfs = np.array(bfs)
dfs = np.array(dfs)
ucs = np.array(ucs)
iter = np.array(iter)
bidir = np.array(bidir)
astar = np.array(astar)

plt.bar(x, bfs, color="#1f77b4")
plt.bar(x, dfs, bottom=bfs, color="#ff7f0e")
plt.bar(x, ucs, bottom=bfs + dfs, color="#2ca02c")
plt.bar(x, iter, bottom=bfs + ucs + dfs, color="#d62728")
plt.bar(x, bidir, bottom=bfs + ucs + dfs + iter, color="#9467bd")
plt.bar(x, astar, bottom=bfs + ucs + dfs + bidir + iter, color="#8c564b")
plt.xlabel("Graph")
plt.ylabel("Time taken by the algorithm")
plt.legend(["BFS", "DFS", "UCS", "iterative deepening", "bi-directional", "A*"])
plt.xticks(fontsize=8, rotation=20)
plt.title("Time taken by each algorithm for different graphs")
plt.show()
