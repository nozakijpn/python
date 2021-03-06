#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 11:52:01 2018

@author: nozaki
"""

import re
import numpy as np
import glob
import sys
from scipy import stats
li = []
def harmonic_mean(x,y):
    return 2/((1/x)+(1/y))

cnt = 0
th = 0
total = 0
pre = ""

path_list = glob.glob("/home/nozaki/newsdata/lbl/NHK*_v.lbl")
#f = open("/home/nozaki/newsdata/lbl/NHK0826_v.lbl","r")
pre = ["","",""]

for path in path_list:
    #print(path)
    f = open(path,"r")
    times = []
    lines = f.readlines()
    flag = 0
    for i,line in enumerate(lines):
        sflag = 0
        if(i>7):
            line = line.replace("\"","")
            line = line.replace(":","")
            
            if(line.find("_S") != -1):
                sflag = 1
                #print(line)

            line = re.sub("_S\w*","",line)
            line = re.sub("_E\w*","",line)
            
            line = line.split()
            if(line[1]=="-1" and sflag == 1):
                if(i!=8):
                    if(line[2]==pre[2] and pre[1]=="-1" and float(line[0])-float(pre[0]) > 0):
                        times.append(int(float(line[0])-float(pre[0])))
                        """
                        print("\n")
                        print(pre[2])
                        print(line[2])
                        print(float(line[0])-float(pre[0]))
                        """
                        total += 1
                        if(float(line[0])-float(pre[0])<th):
                            cnt += 1

            if(line[1]=="-1"):
                pre = line    
    f.close

print("\n")
print(total)
print(cnt)
samepercent = float(cnt)/total
print(samepercent)
#print(np.average(np.array(times)))
