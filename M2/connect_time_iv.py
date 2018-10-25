#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#なぜかspyder上ではうまくconnect_{}.shが書き込めないので、コマンドライン上で動かす必要あり

import numpy as np
from kenkyu_module_M2 import iv_module

flame_time = 0.02321995464 #vdetの１フレームの秒数
th_time = 0.5 #インターバルの時間の閾値
newsname = "NHK0826"
th_iv = 0.7
savepath = "/home/nozaki/newsdata/cutwav/vdet_soxed"
wavpath = "/home/nozaki/newsdata/cutwav/vdet_wav"
ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/raw/"

ivmodule = iv_module(0,0.8,5,0.05,ivpath,wavpath)

f = open("/home/nozaki/newsdata/txt/vdet_txt/{}.txt".format(newsname),"r")#音声切り出しのテキスト
strings = f.readlines()

st = []
end = []

for line in strings:
	data = line.split(" ")

	st.append(round(float(data[2]),2))#発話区間の始まりの配列
	end.append(round(float(data[3]),2))#発話区間の終わりの配列

f.close



f = open("/mnt/disk2/bati_dic/news/work2/noza/{0}/matoldresult_{0}_mar4w_02".format(newsname),"r")#音源識別のテキスト(_02)
strings = f.readlines()
audio_d = [] #音源識別結果の配列
for item in strings:
	audio_d.append(int(item))

interval_list = []#発話の間の種類の配列
interval_time = []#発話の間の秒数の配列
sox_cnt = 0

for i,item1 in enumerate(st):
    cnt_speech_interval = 0
    if(i != 0):
        time_div = st[i]-end[i-1]#一つ前の発話と今の発話と間のインターバルの秒数を計算

        cnt_2,cnt_3,cnt_4 = 0,0,0
        for time in range(int(end[i-1]*100),int(st[i]*100),1):
            time = float(time/100)
            now_time = int(time/flame_time)#正確な秒数を書く必要あり。配列に入れるために100倍とかにする必要あり？
            
            if(audio_d[now_time]==2):
                cnt_2 += 1#BGMの区間数をカウント
            if(audio_d[now_time]==3):
                cnt_3 += 1#ノイズの区間数をカウント
            if(audio_d[now_time]==4):
                cnt_4 += 1#pauseの区間数をカウント

            cnt_speech_interval += 1
        
        sub_li = [cnt_2,cnt_3,cnt_4]
        interval_time.append(time_div)
        interval_list.append(np.argmax(sub_li)+2)#発話の間のインターバルの種類を配列に格納

f.close
sox_list = []

f = open("/home/nozaki/newsdata/connect_{}.sh".format(newsname),"w")
f1 = open("/home/nozaki/newsdata/rename_{}.sh".format(newsname),"w")
flag_skip = 0

for i,item in enumerate(interval_list):
    print(i,i+1,i+2,interval_list[i],interval_time[i])
    
    if(i < np.array(interval_list).shape[0]):#first line
        if(interval_time[i]<th_time):
            flag_time = 1
        else:
            flag_time = 0
        """
        if(interval_list[i+1] == interval_list[i]):
            flag_next = 1
        else:
            flag_next = 0
        """
        #under if is important method!!
        
        ivname1 = "{}_{:04d}".format(newsname,i+1)
        ivname2 = "{}_{:04d}".format(newsname,i+2)
        
        if(flag_time == 1 and ivmodule.calc_cos(ivpath,ivname1,ivname2)>th_iv):#connect method
            sox_list.append(i+1)
        else:#cut method
            sox_cnt += 1
            sox_list.append(i+1)
            if len(sox_list)!=1:
                print("sox ")
                f.write("sox ")
                for item1 in sox_list:
                    print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                    f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                    f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                sox_list = []
            else:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                sox_list = []


sox_list.append(np.array(interval_list).shape[0]+1)
sox_cnt += 1
if len(sox_list)!=1:
    print(sox_list)
    print("sox ")
    f.write("sox ")
    for item1 in sox_list:
        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
        print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
        f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
    print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
    f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))

else:
    f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
    print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
    f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
    sox_list = []
    sox_list.append(i+1)

f1.close
f.close



