#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
input
• inputfile (a .txt file that is properly formatted)
• method (1 for Gurobi, 2 for BDD)

output
(1) optimal value (i.e., the length of the shortest path),
(2) the total number of nodes and the total number of arcs in your non-reduced BDD and in your reduced BDD,
(3) the width of your non-reduced and reduced BDDs (the width is the maximum number of nodes in a layer),
(4) BDD construction time,
(5) BDD reduction time,
(6) solution time (i.e., the time the shortest path algorithm took), and
(7) total time, i.e., sum of (4),(5) and (6)
"""

from gurobipy import *
import pandas as pd
import math
import time

class BDD:
    
    def __init__(self, filename):
        
        self.filename = filename
        
        self.nodes = []
        self.unredNumNodes = int
        self.redNumNodes = int
        
        self.unredWidth = int
        self.redWidth = int
        
        self.arcs = []
        self.unredNumArcs = int
        self.redNumArcs = int
        
        self.numItems = int
        self.numSets = int
        self.p = []
        self.S = []
        
        self.path = []
        
        #Datastructures for path finding
        self.visited_dict = {}      #visited nodes
        self.g_cost = {}            #g_cost for each node
        self.node_layer_dict = {}   #Key: node, value: which layer the key is in
        self.parent = {}
        self.target_node = int
        
        self.build_time = float
        self.reduce_time = float
        self.solve_time = float
        
        self.total_time = float
    
    def __str__(self):
        return('str of BDD')
    
    def __repr__(self):
        return(str(self.path))
    
    def DataReader(self, filename):
        
        # TA's DataReader
        self.filename
        df = pd.read_csv(filename, header=None, sep="\n")
        [self.numItems, self.numSets, self.p, self.S] = df[0].apply(eval)
        
        return(self.numItems, self.numSets, self.p, self.S)
    
    def VariableOrdering(self, filename):
#         subsets = []
#         for s in self.S:
#             subsets.append(tuple(s))
#         set_cost = dict(zip(subsets,self.p))
#         self.S.sort(reverse=True,key=len)
#         for s in range(len(self.S)):
#             self.p[s] = set_cost[tuple(self.S[s])]
        zipped_lists = zip(self.S,self.p)
        sorted_pairs = sorted(zipped_lists,key=lambda x:x[0],reverse=True)
        tuples = zip(*sorted_pairs)
        self.S,self.p = [list(tuple) for tuple in  tuples]
    
    def BDDBuild(self, filename):
        
        build_start_time = time.time()
        
        # Convert lists to sets of items in each set
        for subsetIndex in range(self.numSets):
            self.S[subsetIndex] = set(self.S[subsetIndex])
        
        # Create root node
        layer = { # Create 0th layer of nodes
            0: {i for i in range(self.numItems)}
        }
        self.nodes.append(layer) # Add 0th layer of nodes
        self.visited_dict[0] = False
        self.g_cost[0] = math.inf
        self.node_layer_dict[0] = 0
        self.parent[0] = math.inf
        
        # Create nodes layer by layer
        u = 1 # first available node number
        
        # Determine remaining available items after each set
        remainItemsList = [] # Create empty list for sets
        remainItems = set() # Create empty set of remaining available items after the last set
        for subset in reversed(range(self.numSets)): # Iterate backwards from the last to the first set
            remainItems = remainItems.union(self.S[subset]) # Add items from the current set to the set of remaining available items
            remainItemsList.append(remainItems) # Append the new set of remaining items to the list
        
        for layerIndex in range(self.numSets-1):
            nextLayerNodes = {} # Create the next layer of nodes
            arcsToNextLayer = {} # Create arcs to the next layer
            
            remainItems = remainItemsList[self.numSets-2-layerIndex] # Get the set of remaining items after this layer
    
            for node in self.nodes[layerIndex].keys():
                for d in range(2):
                    if d == 0: # the set is not taken
                        newState = self.nodes[layerIndex][node] # state is unchanged
                    else: # d == 1, the set is taken
                        newState = self.nodes[layerIndex][node] - self.S[layerIndex] # remove items in current set from state
                    if newState.issubset(remainItems): # node is feasible
                        if newState in nextLayerNodes.values(): # next layer already has another node with the same state
                            v = list(nextLayerNodes.keys())[list(nextLayerNodes.values()).index(newState)]
                            arcsToNextLayer[(node,v,d)] = self.p[layerIndex]*d # create arc to that node
                        else: # next layer DOES NOT have a node with the same state
                            nextLayerNodes[u] = newState # create new node
                            self.visited_dict[u] = False
                            self.g_cost[u] = math.inf
                            self.node_layer_dict[u] = layerIndex + 1
                            self.parent[u] = math.inf
                            arcsToNextLayer[(node,u,d)] = self.p[layerIndex]*d # create arc to the new node
                            u += 1 # next available node number
            self.nodes.append(nextLayerNodes)
            self.arcs.append(arcsToNextLayer)
        
        # Create terminal node
        layer = { # Create last layer of nodes
            u: {}
        }
        self.visited_dict[u] = False
        self.g_cost[u] = math.inf
        self.node_layer_dict[u] = len(self.nodes)
        self.parent[u] = math.inf
        self.target_node = u
        self.nodes.append(layer) # Add last layer of nodes
        
        # Consider the x_n variable for the last layer of arcs
        arcsToTerminal = {}
        for node in self.nodes[self.numSets-1].keys():
            for d in range(2):
                if d == 0: # the set is not taken
                    newState = self.nodes[self.numSets-1][node] # state is unchanged
                else: # d == 1, the set is taken
                    newState = self.nodes[self.numSets-1][node] - self.S[self.numSets-1] # remove items in current set from state
                if newState == set(): # node is feasible
                    arcsToTerminal[(node,u,d)] = self.p[self.numSets-1]*d # create arc to the terminal

        self.arcs.append(arcsToTerminal) # append the layer of arcs
        
        # Performance
        self.build_time = time.time()-build_start_time
        
        self.unredNumNodes = 0
        self.unredWidth = 1
        for layer in self.nodes:
            layerNumNodes = len(layer)
            self.unredNumNodes += layerNumNodes
            self.unredWidth = max(self.unredWidth,layerNumNodes)
        
        self.unredNumArcs = 0
        for layer in self.arcs:
            self.unredNumArcs += len(layer)
        
        return(self.arcs,self.build_time,self.unredNumNodes,self.unredWidth,self.unredNumArcs)
    
    def BDDReduce(self, filename):
        
        reduce_start_time = time.time()
        
        for layerIndex in range(self.numSets):
            
            # Determine path from each node to the terminal
            paths = {}
            for arcsIndex in range(len(list(self.arcs[self.numSets-1-layerIndex].keys()))): # iterate through the arcs
                arcI = list(self.arcs[self.numSets-1-layerIndex].keys())[arcsIndex]
                uI,vI,dI = arcI
                if uI not in paths.keys(): # node was not yet added
                    paths[uI] = ((vI,dI)) # add the node and that path from it
                else: # node was already added
                    paths[uI] = (paths[uI],(vI,dI)) # add that path from the node
            # for each pair of nodes
            removed = set() # set of removed nodes to be skipped
            for path1 in range(len(list(paths.keys()))):
                if list(paths.keys())[path1] in removed: # if node was removed
                    continue
                for path2 in range(len(list(paths.keys()))-path1-1):
                    # if their paths are the same
                    if paths[list(paths.keys())[path1]] == paths[list(paths.keys())[path2+path1+1]]: # nodes have the same paths
                        removed.add(list(paths.keys())[path2+path1+1]) # add node to set of nodes to be skipped
                        # Merge u2 to u1
                        # get arc1 starting node
                        u1 = list(paths.keys())[path1]
                        # create arc2 tuple
                        u2 = list(paths.keys())[path2+path1+1]
                        if type(paths[list(paths.keys())[path2+path1+1]][0]) != tuple: # if that node has only one path from it
                            v2,d2 = paths[list(paths.keys())[path2+path1+1]]
                            arc2 = u2,v2,d2
                            # delete arc2
                            self.arcs[self.numSets-1-layerIndex].pop(arc2)
                        else: # that node has multiple paths from it
                            for arc2path in paths[list(paths.keys())[path2+path1+1]]:
                                v2,d2 = arc2path
                                arc2 = u2,v2,d2
                                # delete arc2
                                self.arcs[self.numSets-1-layerIndex].pop(arc2)
                        # redirect incoming arcs
                        for arcIndex in range(len(list(self.arcs[self.numSets-2-layerIndex].keys()))): # loop through previous layer of arcs
                            arc = list(self.arcs[self.numSets-2-layerIndex].keys())[arcIndex]
                            u,v,d = arc
                            if v == u2: # arc ends at node being removed
                                p = self.arcs[self.numSets-2-layerIndex][arc] # get price of set
                                arcRedirect = (u,u1,d) # create new arc
                                self.arcs[self.numSets-2-layerIndex].pop(arc) # remove old arc
                                self.arcs[self.numSets-2-layerIndex][arcRedirect] = p # add new arc
                        # delete v from self.nodes
                        self.nodes[self.numSets-1-layerIndex].pop(u2)
        
        # Performance
        self.reduce_time = time.time()-reduce_start_time
        
        self.redNumNodes = 0
        self.redWidth = 1
        for layer in self.nodes:
            layerNumNodes = len(layer)
            self.redNumNodes += layerNumNodes
            self.redWidth = max(self.redWidth,layerNumNodes)
        
        self.redNumArcs = 0
        for layer in self.arcs:
            self.redNumArcs += len(layer)
        
        return(self.arcs,self.reduce_time,self.redNumNodes,self.redWidth,self.redNumArcs)
    
    def Astar(self, filename):
        #Datastructures
        #n: number of nodes
        #e: number of arcs
        #Visited list: size n, indicates a arc is visited of not
        
        #Fringe: list of arcs that potentially will be visited next
        

        #cost: size n, list of cumulative cost from the start to current arc
        #parent: size n, list of parent for each arc
        
        solve_start_time = time.time()
        
        #Put the root node into the fringe
        fringe = [0]
        self.g_cost[0] = 0
        self.parent[0] = (0,0,0)
        optimal_path = []
        #If fringe is empty, terminate
        #Otherwise, keep looping
        while (len(fringe) > 0):
            #Pop-up current arc with the smallest cost, mark it in the visited list
            
            cur_node = fringe[0]
            for i in range(len(fringe) - 1):
                #Calculate the distance to the target
                cur_dist = len(self.arcs) - self.node_layer_dict[fringe[i]]
                next_dist = len(self.arcs) - self.node_layer_dict[fringe[i+1]]
                if ((self.g_cost[fringe[i]] + cur_dist) > (self.g_cost[fringe[i + 1]] + next_dist)):
                    # print("Swap")
                    cur_node = fringe[i + 1]
            
            fringe.remove(cur_node)
            self.visited_dict[cur_node] = True
            #If it is target, call backtrace path and terminate
            if (cur_node == self.target_node):
                while(self.parent[cur_node] != (0,0,0)):
                    optimal_path.append(self.parent[cur_node])
                    cur_node = self.parent[cur_node][0]
                #optimal_path.append(0)
                break
            
            #Get the current layer of current node
            cur_layer = self.node_layer_dict[cur_node]
            #Iterate all arcs in current layer
            for temp_arcs in self.arcs[cur_layer]:
                #If the arc's start node is cur_node
                if (temp_arcs[0] == cur_node):
                    #This arc is connected to cur_node
                    dest_node = temp_arcs[1]
                    arc_cost = self.arcs[cur_layer][temp_arcs]
                    #Check if adjacent nodes are in visited list
                    if(self.visited_dict[dest_node] == False):
                        #If dest node is in fringe 
                        if dest_node in fringe:
                            cost = self.g_cost[cur_node] + arc_cost
                            #If current cost is better, replace its cost and parent
                            if cost < self.g_cost[dest_node]:
                                self.g_cost[dest_node] = cost
                                self.parent[dest_node] = temp_arcs
                        #If not in fringe, update its cost and parent, put it into the fringe
                        else:
                            cost = self.g_cost[cur_node] + arc_cost
                            self.g_cost[dest_node] = cost
                            self.parent[dest_node] = temp_arcs
                            fringe.append(dest_node)
            #Find the next node by finding the smallest g(n) + h(n)
            #g(n) is the value from cost list
            #h(n) is the number of layers to the target
        self.path = optimal_path
        
        # Performance
        self.solve_time = time.time()-solve_start_time
        
#         print(self.S)
#         print(self.p)
#         print(self.nodes)
#         print(self.arcs)
#         print(optimal_path)
        return(optimal_path,self.solve_time)

def GurobiSolveSetCover(filename):
    
    # TA's DataReader
    df = pd.read_csv(filename, header=None, sep="\n")
    [n, m, pList, sList] = df[0].apply(eval)
    
    # Create model and solve
    
    start_time = time.time()
    
    J = range(n)

    model = Model("model")
    
    x = model.addVars(m,lb=0,vtype=GRB.BINARY,name="x") #either take a set or don't
    model.setObjective(sum(pList[i]*x[i] for i in range(m)), GRB.MINIMIZE)

    model.addConstrs((sum(x[i] for i in range(m) if j in sList[i])>=1 for j in J),name="Constr")

    #m.write("set_covering.lp")
    model.optimize()
    
    run_time = time.time()-start_time
    
    if model.status == GRB.OPTIMAL:
        for v in model.getVars():
            print(v.varName, '=', v.x)
        return(model.getObjective().getValue(),run_time)

def SolveSetCover(inputfile, method):
    
    if method == 1: # Gurobi
        return(GurobiSolveSetCover(inputfile))
    elif method == 2: # BDD
        #Create a BDDSolveSetCover instance
        solver = BDD(inputfile)
        solver.DataReader(inputfile)
        solver.VariableOrdering(inputfile)
        arcs1,build_time,unredNumNodes,unredWidth,unredNumArcs = solver.BDDBuild(inputfile)
        arcs2,reduce_time,redNumNodes,redWidth,redNumArcs = solver.BDDReduce(inputfile)
        
        path,solve_time = solver.Astar(inputfile)
        optimalValue = 0
        for arc in range(len(path)):
            optimalValue += arcs2[-arc-1][path[arc]]
        
        total_time = build_time+reduce_time+solve_time
        
        return(optimalValue,(unredNumNodes,unredNumArcs,redNumNodes,redNumArcs),(unredWidth,redWidth),build_time,reduce_time,solve_time,total_time)
    


# In[1]:


# lista = [['c','c','c'],['a'],['b','b']]
# listA = [['A'],['C','C','C'],['B','B']]
# zipped_lists = zip(lista,listA)
# # print(str(list(zipped_lists)))
# sorted_pairs = sorted(zipped_lists,key=lambda x:x[0],reverse=True)
# print(str(sorted_pairs))
# tuples = zip(*sorted_pairs)
# lista,listA = [list(tuple) for tuple in  tuples]
# print(lista)
# print(listA)

