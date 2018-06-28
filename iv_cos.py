#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#ivのリストを取得し、標準偏差と分散を取得するプログラム

import os # osモジュールのインポート
import numpy as np
import wave
import glob 
import math

ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/"

def get_filelist(path):
# os.listdir('パス')
# 指定したパス内の全てのファイルとディレクトリを要素とするリストを返す
    filelist = []
    files = os.listdir('{0}'.format(path))
    for file in files:
        file = file.replace(".y","")
        filelist.append(file)
        
    filelist.sort()
    num = np.array(filelist).shape #file number
    num = num[0]
    filename = filelist[0]
    filename = filename.replace("_0001","")
    return filelist,num,filename

def threshold_time(path,filelist,num,timemin,timemax):
    timelist = []
    timelist_others = []
    for i in range(num):
        wf = wave.open("{0}{1}.wav".format(path,filelist[i]) , "r" )
        time = float(wf.getnframes()) / wf.getframerate()
        if(timemin < time and time < timemax):
            timelist.append(filelist[i])
        else:
            timelist_others.append(filelist[i])
    return timelist,timelist_others

def get_time(path,filename):
    #wavデータの時間情報取得
    wf = wave.open("{0}{1}.wav".format(path,filename) , "r" )
    time = float(wf.getnframes()) / wf.getframerate()

    return time

def get_ivdata(path,filename):
    f = open('{0}{1}.y'.format(path,filename))
    line = f.readline()
    line.replace(' ', ',')
    cnt = 0
    while line:
        if(cnt != 0):
            line = line.split(",")
            return line
        line = f.readline()
        cnt = cnt + 1
        line = line.replace(' ', ',')
    f.close
    print(line)
    return line

def calc_cos(iv1, iv2):
    """
    cos類似度を計算する関数
    @return cos類似度を計算した結果。0〜1で1に近ければ類似度が高い。
    """

    # iv1のベクトル長を計算
    length1 = 0.0
    for i in iv1:
        length1 += i*i
    
    length1 = math.sqrt(length1)

    # iv2のベクトル長を計算
    length2 = 0.0
    for i in iv2:
        length2 += i*i 
        
    length2 = math.sqrt(length2)
    
    # iv1とiv2の内積を計算
    iv3 = 0.0
    shape = iv1.shape
    for i in range(shape[0]):
        iv3 += iv1[i]*iv2[i]
    
    # cos類似度を計算
    cos = iv3 / (length1 * length2) 
    return cos

def main(speaker_name):
    ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/{0}/".format(speaker_name)
    wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/sph/"
    
    filelist,num,filename = get_filelist(ivpath)
    
    print("filename:{}".format(filename))
    
    #f = open("/home/nozaki/python/memo/{0}.txt".format(filename),"w")
    
    for item in filelist:
        for item2 in filelist:
            if(2<get_time(wavpath,item)):
                if(2<get_time(wavpath,item2)):
                    iv = get_ivdata(ivpath,item)
                    iv2 = get_ivdata(ivpath,item2)
                    
                    iv = np.array(iv)
                    iv = np.array(iv).astype(np.float)
                    iv2 = np.array(iv2)
                    iv2 = np.array(iv2).astype(np.float)
                    print("{0} {1} {2:9f} {3:2f} {4:4f} {5:4f}\n".format(item,item2,get_time(wavpath,item),get_time(wavpath,item2),
                          abs(get_time(wavpath,item) - get_time(wavpath,item2)),calc_cos(iv,iv2)))
    #f.close
     
     
if __name__ == '__main__':
    f = open('/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/A01name.txt')
    lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    
    for line in lines2:
        line = line.replace("\n","")
        if(os.path.exists("{0}{1}".format(ivpath,line))):
            main(line)
            print("\n")