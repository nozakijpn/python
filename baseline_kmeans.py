#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:57:52 2018

@author: nozaki
"""

#adachi's clustering program

import os # osモジュールのインポート
import numpy as np
from kenkyu_module import iv_module
import math 
np.set_printoptions(threshold=np.inf)

def get_ivdata(path,filename):
    #ファイル名を指定してivのリストを返す
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
    return line
    
def calc_cos(ivpath,ivfile1, ivfile2):
    """
    cos類似度を計算する関数
    @return cos類似度を計算した結果。0〜1で1に近ければ類似度が高い。
    入力はyファイルのファイル名
    """
    iv1 = get_ivdata(ivpath,ivfile1)
    iv2 = get_ivdata(ivpath,ivfile2)
    
    iv1 = np.array(iv1)
    iv1 = np.array(iv1).astype(np.float)
    iv2 = np.array(iv2)
    iv2 = np.array(iv2).astype(np.float)
    
    length1 = 0.0
    for i in iv1:
        length1 += i*i
    
    length1 = math.sqrt(length1)

    length2 = 0.0
    for i in iv2:
        length2 += i*i 
        
    length2 = math.sqrt(length2)

    iv3 = 0.0
    shape = iv1.shape
    for i in range(shape[0]):
        iv3 += iv1[i]*iv2[i]
    
    # cos類似度を計算
    cos = iv3 / (length1 * length2) 
    return cos

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

def k_medoidos(ivpath,filelist):
    miniv = 1
    for item1 in filelist:
        for item2 in filelist:
            iv = calc_cos(ivpath,item1,item2)
            if(iv < miniv):
                miniv = iv
                minitem1 = item1
                minitem2 = item2
    return miniv,minitem1,minitem2

def mksubclus(ivpath,filelist,minitem1,minitem2):
    sub_cluster1,sub_cluster2 = [],[]
    for item1 in filelist:
        iv1 = calc_cos(ivpath,item1,minitem1)
        iv2 = calc_cos(ivpath,item1,minitem2)
        if(iv1>=iv2):
            sub_cluster1.append(item1)
        else:
            sub_cluster2.append(item1)
    return sub_cluster1,sub_cluster2

def better_clus(sub_cluster1,sub_cluster2):
    if(len(sub_cluster1)>=len(sub_cluster2)):
        cluster1 = sub_cluster1
        cluster2 = sub_cluster2
    else:
        cluster2 = sub_cluster1
        cluster1 = sub_cluster2
    return cluster1,cluster2

def better_clus2(minitem1,minitem2,sub_cluster1,sub_cluster2):
    sum_iv1,sum_iv2 = 0,0
    for item in sub_cluster1:
        sum_iv1 += calc_cos(ivpath,item,minitem1)
    for item in sub_cluster2:
        sum_iv2 += calc_cos(ivpath,item,minitem2)
    sum_iv1 = sum_iv1/float(len(sub_cluster1))
    sum_iv2 = sum_iv2/float(len(sub_cluster2))
    
    if(sum_iv1 > sum_iv2):
        cluster1 = sub_cluster1
        cluster2 = sub_cluster2
    else:
        cluster2 = sub_cluster1
        cluster1 = sub_cluster2
    return cluster1,cluster2

def test(self,ori_filelist,anslist,queslist):
    tp,tn,fp,fn = 0,0,0,0
    for item in ori_filelist:
        ansflag = self.search_file(anslist,item)
        quesflag = self.search_file(queslist,item)
        
        if(ansflag == 1 and quesflag == 1):
            tp += 1
        if(ansflag == 0 and quesflag == 1):
            fp += 1
        if(ansflag == 1 and quesflag == 0):
            fn += 1
        if(ansflag == 0 and quesflag == 0):
            tn += 1
        
    print("tp:{0} tn:{1} fp:{2} fn:{3}".format(tp,tn,fp,fn))
        
    acc = (tp+tn)/(tp+tn+fp+fn)
        
    recall = float(tp/(tp+fn))
        
    precision = float(tp/(tp+fp))
        
    if(recall + precision == 0):
        print("Error ansclusterとquesclusterのリストが完全不一致です。")
        return 0,0,0,0
    
    f_measure = float((2*recall*precision)/(recall + precision))
    
    return acc,recall,precision,f_measure

def all_anc(num,allanchor,addclus):
    if(np.array(addclus).shape[0]/num > 0.05):
        allanchor.extend(addclus)
    return allanchor

#single_filename = "NHK1114"
filename = ["NHK0826","NHK1112","NHK1113","NHK1114"]
#filename = ["NHK1112","NHK1114"]
calclist = []
time_th = 1
anchor_num = 1
clusters = 5
import sys
print("clusnum,acc,recall,precision,f-measure")
if(anchor_num == 1):
    filename = ["NHK0826","NHK1112","NHK1113","NHK1114"]
else:
    filename = ["NHK1112","NHK1114"]
for roop,single_filename in enumerate(filename):
    print(single_filename)
    cluster1,cluster2,cluster3,cluster4,cluster5 = [],[],[],[],[]
    sub_cluster1,sub_cluster2 = [],[]
    wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/"
    ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/{0}/".format(single_filename)
    
    ivmodule = iv_module(100,0.6,10,10,ivpath,wavpath)
    filelist,num,filename = get_filelist(ivpath)
    all_anchor = []
    ori_filelist,ori_num = ivmodule.timecut(wavpath,filelist,time_th)
    filelist,num = ivmodule.timecut(wavpath,filelist,time_th)
    
    from sklearn.cluster import KMeans
    ivlist = []
    for item in ori_filelist:
        ivlist.append(ivmodule.get_ivdata(ivpath,item))

    ivlist = np.array(ivlist)
    pred = KMeans(n_clusters=clusters).fit_predict(ivlist)
    cnt = [0]*clusters
        
    for i,item in enumerate(pred):
        cnt[item] += 1
    
    cnt = np.array(cnt)
    argcnt = cnt.argsort()[::-1]
    
    anclist = []
    for i,item in enumerate(pred):
        if(argcnt[anchor_num-1]==item):
            anclist.append(ori_filelist[i])
    
    #print(single_filename)
    #print("1")
    anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor{1}.txt".format(single_filename,anchor_num)
    anslist = ivmodule.read_ansfile(anstxtpath)
    acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(filelist,anslist,anclist)
    #print("{},{},{},{},{}".format(clusters,acc*100,recall*100,precision*100,f_measure*100))
    if(tp == 0): 
        print("retry")
        sys.exit()
    for item in [tp,tn,fp,fn]:
        calclist.append(item)
    if(single_filename == "NHK1112" or single_filename == "NHK1114"):
        anclist = []
        for i,item in enumerate(pred):
            if(argcnt[anchor_num]==item):
                anclist.append(ori_filelist[i])
                
        anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor{1}.txt".format(single_filename,anchor_num+1)
        anslist = ivmodule.read_ansfile(anstxtpath)
        acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(filelist,anslist,anclist)
        #print("{},{},{},{},{}".format(clusters,acc*100,recall*100,precision*100,f_measure*100))
        if(tp == 0):
            print("retry")
            sys.exit()
        for item in [tp,tn,fp,fn]:
            calclist.append(item)
    #print("{},{},{},{}".format(acc,recall,precision,f_measure))

    #print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    """
    anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/all_anchor.txt".format(single_filename)
    anslist = ivmodule.read_ansfile(anstxtpath)
    acc,recall,precision,f_measure = ivmodule.test(filelist,anslist,all_anchor)
    #print("{},{},{},{}".format(acc,recall,precision,f_measure))
    print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    """
calclist = np.array(calclist)
calclist = np.reshape(calclist,(6,4))
#print(calclist)
calc = np.sum(calclist,0)
tp = calc[0]
tn = calc[1]
fp = calc[2]
fn = calc[3]
acc = (tp+tn)/(tp+tn+fp+fn)
recall = float(tp/(tp+fn))      
precision = float(tp/(tp+fp))
f_measure = float((2*recall*precision)/(recall + precision))
print("{},{},{},{},{}".format(clusters,acc*100,recall*100,precision*100,f_measure*100))
#print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    

    