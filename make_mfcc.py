#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 14:00:31 2018

@author: nozaki
"""

import librosa

path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0090.wav"
x,fs = librosa.load(path,sr=44100)
print(max(x))
mfccs = librosa.feature.mfcc(x,sr=fs)
print(mfccs.shape)

from scipy.io.wavfile import read

fs,data = read(path)
print(max(data))