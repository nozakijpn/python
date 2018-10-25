#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 15:45:11 2018

@author: nozaki
"""

import wave
import numpy as np
#filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
filelist = ["NHK0826"]
for filename in filelist:
    oldendtime = 0
    f = open("kakiokoshi_txt/{}.txt".format(filename), "r")
    strings = f.readlines()
    
    wf = wave.open("{}.wav".format(filename) , "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    time = time * 100
    timeline = [0]*int(time)
    #print(np.array(timeline).shape)
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        
        if(oldendtime != 0):
            data[1] = float(data[1]) + float(data[0])
            data[0],data[1] = float(data[0]),float(data[1])
            print("{} {} {}".format(i, i+1, data[0]-oldendtime))
        else:
            data[1] = float(data[1]) + float(data[0])
        oldendtime = float(data[1])
        
    
    """
    小島さんの実行結果(st,endのテキスト)を読み込む
    forで行のリストを回し、各行ごとに31行〜35行の処理を行う(enumerateでループ数も保持。これはアンカーのファイル名のリストを作成するときに使う)
        for i in range(st,end):でループを回す
            ifでtimeline[i]が1を含むとき、アンカーの発話であるとする(このとき、カウントアップを入れて、条件以上のときアンカーとする、とかでもいいかも)
            条件を満たしたとき、アンカーのリストに発話データの名前をf.writeで追加する(どこかでアンカーのリストのファイルを開く必要あり)
    """
    #print(timeline)
    f.close