#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 13:50:04 2021

@author: m.daryalal
"""
import pandas as pd

filename = "Checkpoint4_instances/50_500_scpe1.txt"

df = pd.read_csv(filename, header=None, sep="\n")
[u_num, s_num, p, S] = df[0].apply(eval)
#u_num: num of points to be covered
#s_num: num of sets
#p: price for taking each set
#S: the sets
#print(S)
print(len(p))
print(len(S))