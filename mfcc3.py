#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 22:16:57 2018

@author: nozaki
"""

# python
"""
wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0001.wav"
import librosa
x, fs = librosa.load(wavpath, sr=44100)
mfccs = librosa.feature.mfcc(x, sr=fs,n_mfcc=10)
print (mfccs.shape)
"""
#coding:utf-8
import wave
import numpy as np
import cmath as cm
import matplotlib.pyplot as plt
import scipy
import librosa
import librosa.display

if __name__ == '__main__':
    # 波形データ読み込み
    path = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/news/NHK0826_0001.wav"
    #path = "/home/nozaki/TX0528.wav"
    #sample_rate, sound = scipy.io.wavfile.read(librosa.util.example_audio_file())
    sound,sample_rate = librosa.load(path,sr=44100)
    print("sample rate {}".format(sample_rate))
    second = sound.shape[0]/sample_rate
    minute = int(second/60)
    print("{0}分{1}秒".format(minute,int(second%60)))
    window_size = 0.2
    window_stride = 0.2
    n_fft = int(sample_rate * window_size)
    win_length = n_fft
    hop_length = int(sample_rate * window_stride)
    # 短時間フーリエ変換
    D = np.abs(librosa.stft(sound, n_fft=n_fft, hop_length=hop_length,
                         win_length=win_length))
    #D = np.abs(librosa.stft(sound))

    #D1 = np.delete(D,range(int(D.shape[1])-int(D.shape[1]%100),int(D.shape[1])-int(D.shape[1]%100)+int(D.shape[1]%100),1),1)
    D1 = np.delete(D,range(100,400,1),1)
    #D1 = np.reshape(D1,(4411,10,-1))

    #np.savetxt("/home/nozaki/tx0528.csv",D1,delimiter=",")
    
    """
    plt.subplot(2,1,2)
    plt.title('guitar_A4')
    plt.plot(D[0],D[1])
    print(D[0])
    
    # リコーダーA4
    plt.subplot(2,1,2)
    plt.title('recorder_A4')
    plt.plot(frq,dt2)
    """
    # グラフ表示
    librosa.display.specshow(librosa.amplitude_to_db(D1,ref=np.max),y_axis="log",x_axis="time")
    plt.title("power spectrogram")
    plt.colorbar(format="%+2.0f db")
    plt.tight_layout()
    #plt.show()
    