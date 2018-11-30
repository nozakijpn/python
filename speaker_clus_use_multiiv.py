#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os # osモジュールのインポート
import numpy as np
from kenkyu_module import iv_module
np.set_printoptions(threshold=np.inf)

roop_num = 100
iv_th = 0.5
tyouhuku_th = 10
anchor_th = 0.05
test_anchor_num = 1#評価したいアンカーのクラスタ番号の指定
ques_anchor_cluster_num = 1#評価したいアンカーのクラスタ番号

mode = "multi"
single_filename = "NHK0826"

wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/"
ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"

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

        lis = ivmodule.get_thlist(ivpath,maxfile,filelist)#もっとも重複した音声ファイルが多い音声ファイルの重複したwavファイルのリストを返す
        aveiv = []
        for item in lis:
            addcos = 0
            for item2 in filelist:
                addcos =+ ivmodule.calc_cos(ivpath,item, item2)
            if(addcos/len(lis)>iv_th):
                aveiv.append(item2)
        lis = aveiv + lis
        
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
    queslist = ivmodule.clusnum_to_filename(cluster,ori_num,ori_filelist,anchor_num,ques_anchor_cluster_num)#クラスタ分けの数字からファイル名をクラスタ毎に取り出す
    
    """時間的な分散の云々かんぬん
    print(queslist)
    variance = ivmodule.time_del_clus(ivpath,queslist,filename)
    print(variance)
    """
    
    acc,recall,precision,f_measure = ivmodule.test(ori_filelist,anslist,queslist)
    print("{},{},{},{}".format(acc,recall,precision,f_measure))
    print("acc:{0:.3f}\nrecall:{1:.3f}\nprecision:{2:.3f}\nf_measure:{3:.3f}".format(acc,recall,precision,f_measure))
    
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