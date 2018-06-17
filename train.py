# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 18:37:59 2018

@author: Daichi-N
"""

import os
import numpy as np
import shutil

def replace_csv_data(self):
    shutil.rmtree("data/rep")
    os.mkdir("data/rep")
    for name in range(1,5000):
        for year in range(2015,2017):
            if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
                f = open('data/{0}_{1}.csv'.format(name,year))
                lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
                # lines2: リスト。要素は1行の文字列データ
                
                for line in lines2:
                    fout = open('data/rep/{0}_{1}.csv'.format(name,year), 'a')
                    line = line.replace('\"', '')
                    fout.write(line)
                    fout.close
                fout.close
                f.close
                
  
#replace_csv_data(1)              

for name in range(1,5000):
    for year in range(2015,2017):
        if(os.path.exists('data/{0}_{1}.csv'.format(name,year))==True):
            data = np.genfromtxt("data/rep/{0}_{1}.csv".format(name,year),delimiter=",", skip_header=2, dtype='int')
            data = np.delete(data, 0, 1)
            data = np.delete(data, 5, 1)
            maxcnt = data.shape[0]
            maxcnt = int(maxcnt/21)
            #始値 	高値	安値	終値	出来高
            for i in range(0,maxcnt):
                print(data[i*21:i*21+21])
                sub = data[i*21+20,3]-data[i*21+19,3]#最終日とその前日の差
                if(sub>0):
                    label=1
                else:
                    label=0
                print(sub)
