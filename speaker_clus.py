#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os # osモジュールのインポート
import numpy as np
from kenkyu_module import iv_module
np.set_printoptions(threshold=np.inf)

roop_num = 100
iv_th = 0.6
tyouhuku_th = 10
anchor_th = 0.05

wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/sph/"


def main(speaker_name,ivpath):
    ivpath = "{0}{1}/".format(ivpath,speaker_name)
    anstxtpath = "/home/nozaki/speaker_clustering/news_kotae/{0}/re_anchor1.txt".format(speaker_name)
    
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
        
        if(i == 0):
            queslist1 = lis#1人目のクラスタ
        if(i == 1):
            queslist2 = lis#2人目のクラスタ
            
        for item in lis:
            delnum = ivmodule.search_filenum(ori_filelist,item,ori_num)
            cluster[delnum] = i+1#クラスタ分けされた音声ファイルにラベルを付ける
            filelist.remove(item)#クラスタ分けされた音声ファイルをリストから削除する
            all_anchor.append(item)
     
    print("anchor_num is:{}\n".format(anchor_num))
    
    #clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    
    acc,recall,precision,f_measure = ivmodule.test(ori_filelist,anslist,queslist1)

    print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    
if __name__ == '__main__':
    #ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/"
    ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"
    f = open('/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/newslist.txt')
    lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    f.close()
    
    
    for line in lines2:
        line = line.replace("\n","")
        if(os.path.exists("{0}{1}".format(ivpath,line))):
            main(line,ivpath)
            print("\n")
    
    #main("NHK1112",ivpath)