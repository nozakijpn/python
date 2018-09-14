#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 22:16:57 2018

@author: nozaki
"""
#coding:utf-8
import matplotlib.pyplot as plt
from scipy import signal
import librosa

# python
"""
wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0001.wav"
import librosa
x, fs = librosa.load(wavpath, sr=44100)
mfccs = librosa.feature.mfcc(x, sr=fs,n_mfcc=10)
print(mfccs.shape)
print(len(x))
"""

wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0001.wav"

data, fs = librosa.load(wavpath, sr=44100)
time = len(data)
plt.close('all')
print("{}[s]".format(time/44100))

fs = 44100.0 # サンプリング周波数
f,t,Sxx = signal.spectrogram(data, fs,noverlap=0,nperseg=1024)
print(time)
print(len(t)*512*2)
plt.figure()
plt.pcolormesh(t,f,Sxx,vmax=1e-6)
plt.xlim([0,0.2])
plt.ylim([0,2000])
plt.xlabel(u"time [sec]")
plt.ylabel(u"frecuency [Hz]")
# plt.colorbar()
plt.show()
