#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import math

class BDD:
    
    def __init__(self, filename):
        
        # print("run init")
        self.filename = filename
        self.nodes = []
        self.arcs = []
        self.numItems = int
        self.numSets = int
        self.p = []
        self.S = []
        
        #Datastructures for path finding
        self.visited_dict = {}      #visited nodes
        self.g_cost = {}            #g_cost for each node
        self.node_layer_dict = {}   #Key: node, value: which layer the key is in
        self.parent = {}
        self.target_node = int
        
        # self.DataReader(filename)
        # self.BDDBuild(filename)
        # self.BDDReduce(filename)
        # self.Algorithm(filename)
    
    def __str__(self):
        return('str of BDD')
    
    def __repr__(self):
        return(str(self.arcs))
    
    def DataReader(self, filename):
        # print("run DataReader")
        
        # TA's DataReader
        self.filename
        df = pd.read_csv(filename, header=None, sep="\n")
        [self.numItems, self.numSets, self.p, self.S] = df[0].apply(eval)
        
        return(self.numItems, self.numSets, self.p, self.S)
        
    def BDDBuild(self, filename):
        # print("run BDDBuilder")
        
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
#         self.arcs.append({}) # Create and add 0th layer of arcs
        
        # Create nodes layer by layer
        u = 1 # first available node number
        
        remainItemsList = []
        remainItems = set()
        for subset in reversed(range(self.numSets)):
            remainItems = remainItems.union(self.S[subset])
            remainItemsList.append(remainItems)
        
        for layerIndex in range(self.numSets-1):
            nextLayerNodes = {} # Create the next layer of nodes
            arcsToNextLayer = {} # Create arcs to the next layer
            
            remainItems = remainItemsList[self.numSets-2-layerIndex]
    
            for node in self.nodes[layerIndex].keys():
                for d in range(2):
#                     print("layerIndex="+str(layerIndex)+" node="+str(node)+" d="+str(d))
                    if d == 0:
                        newState = self.nodes[layerIndex][node]
                    else: # d == 1
                        newState = self.nodes[layerIndex][node] - self.S[layerIndex]
#                     print(d,newState,remainItems)
                    if newState.issubset(remainItems):
                        if newState in nextLayerNodes.values():
                            # v = nextLayerNodes.keys[nextLayerNodes.values().index(newState)]
                            v = list(nextLayerNodes.keys())[list(nextLayerNodes.values()).index(newState)]
                            arcsToNextLayer[(node,v,d)] = self.p[layerIndex]*d
                            # print((node,v,d))
                            
                        else:
                            nextLayerNodes[u] = newState
                            self.visited_dict[u] = False
                            self.g_cost[u] = math.inf
                            self.node_layer_dict[u] = layerIndex + 1
                            self.parent[u] = math.inf
                            arcsToNextLayer[(node,u,d)] = self.p[layerIndex]*d
                            # print((node,u,d))
                            u += 1 # next available node number
#                     print(self.nodes)
#                     print(self.arcs)
            self.nodes.append(nextLayerNodes)
            self.arcs.append(arcsToNextLayer)
        
        # Create terminal node
        layer = { # Create last layer of nodes
            u: {}
        }
        #print(u)
        self.visited_dict[u] = False
        self.g_cost[u] = math.inf
        # print(self.nodes)
        self.node_layer_dict[u] = len(self.nodes)
        self.parent[u] = math.inf
        self.target_node = u
        self.nodes.append(layer) # Add last layer of nodes
        
        # Consider the x_n variable
        arcsToTerminal = {}
#         print(self.nodes[self.numSets-1].keys())
        for node in self.nodes[self.numSets-1].keys():
            for d in range(2):
#                 print("node="+str(node)+" d="+str(d))
                if d == 0:
                    newState = self.nodes[self.numSets-1][node]
                else:
                    newState = self.nodes[self.numSets-1][node] - self.S[self.numSets-1]
