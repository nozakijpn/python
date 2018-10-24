import glob
import numpy as np
bins = []
list_time = []
list_cos = []

ivpath = ""
wavpath = ""
center_wav_time = 5


for i in range(0,100,5):
        bins.append(i*0.1)
        bins = np.array(bins)


filelist = glob.glob(ivpath)

for filename in filelist:
        list_time.append(get_time(wavpath,filename))
        list_iv.append(get_iv)
center_time = getNearestValue(list, center_wav_time)
center_time_num = list_time.index(center_time_num)

center_time_name = filelist[center_time_num]

del list_time[center_time_num]
del filelist[center_time_num]

for filename in filelist:
        cos = calc_cos(ivpath,center_time_name,filelist)
        list_cos.append(cos)

inds = np.digitize(np.array(list_time), bins)#それぞれのi-vectorのwavの時間がどれに区切られるかを計算

list_average_cos = []
for i in range(len(bins)): #それぞれの時間の範囲を人海作戦
        sub_list_cos = []
        for j,item in enumerate(inds):
                if(i == item):#wavの収録時間と範囲が一致した時、
                        sub_list_cos.append(list_cos[j])

        list_average_cos.append(np.average(sub_list_cos))

print(list_average_cos)#0.5秒ごとのコサイン類似度の平均を表示


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
        wf = wave.open("{0}{1}.wav".format(wavpath,filename) , "r" )
        time = float(wf.getnframes()) / wf.getframerate()

        return time

def get_ivdata(ivpath,filename):
        #ファイル名を指定してivのリストを返す
        f = open('{0}{1}.y'.format(ivpath,filename))
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