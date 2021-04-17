# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:49:00 2021

@author: Sara
"""

#This file is the pseudo code for variable ordering optimization for build BDD function

#Idea: Random shuffle. If we find the size is growing exponentially, then re-do random shuffle
def variable_ordering():
    Init subsetTable = empty table
    For each subsetIndex s:
        subsetTable[subsetIndex] = Number of covered points
    
    Sort subsetTable in decending order
    
    return subsetTable
    

