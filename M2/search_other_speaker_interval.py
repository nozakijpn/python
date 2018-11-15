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

cnt = 0
th = float(sys.argv[1])
total = 0
sflag = 0
eflag = 0

pre = ""

path_list = glob.glob("/home/nozaki/newsdata/lbl/NHK*_v.lbl")
#f = open("/home/nozaki/newsdata/lbl/NHK0826_v.lbl","r")

for path in path_list:
    print(path)
    f = open(path,"r")
    times = []
    lines = f.readlines()
    flag = 0
    pre = ["","",""]
    eflag = 0

    for i,line in enumerate(lines):
        
        if(i>7):
            line = line.replace("\"","")
            line = line.replace(":","")
            sflag = 0

            if(line.find("_S") != -1):
                sflag = 1
            elif(line.find("_E") != -1):
                eflag += 1
            elif(line.find("<Voice>") != -1):
                break

            #print(sflag)
            line = re.sub("_S\w*","",line)
            line = re.sub("_E\w*","",line)
            line = re.sub("-\w*","",line)
            line = line.split()
            if(sflag == 1 and eflag%2 == 0):
                if(i!=8):
                    if(line[1]!=pre[1] and pre[1]!="121" and pre[1]!=""):
                        if(float(line[0])-float(pre[0])<10 and float(line[0])-float(pre[0])>0.1):
                            
                            print(pre[1],line[1])
                            """
                            print("\n")
                            print(path)
                            print(pre[2])
                            print(line[2])
                            
                            print(pre[2],line[2])
                            print(float(line[0])-float(pre[0]))
                            """
                            times.append(int(float(line[0])-float(pre[0])))
                            #print(float(line[0])-float(pre[0]))

                            total += 1

                            if(float(line[0])-float(pre[0])>th):
                                cnt += 1

            if(line[1]!="121"):
                pre = line
    f.close

print("\n")
print(total)
print(float(cnt)/total)

print("\n")
print(np.average(np.array(times)))
