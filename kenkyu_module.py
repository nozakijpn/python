#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 11:05:30 2018

@author: nozaki
"""
import os # osモジュールのインポート
import numpy as np
import wave 
import math

class iv_module:
    def __init__(self,roop_num,iv_th,tyouhuku_th,anchor_th):
        self.roop_num = roop_num
        self.iv_th = iv_th
        self.tyouhuku_th = tyouhuku_th
        self.anchor_th = anchor_th
        
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
        
        #print("tp:{0} tn:{1} fp:{2} fn:{3}".format(tp,tn,fp,fn))
        
        acc = (tp+tn)/(tp+tn+fp+fn)
        
        recall = float(tp/(tp+fn))
        
        precision = float(tp/(tp+fp))
        
        f_measure = float((2*recall*precision)/(recall + precision))
        
        return acc,recall,precision,f_measure
        
    def read_ansfile(self,anstxtpath):    
        ans = []
        f = open(anstxtpath)
        lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        f.close()
        
        for line in lines2:
            line = line.replace("\n","")
            ans.append(line)
        return ans       
        
    def search_file(self,filelist,search_file):
        for item in filelist:
            if(item == search_file):
                return 1                   #if exist
        return 0                           #if not exist
            
    def clusnum_to_filename(self,cluster,ori_num,ori_filelist,anchor_num):
        for i in range(anchor_num):
            print("cluster_{0}".format(i+1))
            for j in range(ori_num):
                if(cluster[j] == i+1):
                    print(ori_filelist[j])
            print("\n")
    
    def cnt_filenum(self,filelist):
        filelist = np.array(filelist)
        num = filelist.shape
        return num[0]
    
    def cnt_tyouhuku_num(self,ivpath,filelist):   
        #リストにある音声ファイルのcos類似度による重複回数のリストを返す
        tyouhuku = []
        iv_th = self.iv_th
        i = 0
        for item in filelist:
            cnt = 0
            for item2 in filelist:
                if(item != item2):
                    if(self.calc_cos(ivpath,item,item2) > iv_th):
                        cnt += 1
            tyouhuku.append(cnt)
            i += 1
        
        return tyouhuku
    
    def search_filenum(self,filelist,filename,num):
        for i in range(num):
            if(filelist[i] == filename):
                return i
        
    def make_tyouhukulist(self,filelist,tyouhukulist,num):
        #重複回数が閾値以上のファイルのリストを返す
        tyouhuku_th = self.tyouhuku_th
        lis = []
        for i in range(num):
            cnt = 0
            for item in tyouhukulist:
                if(filelist[i]==item):
                    cnt += 1
            if(cnt > tyouhuku_th):
                lis.append(filelist[i])
            
        return lis
    
    def get_tyouhukulist(self,ivpath,filelist,th_list):
        #重重したwavファイルのリストを返す
        tyouhukulist = []
        for item in th_list:
            li = self.get_thlist(ivpath,item,filelist)
            tyouhukulist = tyouhukulist + li
            
        return tyouhukulist
        
    
    def get_thlist(self,ivpath,maxfile,filelist):
        #閾値以上のファイルのリストを返す
        list = []
        iv_th = self.iv_th
        for item in filelist:
            if(self.calc_cos(ivpath,maxfile,item)>iv_th):
                if(maxfile != item):
                    list.append(item)
                
        return list
     
               
    def get_filelist(self,path):
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
    
    def threshold_time(self,path,filelist,num,timemin,timemax):
        #指定した時間内のwavファイルとそれ以外のwavファイルでそれぞれリスト化して返す
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
    
    def get_time(self,path,filename):
        #wavデータの時間情報取得
        wf = wave.open("{0}{1}.wav".format(path,filename) , "r" )
        time = float(wf.getnframes()) / wf.getframerate()
    
        return time
    
    def get_ivdata(self,path,filename):
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
    
    def calc_cos(self,ivpath,ivfile1, ivfile2):
        """
        cos類似度を計算する関数
        @return cos類似度を計算した結果。0〜1で1に近ければ類似度が高い。
        入力はyファイルのファイル名
        """
        iv1 = self.get_ivdata(ivpath,ivfile1)
        iv2 = self.get_ivdata(ivpath,ivfile2)
        
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
    
    def print_cos(self,wavpath,ivpath,filelist):
        for item in filelist:
            for item2 in filelist:
                if(2<self.get_time(wavpath,item)):
                    if(2<self.get_time(wavpath,item2)):
                        
                        print("{0} {1} {2:9f} {3:2f} {4:4f} {5:4f}\n".format(item,item2,self.get_time(wavpath,item),self.get_time(wavpath,item2),
                              abs(self.get_time(wavpath,item) - self.get_time(wavpath,item2)),self.calc_cos(ivpath,item,item2)))