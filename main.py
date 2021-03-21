import numpy as np
import time
from math import gcd
import BDDSolveSetCover_Group9 as solver
from graphviz import Digraph

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

def main():
    arcs_dict, path = solver.BDDSolveSetCover("Checkpoint4_instances/example.txt")
    # arcs_dict, path = solver.BDDSolveSetCover("Checkpoint4_instances/50_500_scpe1.txt")
    # arcs_dict, path = solver.BDDSolveSetCover("Checkpoint4_instances/240_192_scpcyc06.txt")
    print(arcs_dict)
    print(path)
    draw_graph(arcs_dict, path)

if __name__ == "__main__":
    main()