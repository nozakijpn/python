import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from math import *
from scipy.stats import norm
import glob
import wave
import re
import os
from kenkyu_module import iv_module

#path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/*.wav"
#path = "/home/nozaki/newsdata/cutwav/vdet_wav/*.wav"
#path = "./*.y"
path = "/home/nozaki/speaker_clustering/news_i-vector/iv/raw/*.y"
path_list = glob.glob(path)
path_list.sort()
#path_list1=["./JF012_0043.y"]
time_list = []
name = ""
list_same,list_other = [],[]
ivpath = ""
#ivpath = "/home/nozaki/speaker_clustering/news_i-vector/iv/raw"
ivmodule = iv_module(0,0.8,5,0.05,path,"")

for item in path_list:
    result1 = item.replace("./","")
    sp1 = re.sub("_[a-xA-Z0-9_]*.y","",result1)
    result1 = result1.replace(".y","")
    print("now:",result1)
    for item2 in path_list:
    	if(item != item2):
	    	result2 = item2.replace("./","")
	    	sp2 = re.sub("_[a-xA-Z0-9_]*.y","",result2)
	    	result2 = result2.replace(".y","")
	    	if(sp1 == sp2):
	    		list_same.append(ivmodule.calc_cos(ivpath,result1,result2))
	    	else:
	    		list_other.append(ivmodule.calc_cos(ivpath,result1,result2))
	    	#print(sp1,sp2,result1,result2,ivmodule.calc_cos(ivpath,result1,result2))

list_same = np.array(list_same)
list_other = np.array(list_other)

plt.xlabel("Cosine similarity")
plt.ylabel("Number of speech data[%]")
#plt.title("histogram of time plot")
plt.hist(list_same,bins=200,range=(-1,1),normed=True)
#plt.plot(x,norm.pdf(x)*200,lw=3,color="r")
plt.show()

plt.xlabel("Cosine similarity")
plt.ylabel("Number of speech data[%]")
#plt.title("histogram of time plot")
plt.hist(list_other,bins=200,range=(-1,1),normed=True)
#plt.plot(x,norm.pdf(x)*200,lw=3,color="r")
plt.show()