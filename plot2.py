#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:37:46 2018

@author: nozaki
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os # osモジュールのインポート
import numpy as np
from kenkyu_module import iv_module
import pandas as pd #pandasというデータ分析ライブラリを利用
import matplotlib.pyplot as plt #プロット用のライブラリを利用
from sklearn import cross_validation, preprocessing, decomposition #機械学習用のライブラリを利用
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
np.set_printoptions(threshold=np.inf)

roop_num = 100
iv_th = 0.6
tyouhuku_th = 10
anchor_th = 0.05
test_anchor_num = 1#評価したいアンカーのクラスタ番号の指定

mode = "single"
single_filename = "NHK1114"

wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/"
ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"

def main(speaker_name,ivpath):
    ivpath = "{0}{1}/".format(ivpath,speaker_name)
    
    anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor{1}.txt".format(speaker_name,test_anchor_num)
    
    ivmodule = iv_module(roop_num,iv_th,tyouhuku_th,anchor_th,ivpath,wavpath)
    
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
     
    print("anchor_num is:{}\n".format(anchor_num))
    
    #ivmodule.all_clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    queslist = ivmodule.clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num,test_anchor_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    
    #acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(ori_filelist,anslist,queslist)

    #print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    
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
    # 解説4：主成分分析を実施-------------------------------
    pca = decomposition.PCA(n_components=10)
    
    X_transformed = pca.fit_transform(X)
    #print(X_transformed)
    # 6: 結果をプロットする-----------------------------
    #matplotlib inline
    plt.figure(figsize=(5,5))
    plt.subplot(1, 1, 1)
    X = X_transformed[:,0]
    Y = X_transformed[:,1]
    
    clusters = 6
    
    ivlist = np.array(X_transformed)
    pred = KMeans(n_clusters=clusters).fit_predict(ivlist)
    X_1,Y_1 = [],[]
    
    cnt = [0]*clusters
    
    for i,item in enumerate(pred):
        cnt[item] += 1
    
    cnt = np.array(cnt)
    argcnt = cnt.argsort()[::-1]
    
    plt.title("scatter plot of 2-dimensional i-vector")
    colors = ["red","green","blue","magenta","orangered","yellow","cyan","lime","cornflowerblue","black","gray"]
    chart1,chart2 = [],[]
    for j in argcnt:
        chart1 = []
        X_1,Y_1 = [],[]
        for i,item in enumerate(ori_filelist):#図の重ねがけで使う
            if(pred[i]==j):
                chart1.append(i)
        for item in chart1:
            X_1.append(X[item])
            Y_1.append(Y[item])
        plt.scatter(X_1,Y_1,marker=".",c=colors[j])
    X_1,Y_1 = [],[]

    
    #plt.scatter(X_1,Y_1,marker="o",c="red")
    #plt.scatter(X_2,Y_2,marker="x",c="black")
    #plt.title("scatter plot of 2-dimensional i-vector")
    
    
    plt.grid(which='major',color='black',linestyle=':')
    #plt.scatter(X,Y,c=clus0or1)
    plt.xlabel('iv1')
    plt.ylabel('iv2')
    plt.legend()
    
if __name__ == '__main__':
    
    if(mode == "multi"):
        #ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/"
        
        f = open('/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/newslist.txt')
        lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        f.close()
        
        
        for line in lines2:
            line = line.replace("\n","")
            if(os.path.exists("{0}{1}".format(ivpath,line))):
                main(line,ivpath)
                print("\n")
                
    if(mode == "single"):
        main(single_filename,ivpath)