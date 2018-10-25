#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 15:07:42 2018

@author: nozaki
"""

import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from math import *
from scipy.stats import norm
import glob
import wave

path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/*.wav"
path_list = glob.glob(path)

time_list = []

for item in path_list:
    wf = wave.open(item, "r" )
    time = float(wf.getnframes()) / wf.getframerate()
    time_list.append(time)
    

plt.xlabel("time[s]")
plt.ylabel("Num of speech data")
plt.title("histogram of time plot")
plt.hist(time_list,bins=50,range=(0,50))
#plt.plot(x,norm.pdf(x)*200,lw=3,color="r")
plt.show()