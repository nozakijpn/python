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
savepath = "../../sph"
path_list = glob.glob(path)
path_list.sort()
time_list = []
name = ""

basename="JM110_JB10N044"
basespeaker="JM110"


for item1 in path_list:
    item1 = item1.replace("./","")
    item1 = item1.replace(".wav","")
    if(item1.find(basespeaker)==-1):
   		os.system("sox ../../{0}.wav {1}.wav {2}/{0}_{1}_mix.wav".format(basename,item1,savepath))
   		print("now:",item1)