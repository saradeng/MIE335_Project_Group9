#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:07:05 2021

Draw the graph representation of a BDD

@author: m.daryalal

install graphviz on MacOS: pip install graphviz 
install graphviz using Anaconda: conda install graphviz

"""

from graphviz import Digraph
#import os
#os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

# draw_graph takes as an argument a list of arcs, where an 
# arc is a 3d tuple: (source, destination, type)
def draw_graph(arcs):
    
    G = Digraph()
    
    styles = ["dashed",""]
    
    for arc in arcs:
        G.edge(str(arc[0]), str(arc[1]), style=styles[arc[2]], color="red")    
    
    G.view()
    
# BDD in the project description
# arcs = [(0,1,0),(0,2,1),(1,3,1),(2,4,0),(2,5,1),(3,6,1),(4,6,1),(5,6,0),(5,6,1)]

# BDD example in Checkpoint 2
arcs = [(0,1,0),(0,2,1),(1,3,1),(2,4,1),(3,5,0),(3,6,1),(4,7,0),(4,8,1),(5,9,1),
        (6,10,0),(6,11,1),(7,12,1),(8,12,1),(8,13,0),(9,14,1),(10,14,1),(11,14,1),
        (12,14,0),(12,14,1),(13,14,1)]

draw_graph(arcs)