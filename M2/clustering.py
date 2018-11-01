#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os # osモジュールのインポート
import numpy as np
from kenkyu_module import iv_module
np.set_printoptions(threshold=np.inf)
import glob
import sys

args = sys.argv

roop_num = 100
iv_th = float(args[1])
tyouhuku_th = 20
anchor_th = 0.05
test_anchor_num = 1#評価したいアンカーのクラスタ番号の指定
ques_anchor_cluster_num = 1#評価したいアンカーのクラスタ番号
time_th = 1
search_mode = "all_anchor"#if you want to calculate that search acc of all anchor ,write "all_anchor".
mode = "multi"#single or multi
single_filename = "NHK1112"

wavpath = "/home/nozaki/newsdata/cutwav/vdet_wav/"
ivpath = "/home/nozaki/speaker_clustering/news_i-vector/iv/raw/"

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]

print("iv_th : {}".format(iv_th))

if(mode=="single"):
    newslist = [single_filename]
calclist = []
f_measurelist = []
#def main(speaker_name,ivpath):
for speaker_name in newslist:
    print(speaker_name)
    #print(iv_th)
    #ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"
    #ivpath = "{0}{1}/".format(ivpath,speaker_name)
    
    anstxtpath = "/home/nozaki/newsdata/txt/vdet_txt/{0}_anchorlist.txt".format(speaker_name)
    if(search_mode == "all_anchor"):
        anstxtpath = "/home/nozaki/newsdata/txt/vdet_txt/{0}_all_anchorlist.txt".format(speaker_name)#if all anchor search
    
    ivmodule = iv_module(roop_num,iv_th,tyouhuku_th,anchor_th,ivpath,wavpath)
    
    #filelist,num,filename = ivmodule.get_filelist(ivpath)#filelist:ループされていく毎に減っていくwavデータのリスト
    #ori_filelist,ori_num,_ = ivmodule.get_filelist(ivpath)     #ori_filelist:クラスタ分けする全ての音声ファイル
    
    filelist,ori_filelist = [],[]
    fil = glob.glob("{}/{}*.y".format(ivpath,speaker_name))
    fil.sort()
    for item in fil:
        item = item.replace(ivpath,"")
        item = item.replace(".y","")
        filelist.append(item)
        ori_filelist.append(item)
    num = len(filelist)
    ori_num = len(filelist)
    filename = speaker_name
    
    anslist = ivmodule.read_ansfile(anstxtpath)
    cluster = np.zeros(ori_num)
    all_anchor = []
    anchor_num = 0
    
    ori_filelist,ori_num = ivmodule.timecut(wavpath,ori_filelist,time_th)
    filelist,num = ivmodule.timecut(wavpath,ori_filelist,time_th)
    
    
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
     
    
    print(anchor_num)
    """
    #ivmodule.all_clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    queslist = ivmodule.clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num,ques_anchor_cluster_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(ori_filelist,anslist,queslist)
    f_measurelist.append(f_measure)
    #print("{},{},{},{}".format(acc,recall,precision,f_measure))
    for item in [tp,tn,fp,fn]:
        calclist.append(item)
    """
    
    """
    if(speaker_name == "NHK1112" or speaker_name == "NHK1114"):
        anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor{1}.txt".format(speaker_name,test_anchor_num+1)
        anslist = ivmodule.read_ansfile(anstxtpath)
        queslist = ivmodule.clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num,ques_anchor_cluster_num+1)
        acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(ori_filelist,anslist,queslist)
        print("{},{},{},{}".format(acc,recall,precision,f_measure))
        f_measurelist.append(f_measure)
        for item in [tp,tn,fp,fn]:
            calclist.append(item)
    """
    
    if(search_mode == "all_anchor"):
        allanc = np.array([])
        for i in range(anchor_num):
            i = i+1
            queslist = ivmodule.clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num,ques_anchor_cluster_num)
            allanc = np.hstack((allanc,queslist))
        queslist = allanc
        #print(queslist)
    anslist = ivmodule.read_ansfile(anstxtpath)
    queslist = queslist.tolist()
    acc,recall,precision,f_measure,tp,tn,fp,fn = ivmodule.test(ori_filelist,anslist,queslist)
    print("{},{},{},{}".format(acc,recall,precision,f_measure))
    
    
    """時間的な分散の云々かんぬん
    print(queslist)
    variance = ivmodule.time_del_clus(ivpath,queslist,filename)
    print(variance)
    """

"""
    #print("anchor_num is:{}\n".format(anchor_num))
    #print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    #for i,item in enumerate(ori_filelist):
    #    print("{0} {1}".format(ori_filelist[i],int(cluster[i])))
calclist = np.array(calclist)
#print(calclist.shape)
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
print("total {},{},{},{}".format(acc*100,recall*100,precision*100,f_measure*100))
print("std : {}".format(np.std(np.array(f_measurelist))*100))
"""
