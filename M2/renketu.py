#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 10:37:05 2018

@author: nozaki
"""

import glob
import re
path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/balance"
wavlist = glob.glob("{}/*".format(path))
output = open("{}/../renketu.sh".format(path),"w")

wavlist2 = []
for item in wavlist:
    item = re.sub("{}/".format(path),"",item)
    item = re.sub(".{17}$","",item)
    wavlist2.append(item)

wavlist = list(set(wavlist2))
wavlist.sort()


for item in wavlist:
    cnt = 0
    mix = []
    cntfile = 0
    itemlist = glob.glob("{}/{}*".format(path,item))
    #itemlist = glob.glob("{}/{}*".format(path,"JM001"))
    for i,item2 in enumerate(itemlist):
        mix.append(item2)
        cnt += 1
        if(cnt == 5):
            output.write("sox ")
            for item3 in mix:
                output.write("{} ".format(item3))
            output.write("../renketu_balance/{}_{}.wav\n".format(item,cntfile))
            mix = []
            cnt = 0
            cntfile += 1
        
    
        