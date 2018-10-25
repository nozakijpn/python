#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:37:59 2018

@author: nozaki
"""

#filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
filelist = ["NHK0826"]

for filename in filelist:
    output = open("{}.ref1".format(filename),"w")
    f = open("{}.txt".format(filename), "r")
    strings = f.readlines()
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break

        print("{}".format(data[2]))
        output.write("{}\n".format(data[2]))
        #output.write("sox {}.wav cutwav/{}/{}_{}.wav trim {} {}\n".format(filename,filename,filename,str(i).zfill(4),data[0],round(float(data[1]),2)))
        
    f.close
output.close()