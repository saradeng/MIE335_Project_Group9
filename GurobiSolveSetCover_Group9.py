#!/usr/bin/env python
# coding: utf-8

# In[1]:


from gurobipy import *
import pandas as pd


# In[2]:


def GurobiSolveSetCover(filename):
    
    # TA's DataReader
    df = pd.read_csv(filename, header=None, sep="\n")
    [n, m, pList, sList] = df[0].apply(eval)
    
    # Create model and solve
    
    J = range(n)

    model = Model("model")
    
    x = model.addVars(m,lb=0,vtype=GRB.BINARY,name="x") #either take a set or don't
    model.setObjective(sum(pList[i]*x[i] for i in range(m)), GRB.MINIMIZE)

    model.addConstrs((sum(x[i] for i in range(m) if j in sList[i])>=1 for j in J),name="Constr")

    #m.write("set_covering.lp")
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        for v in model.getVars():
            print(v.varName, '=', v.x)


# In[3]:


# GurobiSolveSetCover("test.txt")

