# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 20:23:44 2021

@author: Sara
"""

Function backtrace(startNode, cur_node):
    While cur_node != startNode:
        Add cur_node into optimal_path
    
    Return optimal_path

Function Astar(graph, startNode, endNode) return optimal_path:
    Set fringe To startNode
    
    while fringe is not empty:
    
        Set visited_dict to empty
        Sort the fringe based on the distance between each fringe node and the endNode
        Pop fringe[0] as cur_node
        
        Mark cur_node in visited_dict as True
        
        If cur_node is endNode Then:
            Call backtrace(startNode, cur_node) Return optimal_path
            Return optimal_path
        
        For all nodes i that connect to cur_node and NOT visited before:
            If i is in fringe:
                Calculate cost = g_cost of cur_node + arc cost
                if cost < g_cost of i:
                    Set g_cost of i to cost
            If i is not in fringe:
                Set g_cost of i = g_cost of cur_node + arc cost
                Add i into fringe
    Endwhile
Endfunction