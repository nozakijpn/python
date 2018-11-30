#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 16:25:28 2018

@author: nozaki
"""

print(__doc__)

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
import numpy as np
from kenkyu_module import iv_module
import pandas as pd #pandasというデータ分析ライブラリを利用
import matplotlib.pyplot as plt #プロット用のライブラリを利用
from sklearn import cross_validation, preprocessing, decomposition #機械学習用のライブラリを利用
from mpl_toolkits.mplot3d import Axes3D
np.set_printoptions(threshold=np.inf)
# #############################################################################
# Generate sample data
centers = [[1, 1], [-1, -1], [1, -1]]
"""
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5,
                            random_state=0)
print(labels_true)
"""

roop_num = 100
iv_th = 0.5
tyouhuku_th = 10
anchor_th = 0.05
test_anchor_num = 1#評価したいアンカーのクラスタ番号の指定

mode = "single"
single_filename = "NHK1114"

wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/"
ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"


def affinity_propagation(X):
    # #############################################################################
    # Compute Affinity Propagation
    af = AffinityPropagation(preference=-50).fit(X)
    
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_
    
    n_clusters_ = len(cluster_centers_indices)
    return labels,cluster_centers_indices

def main(speaker_name,ivpath):
    ivpath = "{0}{1}/".format(ivpath,speaker_name)
    
    anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor{1}.txt".format(speaker_name,test_anchor_num)
    
    ivmodule = iv_module(roop_num,iv_th,tyouhuku_th,anchor_th)
    
    filelist,num,filename = ivmodule.get_filelist(ivpath)#filelist:ループされていく毎に減っていくwavデータのリスト
    ori_filelist,ori_num,_ = ivmodule.get_filelist(ivpath)     #ori_filelist:クラスタ分けする全ての音声ファイル
    anslist = ivmodule.read_ansfile(anstxtpath)
    cluster = np.zeros(ori_num)
    all_anchor = []
    anchor_num = 0
    
    print("filename:{}".format(filename))
    
    for i in range(roop_num):
        num = ivmodule.cnt_filenum(filelist)
        tyouhuku = ivmodule.cnt_tyouhuku_num(ivpath,filelist)#リストにある音声ファイルのcos類似度による重複回数のリストを返す
        
        maxfile = filelist[np.argmax(tyouhuku)]#重複回数が最大となる音声ファイルを探し、

        th_list = ivmodule.get_thlist(ivpath,maxfile,filelist)#もっとも重複した音声ファイルが多い音声ファイルの重複したwavファイルのリストを返す
        
        tyouhukulist = ivmodule.get_tyouhukulist(ivpath,filelist,th_list)#重重したwavファイルのリストを返す

        lis = np.array(ivmodule.make_tyouhukulist(filelist,tyouhukulist,num))#重複回数が閾値以上のファイルのリストを返してnumpy.arrayに変換
        
        if((ivmodule.cnt_filenum(lis)/ori_num) < anchor_th):
            if(anchor_num == 0):
                anchor_num = i
            break
            
        for item in lis:
            delnum = ivmodule.search_filenum(ori_filelist,item,ori_num)
            cluster[delnum] = i+1#クラスタ分けされた音声ファイルにラベルを付ける
            filelist.remove(item)#クラスタ分けされた音声ファイルをリストから削除する
            all_anchor.append(item)
    
    #for plot program
    clus0or1 = []
    for item in ori_filelist:
        flag = 0
        for item2 in anslist:
            if(item == item2):
                clus0or1.append("1")
                flag = 1
                break
        if(flag == 0):
            clus0or1.append("0")
    clus0or1 = np.array(clus0or1)
    
    iv = []
    for item in ori_filelist:
        iv.append(ivmodule.get_ivdata(ivpath,item))

    chart1,chart2 = [],[]
    for i,item in enumerate(ori_filelist):#図の重ねがけで使う
        if(clus0or1[i]=="0"):
            chart1.append(i)
        else:
            chart2.append(i)
        
    df_wine_all = pd.DataFrame(iv)
    X=df_wine_all.iloc[0:].values
    
    # 3：データの整形-------------------------------------------------------
    sc=preprocessing.StandardScaler()
    sc.fit(X)
    X=sc.transform(X)
    #print(X)
    
    labels,center = affinity_propagation(X)
    clusnum = max(labels)+1
    print("a number of cluster is {0}".format(clusnum))
    
    print("center iv is")
    
    num = []    
    for item in range(clusnum):
        sub = 0
        for item2 in labels:
            if(item == item2):
                sub += 1
        num.append(sub)
    
    cluslist = []
    for i,item in enumerate(center):
        cluslist.append(ori_filelist[item])
        print(ori_filelist[item],labels[item],num[i])
        
    """
    for i,item1 in enumerate(cluslist):
        for j,item2 in enumerate(cluslist):                 
            print(item1,item2,iv)
    """
    

if __name__ == '__main__':
    import os
    if(mode == "multi"):
        #ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/"
        
        f = open('/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/newslist.txt')
        lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        f.close()
        
        
        for line in lines2:
            line = line.replace("\n","")
            if(os.path.exists("{0}{1}".format(ivpath,line))):
                X = main(line,ivpath)
                
    if(mode == "single"):
        X = main(single_filename,ivpath)
