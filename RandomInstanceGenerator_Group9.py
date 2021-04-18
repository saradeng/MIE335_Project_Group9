#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def RandomInstanceGenerator(n,m,U,d):
    
    """
    Inputs:
    n = number of items to cover e.g. 7
    m = number of subsets e.g. 5
    U = max cost of subset
    d = probability for Bernoulli distribution, 0 < d <= 1
    
    Outputs:
    n
    m
    p = cost of each subset
    S = items contained in each subset
    """
        
    file = open("test.txt","w")
    
    # Line 1
    nString = str(n)
    file.writelines([nString,"\n"])
    
    # Line 2
    mString = str(m)
    file.writelines([mString,"\n"])
    
    # Line 3
    np.random.seed(29281) # COMMENT OUT TO LET IT RANDOMIZE
    p = np.random.randint(U,size=(m)) # costs of subsets e.g. [3,5,2,2,7] ARE THEY ONLY INTEGERS?
    pString = np.array2string(p,separator=',').replace(' ','').replace('\n','')
    file.writelines([pString,"\n"])
    
    
    # Make adjacency matrix
    
    A = np.empty((n,m), int) # adjacency matrix; refer to Lab 3

    for i in range(n): # for each item to cover
        for j in range(m): # for each subset
            A[i][j] = np.random.binomial(1, d) # is it covered
    
    for i in range(n): # for each item to cover
        x = 0
        for j in range(m): # count number of times i has been covered
            x = x + A[i][j]
        if x == 0: # if i has not been covered
            A[i][np.random.randint(m)] = 1 # cover it
    
    # Line 4
    
    file.write("[")
    for j in range(m): # for each subset
        if j > 0:
            #if np.sum(A,axis=0)[j-1] > 0:
            file.write(",") #separate this subset from previous subset
        for i in range(n): # for each item to cover
            if i == 0:
                #if np.sum(A,axis=0)[j] > 0:
                file.write("[") # start subset
            if A[i][j] == 1:
                file.write(str(i)) # add item to subset
                total = 0
                for a in range(len(A)-i-1): # count remaining items in this subset
                    total = total + A[a+i+1][j]
                if total > 0:
                    file.write(",") #separate this item from next item
        file.write("]") # end subset
    file.write("]")
    
    
    file.close()
    
    return


# In[3]:


# n = 10 # number of items to cover e.g. 7, 0 < n
# m = 10 # number of subsets e.g. 5, 0 < m
# U = 10 # max cost of subset, 0 < U < 2147483647 int32 max value
# d = 1 # probability for Bernoulli distribution, 0 < d <= 1

# n = 10
# m = 100
# U = 2147483647
# d = 0.5

# RandomInstanceGenerator(n,m,U,d)

