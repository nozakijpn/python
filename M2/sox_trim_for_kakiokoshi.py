#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:42:24 2018

@author: nozaki
"""

basepath = "/home/nozaki/newsdata"
savedic = "{}/cutwav/kakiokoshi_wav".format(basepath)
filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
#filelist = ["NHK1114"]

output = open("{}/sox_trim_for_kakiokoshi.sh".format(basepath), "w")

for filename in filelist:
    f = open("{}/kakiokoshi_txt/{}.txt".format(basepath,filename), "r")
    strings = f.readlines()
    
    for i,line in enumerate(strings):
        print(line)
        data = line.split()
        if(data[0]=="0"):
            break
        
        data[0],data[1] = float(data[0]),float(data[1])
    
        output.write("sox {}.wav {}/{}_{:04d}.wav trim {} {}\n".format(filename,savedic,filename,i+1,data[0],data[1]))