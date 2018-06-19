# -*- coding: utf-8 -*-

import os
import numpy as np
import shutil

def replace_csv_data():
    #shutil.rmtree("data/rep")
    #os.mkdir("data/rep")
    for name in range(1,10000):
        for year in range(2000,2019):
            print(name)
            if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
                f = open('data/{0}_{1}.csv'.format(name,year),encoding='cp932')
                lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
                # lines2: リスト。要素は1行の文字列データ
                
                for line in lines2:
                    fout = open('data/rep/{0}_{1}.csv'.format(name,year), 'a')
                    line = line.replace('\"', '')
                    fout.write(line)
                    fout.close
                fout.close
                f.close
                
def mktrainset():
    hairetu = []
    hairetu = np.array(hairetu)
    labels = []
    labels = np.array(labels)
    for name in range(1,10000):
        for year in range(2000,2019):
            if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
                data = np.genfromtxt("data/rep/{0}_{1}.csv".format(name,year),delimiter=",", skip_header=2, dtype='int')
                data = np.delete(data, 0, 1)
                data = np.delete(data, 5, 1)
                maxcnt = data.shape[0]
                maxcnt = int(maxcnt/21)
                print(maxcnt)
                #始値 	高値	安値	終値	出来高
                for i in range(0,maxcnt):
                    #print(data[i*21:i*21+21].shape)
                    hairetu = np.append(hairetu,np.array(data[i*21:i*21+20]))
                    sub = data[i*21+20,3]-data[i*21+19,3]#最終日とその前日の差
                    if(sub>0):#値が上がっていればlabelに1を返す
                        label=1
                    else:
                        label=0
                    labels = np.append(labels,label)
        traindata = np.reshape(hairetu,(-1,20,5))#trainセットを作成
        print(traindata.shape)#batch,days,features
        print(labels.shape)
        
    return traindata,labels

  
#replace_csv_data()           
trainset,labels = mktrainset()
