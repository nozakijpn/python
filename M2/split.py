#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 14:37:59 2018

@author: nozaki
"""
output = open("soxprog.sh","w")
output.write("mkdir cutwav\n")
filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
for filename in filelist:
    output.write("mkdir cutwav/{}\n".format(filename))
    f = open("{}.txt".format(filename), "r")
    strings = f.readlines()
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        if(filename == "NHK0825" or filename == "NHK0826"):
            data[1] = float(data[1]) - float(data[0])
        #print("sox {}.wav cutwav/{}/{}_{}.wav trim {} {}".format(filename,filename,filename,str(i).zfill(4),data[0],round(float(data[1]),2)))
        output.write("sox {}.wav cutwav/{}/{}_{}.wav trim {} {}\n".format(filename,filename,filename,str(i).zfill(4),data[0],round(float(data[1]),2)))
        
    f.close
output.close()