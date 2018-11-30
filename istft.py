#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 08:25:59 2018

@author: nozaki
"""

import wave
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
import scipy
import librosa
import librosa.display
# 波形データ読み込み
path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0008.wav"
#path = "/home/nozaki/TX0528.wav"
#sample_rate, sound = scipy.io.wavfile.read(librosa.util.example_audio_file())
sound,sample_rate = librosa.load(path,sr=44100)
"""
  
  print("sample rate {}".format(sample_rate))
  second = sound.shape[0]/sample_rate
  minute = int(second/60)
  print("{0}分{1}秒".format(minute,int(second%60)))
"""
window_size = 0.2
window_stride = 0.1
n_fft = int(sample_rate * window_size)
win_length = n_fft
hop_length = int(sample_rate * window_stride)
# 短時間フーリエ変換
D = librosa.stft(sound, n_fft=n_fft, hop_length=hop_length,win_length=win_length)
#D = librosa.stft(sound)

#librosa.core.istft(stft_matrix, hop_length=None, 
#win_length=None, window='hann', center=True, dtype=<class 'numpy.float32'>, length=None)

D1 = librosa.istft(D,hop_length=hop_length,win_length=win_length)

print(sound.shape)
print(D1.shape)