#                 print(newState,newState=={})
                if newState == set():
                    arcsToTerminal[(node,u,d)] = self.p[self.numSets-1]*d
                    # print((node,u,d))

#                 print(self.nodes)
#                 print(self.arcs)
#         self.nodes.append(nextLayerNodes)
#         print(arcsToTerminal)
        self.arcs.append(arcsToTerminal)
        # print("nodes are: ", self.nodes)
        # print(self.arcs)
        # print(len(self.arcs))
        # print(self.visited_dict)
        # print(self.g_cost)
        # print(self.node_layer_dict)
        # print(self.parent)
        return(self.arcs)
    
    def BDDReduce(self, filename):
        # print("run BDDReducer")
        for layerIndex in range(self.numSets):
#             print(self.arcs[self.numSets-1-layerIndex])
            numArcsFromU = {}
            potentialMatch = set() # have at least 1 arc in common
            for arc1index in range(len(list(self.arcs[self.numSets-1-layerIndex].keys()))):
                arc1 = list(self.arcs[self.numSets-1-layerIndex].keys())[arc1index]
                u1,v1,d1 = arc1
                if u1 not in numArcsFromU.keys():
                    numArcsFromU[u1] = 1
                else:
                    numArcsFromU[u1] = 2
                for arc2index in range(len(list(self.arcs[self.numSets-1-layerIndex].keys()))-arc1index-1):
                    arc2 = list(self.arcs[self.numSets-1-layerIndex].keys())[arc1index+arc2index+1]
                    u2,v2,d2 = arc2
#                     print(arc1,arc2)
                    if (v1 == v2) and (d1 == d2):
                        potentialMatch.add((arc1,arc2))
#             print(potentialMatch)
            for pair in potentialMatch:
                arc1,arc2 = pair
                u1,v1,d1 = arc1
                u2,v2,d2 = arc2
                if numArcsFromU[u1] == numArcsFromU[u2]:
#                     print("match")
#                     print(u1,u2)
                    # Merge u2 to u1
                    self.arcs[self.numSets-1-layerIndex].pop(arc2) # delete arc2
                    # redirect incoming arcs. CHECK if index might get out of bounds in some cases
                    for arcIndex in range(len(list(self.arcs[self.numSets-2-layerIndex].keys()))):
                        arc = list(self.arcs[self.numSets-2-layerIndex].keys())[arcIndex]
                        u,v,d = arc
                        if v == u2:
                            p = self.arcs[self.numSets-2-layerIndex][arc]
                            arcRedirect = (u,u1,d)
                            self.arcs[self.numSets-2-layerIndex].pop(arc)
                            self.arcs[self.numSets-2-layerIndex][arcRedirect] = p
                    # delete v from self.nodes
                    self.nodes[self.numSets-1-layerIndex].pop(u2)
        
        # print(self.nodes)
        # print(self.arcs)
        return(self.arcs)
    
    def Astar(self, filename):
        # print("run Algorithm")
        #Datastructures
        #n: number of nodes
        #e: number of arcs
        #Visited list: size n, indicates a arc is visited of not
        
        #Fringe: list of arcs that potentially will be visited next
        

        #cost: size n, list of cumulative cost from the start to current arc
        #parent: size n, list of parent for each arc
        
        #Put the root node into the fringe
        fringe = [0]
        self.g_cost[0] = 0
        self.parent[0] = (0,0,0)
        # print(self.g_cost)
        # print("target node is: ", self.target_node)
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
            
            print("Visiting: ", cur_node)
            # print(fringe)
            # print(self.g_cost)
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
        # print(optimal_path)
        return optimal_path
        
def BDDSolveSetCover(filename):
     print("run BDDSolveSetCover")
     #Create a BDDSolveSetCover instance
     solver = BDD(filename)
     solver.DataReader(filename)
     solver.BDDBuild(filename)
     arcs = solver.BDDReduce(filename)
     path = solver.Astar(filename)
     return arcs, path


# In[ ]:




