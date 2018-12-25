import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from math import *
from scipy.stats import norm
import glob
import wave
import re
import os

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

#path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/*.wav"
#path = "/home/nozaki/newsdata/cutwav/vdet_wav/*.wav"
path = "./*_mix.y"
path_list = glob.glob(path)
path_list.sort()
time_list = []
name = ""

basename="JM110_JB10N044"

ivlist=[]

for item1 in path_list:
    item1 = item1.replace("./","")
    item1 = item1.replace(".y","")
    ivlist.append(calc_cos("./",basename,item1))
    print("now"+item1)
plt.xlabel("Cosine similarity")
plt.ylabel("Num of speech data")
#plt.title("histogram of time plot")
plt.hist(ivlist,bins=200,range=(-1,1),normed=True)
#plt.plot(x,norm.pdf(x)*200,lw=3,color="r")
plt.show()