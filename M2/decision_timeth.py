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

for i in range(0,200,1):
    i = i*0.01

    cnt = 0
    th = i
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
    """
    print("\n")
    print(total)
    """
    samepercent = float(cnt)/total
    #print(np.average(np.array(times)))
    total = 0
    cnt = 0

    pre = ["","",""]
    for path in path_list:
        #print(path)
        f = open(path,"r")
        times = []
        lines = f.readlines()
        flag = 0
        pre = ["","",""]
        for i,line in enumerate(lines):
            sflag = 0
            if(i>7):
                line = line.replace("\"","")
                line = line.replace(":","")
                
                if(line.find("_S") != -1):
                    sflag = 1

                line = re.sub("_S\w*","",line)
                line = re.sub("_E\w*","",line)
                
                line = line.split()
                if(line[1]=="-1" and sflag == 1):
                    if(i!=8):
                        if(line[2]!=pre[2] and pre[1]=="-1"):

                            if(float(line[0])-float(pre[0])<10):
                                """
                                print("\n")
                                print(path)
                                print(pre[2])
                                print(line[2])
                                """
                                times.append(int(float(line[0])-float(pre[0])))
                                #print(float(line[0])-float(pre[0]))

                                total += 1

                                if(float(line[0])-float(pre[0])>th):
                                    cnt += 1

                if(line[1]=="-1"):
                    pre = line
        f.close
    #print("\n")
    #print(total)
    #print(float(cnt)/total)

    #print("\n")
    otherpercent = float(cnt)/total
    #print(samepercent,otherpercent)
    #print(np.average(np.array(times)))
    if(samepercent==0):
        samepercent = 0.00001
    if(otherpercent==0):
        otherpercent = 0.00001
    print("{},{}".format(str(round(th,2)),harmonic_mean(samepercent,otherpercent*5)))
    li.append(harmonic_mean(samepercent,otherpercent*5))

list_hm = np.array(li)
print(np.argmax(list_hm),np.max(list_hm))
