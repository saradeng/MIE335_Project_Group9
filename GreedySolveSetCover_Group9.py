#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import math
import time


# In[2]:


def GreedySolveSetCover(filename):
    
    # TA's DataReader
    df = pd.read_csv(filename, header=None, sep="\n")
    [numItems, numSubsets, costs, sList] = df[0].apply(eval)
    
    A = np.zeros((numItems,numSubsets),int)
    for i in range(len(sList)):
        for j in sList[i]:
            A[j][i] = 1
    
    k = 1
    
    # Solve set cover problem
    
    #sets taken
    S = np.zeros((numSubsets,), dtype=int)
    #initializes as array of 0s of size j (number of columns in A)
    
    #number of times each element is covered
    ax = np.zeros((numItems,), dtype=int)
    #initializes as array of 0s of size i (number of rows in A)
    
    while np.amin(ax) < k:
        
        #initialize U very large
        U = math.inf
        
        #J stores j with minimum u_j; default to 0
        J = 0
        
        for j in range(len(S)):
        
            #skip sets that are already taken
            if S[j] == 1:
                continue
                
            #number of uncovered elements, including elements not covered enough times
            n = 0
            #initializes as 0
            
            for i in range(len(A)):
                if A[i][j] == 1:
                    if ax[i] < k:
                        n = n + 1
            
            if n > 0:
                u = costs[j]/n
            else:
                u = math.inf
            
            #select j that has minimum u_j
            if u < U:
                U = u
                J = j
        
        #update S
        S[J] = 1
        
        #update ax
        for i in range(len(A)):
            if A[i][J] == 1:
                ax[i] = ax[i] + 1
    
    z = 0
    for s in range(len(S)):
        z += S[s]*costs[s]
    
    return(z)


# In[3]:


# GreedySolveSetCover("test.txt")

