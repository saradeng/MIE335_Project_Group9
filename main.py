import numpy as np
import time
from math import gcd
import BDDSolveSetCover_Group9 as solver
import RandomInstanceGenerator_Group9 as RIG
from graphviz import Digraph
import matplotlib.pyplot as plt

# draw_graph takes as an argument a list of arcs, where an 
# arc is a 3d tuple: (source, destination, type)
def draw_graph(arcs_dict, path):
    
    G = Digraph()
    
    styles = ["dashed",""]
    
    for i in range(len(arcs_dict)):
        for arc in arcs_dict[i]:
            if arc in path:
                G.edge(str(arc[0]), str(arc[1]), style=styles[arc[2]], color="red", label=str(arcs_dict[i][arc]))    
            else:
                G.edge(str(arc[0]), str(arc[1]), style=styles[arc[2]], color="black", label=str(arcs_dict[i][arc]))    
    
    G.view()

def plot_graph(n):
    d = 0.5
    mean_times = []
    max_times = []
    astar_mean_times = []
    astar_max_times = []
    for i in range(2, n+1):
        print(i)
        times_n = []
        astar_times_n = []
        for j in range(10):
            U = 10
            m = 10 * i
            RIG.RandomInstanceGenerator(i,m,U,d)
            start = time.time()
            arcs_dict, path, astar_time = solver.BDDSolveSetCover("test.txt")
            end = time.time()
            elapsed_time = end - start
            times_n.append(elapsed_time)
            astar_times_n.append(astar_time)
            
        #Calculate mean and max for times_n
        mean = sum(times_n) / len(times_n)
        mean_times.append(mean)
        max_times.append(max(times_n))
        mean = sum(astar_times_n) / len(astar_times_n)
        astar_mean_times.append(mean)
        astar_max_times.append(max(astar_times_n))
        
        
    
    plt.plot(range(2, n+1), mean_times, "-b", label="mean time")
    plt.plot(range(2, n+1), max_times, "-r", label="max time")
    plt.legend(loc="upper left")
    plt.xlabel("size (n)")
    plt.ylabel("mean/max elapsed time for each n")
    plt.show()
    
    plt.plot(range(2, n+1), astar_mean_times, "-b", label="astar mean time")
    plt.plot(range(2, n+1), astar_max_times, "-r", label="astar max time")
    plt.legend(loc="upper left")
    plt.xlabel("size (n)")
    plt.ylabel("mean/max elapsed time for each n")
    plt.show()
    
    
def main():
    plot_graph(5)
    
if __name__ == "__main__":
    main()