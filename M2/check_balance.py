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
path_list = glob.glob(path)
path_list.sort()
time_list = []
name = ""

for item in path_list:
    wf = wave.open(item, "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    time_list.append(time)
    result = item.replace("./","")
    result = re.sub("_[a-xA-Z0-9_]*.raw.wav","",result)
    if(name != result):
    	name = result
    	cnt = 1
    else:
    	cnt += 1
    os.system("sox {} ../../sph/{}_{:04d}.wav trim 0.1 1.1\n".format(item,name,cnt))
   
time_list = np.array(time_list)
print(np.max(time_list))
print(np.min(time_list))