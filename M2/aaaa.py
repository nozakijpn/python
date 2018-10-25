#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 15:45:11 2018

@author: nozaki
"""

import wave
import numpy as np

#filelist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
filelist = ["NHK0826","NHK1112","NHK1113"]
for filename in filelist:
    f = open("/home/nozaki/newsdata/kakiokoshi_txt/{}.txt".format(filename), "r")
    strings = f.readlines()
    
    wf = wave.open("/home/nozaki/newsdata/{}.wav".format(filename) , "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    print(time)
    time = time * 100
    print(int(time))
    
    timeline_ori = [0]*int(time)
    timeline_pred = [0]*int(time)
    print(np.array(timeline_ori).shape)
    
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        
        data[1] = float(data[1]) + float(data[0])
        data[0],data[1] = float(data[0]),float(data[1])
        data[0] = data[0] * 100
        data[1] = data[1] * 100
        data[0],data[1] = int(data[0]),int(data[1])
        
        for nowtime in range(data[0],data[1]+1):
            timeline_ori[nowtime] = 1
    
    f = open("/mnt/disk2/bati_dic/news/work2/nozaki_{}_sox.txt".format(filename), "r")
    print("/mnt/disk2/bati_dic/news/work2/nozaki_{}_sox.txt".format(filename))
    strings = f.readlines()
    for i,line in enumerate(strings):
        data = line.split()
        if(data[0]=="0"):
            break
        
        data[2],data[3] = float(data[2]),float(data[3])
        data[2] = data[2] * 100
        data[3] = data[3] * 100
        data[2],data[3] = int(data[2]),int(data[3])
        
        for nowtime in range(data[2],data[3]+1):
            timeline_pred[nowtime] = 1
            #print(data[3])
    """
    小島さんの実行結果(st,endのテキスト)を読み込む
    forで行のリストを回し、各行ごとに31行〜35行の処理を行う(enumerateでループ数も保持。これはアンカーのファイル名のリストを作成するときに使う)
        for i in range(st,end):でループを回す
            ifでtimeline[i]が1を含むとき、アンカーの発話であるとする(このとき、カウントアップを入れて、条件以上のときアンカーとする、とかでもいいかも)
            条件を満たしたとき、アンカーのリストに発話データの名前をf.writeで追加する(どこかでアンカーのリストのファイルを開く必要あり)
    
    
    """
    tp,tn,fp,fn = 0,0,0,0
    for i,ansflag in enumerate(timeline_ori):
        predflag = timeline_pred[i]        
        if(ansflag == 1 and predflag == 1):
            tp += 1
        if(ansflag == 0 and predflag == 1):
            fp += 1
        if(ansflag == 1 and predflag == 0):
            fn += 1
        if(ansflag == 0 and predflag == 0):
            tn += 1
    
    recall = float(tp/(tp+fn))
    precision = float(tp/(tp+fp))
    f_measure = float((2*recall*precision)/(recall + precision))
    
    print("recall:{}\nprecision:{}\nf-measure:{}".format(recall,precision,f_measure))
    f.close
