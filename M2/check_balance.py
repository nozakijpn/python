import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from math import *
from scipy.stats import norm
import glob
import wave
import re
import os

#path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/*.wav"
#path = "/home/nozaki/newsdata/cutwav/vdet_wav/*.wav"
path = "./*.wav"
savepath = "../trim_short_balance"
path_list = glob.glob(path)
path_list.sort()
time_list = []
name = ""

cuttime = 0.3

basename="JM110_JB10N044"
basespeaker="JM110"

th_shortest = 5

trim_st = 2

for item in path_list:
    wf = wave.open(item, "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    if(time > trim_st+cuttime):
        time_list.append(time)
        result = item.replace("./","")
        result = re.sub("_[a-xA-Z0-9_]*.raw.wav","",result)
        if(name != result):
        	name = result
        	cnt = 1
        else:
        	cnt += 1
        os.system("sox {} {}/{}_{:04d}.wav trim {} {}\n".format(item,savepath,name,cnt,trim_st,cuttime))
        print("sox {} {}/{}_{:04d}.wav trim {} {}\n".format(item,savepath,name,cnt,trim_st,cuttime))
   
#time_list = np.array(time_list)
