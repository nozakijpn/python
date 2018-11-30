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
#th = float(sys.argv[1])
total = 0
sflag = 0
eflag = 0

pre = ""
path_base = "/home/nozaki/newsdata/lbl/"
path_list = glob.glob("{}NHK*_v.lbl".format(path_base))
path_save = "/home/nozaki/tooltxt"
#f = open("/home/nozaki/newsdata/lbl/NHK0826_v.lbl","r")

for path in path_list:
    f = open(path,"r")
    path_sub = path.replace(path_base,"")
    fout = open("{}/{}".format(path_save,path_sub),"w")
    times = []
    lines = f.readlines()
    flag = 0
    pre = ["","",""]
    eflag = 0
    spname1,spname2 = "",""
    s1,s2 = 0,0
    sflag,eflag = 0,0
    for i,line in enumerate(lines):
        
        if(i>7):
            line = line.replace("\"","")
            line = line.replace(":","")

            if(line.find("_S") != -1):
                sflag = 1
            elif(line.find("_E") != -1):
                eflag = 1
            elif(line.find("<Voice>") != -1):
                break
            else:
                sflag,eflag = 0,0


            #print(sflag)
            line = re.sub("_S\w*","",line)
            line = re.sub("_E\w*","",line)
            line = re.sub("-\w*","",line)
            line = line.split()
            if(not spname1 and sflag):
                spname1 = line[1]
                s1 = float(line[0])
            elif(spname1 and sflag):
                spname2 = line[1]
                s2 = float(line[0])

            if(spname1==line[1] and eflag):
                print("{} {} {}".format(s1,line[0],line[1]))
                fout.write("{} {} {}\n".format(s1,line[0],line[1]))
                spname1 = ""
            elif(spname2==line[1] and eflag):
                print("{} {} {}".format(s2,line[0],line[1]))
                fout.write("{} {} {}\n".format(s2,line[0],line[1]))
                spname2 = ""
        sflag,eflag = 0,0
    f.close
"""
print("\n")
print(total)
print(float(cnt)/total)

print("\n")
print(np.average(np.array(times)))
"""