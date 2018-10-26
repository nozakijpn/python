#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 15:45:11 2018

@author: nozaki

書き起こしテキストから得られたアンカーの発話区間とvdetの発話区間のマッチングを取るプログラム
"""

import wave
import numpy as np

basepath = "/home/nozaki/newsdata"
filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]

for filename in filelist:
    f = open("{}/kakiokoshi_txt/{}.txt".format(basepath,filename), "r")
    strings = f.readlines()
    
    #発話時間のプレスホルダーを作成(0.01秒単位)
    wf = wave.open("{}/wav/{}.wav".format(basepath,filename) , "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    time = time * 100
    timeline = [0]*int(time)
    timeline_pred = [0]*int(time)
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        
        data[1] = float(data[1]) + float(data[0])
        data[0],data[1] = float(data[0]),float(data[1])
        data[0] = data[0] * 100
        data[1] = data[1] * 100
        data[0],data[1] = int(data[0]),int(data[1])
        
        #f1 = open("{}/anchorlist/{}_anchor1.txt".format(basepath,filename), "r")
        f1 = open("{}/anchorlist/{}_allanchor.txt".format(basepath,filename), "r")
        anchor_data = f1.readlines()
        for item2 in anchor_data:
            item2 = int(item2)
            if(item2 == i+1):
                print(i+1)
                for nowtime in range(data[0],data[1]+1):
                    timeline[nowtime] = 1
        f1.close
    f.close

    f = open("{}/txt/vdet_txt/{}.txt".format(basepath,filename), "r")
    strings = f.readlines()
    
    output = open("{}/txt/vdet_txt/{}_all_anchorlist.txt".format(basepath,filename), "w")
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        
        data[2],data[3] = float(data[2]),float(data[3])
        data[2] = data[2] * 100
        data[3] = data[3] * 100
        data[2],data[3] = int(data[2]),int(data[3])
        
        cnt = 0
        for nowtime in range(data[2],data[3]+1):
            if(timeline[nowtime] == 1):
                cnt =+ 1
        if(cnt >= 1):
            output.write("{}_{:04d}\n".format(filename,i+1))
            print("{}_{:04d}".format(filename,i+1))
        f1.close
    f.close
    output.close
    #print(timeline)
