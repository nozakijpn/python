import glob
import numpy as np
import math
import wave
import matplotlib.pyplot as plt
import matplotlib
import itertools

ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw"
wavpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/data/sph"
center_wav_time = 100

def getNearestValue(list, num):
    """
    概要: リストからある値に最も近い値を返却する関数
    @param list: データ配列
    @param num: 対象値
    @return 対象値に最も近い値
    """
    # リスト要素と対象値の差分を計算し最小値のインデックスを取得
    idx = np.abs(np.asarray(list) - num).argmin()
    return list[idx]


def get_time(wavpath,filename):
    #wavデータの時間情報取得
    wf = wave.open("{0}/{1}.wav".format(wavpath,filename) , "r" )
    time = float(wf.getnframes()) / wf.getframerate()

    return time

def get_ivdata(ivpath,filename):
        #ファイル名を指定してivのリストを返す
    f = open('{0}/{1}.y'.format(ivpath,filename))
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
  

def main():
    bins = []
    list_time = []
    list_cos = []

    for i in range(0,100,5):
        bins.append(i*0.1)
    bins = np.array(bins)
    
    ylist = glob.glob("{}/*.y".format(ivpath))
    
    filelist = []
    for item in ylist:
        item = item.replace("{}/".format(ivpath),"")
        item = item.replace(".y","")
        filelist.append(item)
    
    filelist.sort()
    
    for filename in filelist:
            list_time.append(get_time(wavpath,filename))
    
    center_time = getNearestValue(list_time, center_wav_time)
    center_time_num = list_time.index(center_time)
    
    center_time_name = filelist[center_time_num]
    
    print(center_time_name,center_time)
    
    del list_time[center_time_num]
    del filelist[center_time_num]
    
    for filename in filelist:
            cos = calc_cos(ivpath,center_time_name,filename)
            list_cos.append(cos)
    
    lll = []
    nowtime = 0
    nowcnt = 400
    for i,item in filelist:
        lll.append(item)
        nowtime += list_time[i]
        if(nowtime > 10):
            print("sox ")
            for j in lll:
                print("{}.wav ".format(j))
            print("{:04d}.wav".format(nowcnt))
            nowcnt += 1
    
if __name__ == '__main__':
    main()

