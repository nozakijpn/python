#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#なぜかspyder上ではうまくconnect_{}.shが書き込めないので、コマンドライン上で動かす必要あり

import numpy as np
from kenkyu_module import iv_module
import sys
from scipy.spatial.distance import correlation
args = sys.argv

flame_time = 0.02322 #vdetの１フレームの秒数
th_time =0.8#インターバルの時間の閾値1.26
#newsname = "NHK0826"
newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
th_iv = 0.2
th_pearson = 0.7 #0.75
time_shortest = 0.3 #[sec] 0.5

mode = int(args[1])
if(len(args) >= 3):
    th_time = float(args[2])
if(len(args) >= 4):
    th_iv = float(args[3])
"""
mode = 1 : timeonly
mode = 2 : time and iv
mode = 3 : background noise
mode = 4 : background noise and time
mode = 5 : background noise use pearson for interval time
mode = 6 : mode5 and time
mode = 7 : mode6 or shortest_time
mode = 8 : mode7 + ivcos
"""
f = open("/home/nozaki/newsdata/connect.sh","w")
f1 = open("/home/nozaki/newsdata/rename.sh","w")

wavpath = "/home/nozaki/newsdata/cutwav/vdet_wav"
ivpath = "/home/nozaki/speaker_clustering/news_i-vector/iv/ori_vdet/"

if(mode == 1):
    savepath = "/home/nozaki/newsdata/cutwav/vdet_soxed/timeonly"
elif(mode == 2):
    savepath = "/home/nozaki/newsdata/cutwav/vdet_soxed/time_iv"
else:
    savepath = "/home/nozaki/newsdata/cutwav/vdet_soxed/background_noise"

f.write("rm {} -r\nmkdir {}\n".format(savepath,savepath))

for newsname in newslist:
    f3 = open("/home/nozaki/newsdata/txt/vdet_txt/{}.txt".format(newsname),"r")#音声切り出しのテキスト
    strings = f3.readlines()

    st = []
    end = []

    for line in strings:
    	data = line.split(" ")

    	st.append(round(float(data[2]),2))#発話区間の始まりの配列
    	end.append(round(float(data[3]),2))#発話区間の終わりの配列

    f3.close

    #ivpath = "/home/nozaki/speaker_clustering/02_i-vector_system_with_ALIZE3.0/iv/soturon_news_ivdata/"
    
    #ivpath = "{0}{1}/".format(ivpath,newsname)

    ivmodule = iv_module(0,0.8,5,0.05,ivpath,wavpath)

    f3 = open("/mnt/disk2/bati_dic/news/work2/noza/{0}/matoldresult_{0}_mar4w_02".format(newsname),"r")#音源識別のテキスト(_02)
    strings = f3.readlines()
    audio_d = [] #音源識別結果の配列
    for item in strings:
    	audio_d.append(int(item))

    interval_list = []#発話の間の種類の配列
    interval_time = []#発話の間の秒数の配列
    sox_cnt = 0

    list_bgm,list_noise,list_pause = [],[],[]

    for i,item1 in enumerate(st):
        cnt_speech_interval = 0
        if(i != 0):
            time_div = st[i]-end[i-1]#一つ前の発話と今の発話と間のインターバルの秒数を計算

            cnt_1,cnt_2,cnt_3,cnt_4,cnt_total = 0,0,0,0,0
            for time in range(int(end[i-1]*100),int(st[i]*100),1):
                time = float(time/100)
                now_time = int(time/flame_time)#正確な秒数を書く必要あり。配列に入れるために100倍とかにする必要あり？
                cnt_total += 1
                
                #print(audio_d[now_time])

                if(audio_d[now_time]==1):
                    cnt_total -= 1#if speech ,descount cnt_total
                if(audio_d[now_time]==2):
                    cnt_2 += 1#BGMの区間数をカウント
                if(audio_d[now_time]==3):
                    cnt_3 += 1#ノイズの区間数をカウント
                if(audio_d[now_time]==4):
                    cnt_4 += 1#pauseの区間数をカウント

                cnt_speech_interval += 1
            
            sub_li = [cnt_2,cnt_3,cnt_4]
            #print("{}_{:04}".format(newsname,i),st[i-1],end[i-1])
            #print("{}_{:04}".format(newsname,i),"{}[sec]".format(str(round(end[i-1]-st[i-1],2))))
            #print("     ",sub_li,"{}[sec]".format(str(round(st[i]-end[i-1],2))))
            interval_time.append(time_div)
            interval_list.append(np.argmax(sub_li)+2)#発話の間のインターバルの種類を配列に格納
            list_bgm.append(float(cnt_2)/cnt_total)
            list_noise.append(float(cnt_3)/cnt_total)
            list_pause.append(float(cnt_4)/cnt_total)

    f3.close
    sox_list = []

    flag_skip = 0

    fout = open("./kari.txt","w")
    for i in range(1,100,1):
        fout.write("{}_{:04d}\n".format(newsname,i))
        fout.write("    {} {}[sec]\n".format(interval_list[i-1],interval_time[i-1]))
    fout.close()

    if(mode == 1):
        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
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
                
                #if(flag_time == 1 and ivmodule.calc_cos(ivpath,ivname1,ivname2)>th_iv):#connect method
                if(flag_time == 1):#connect method
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []


        sox_list.append(np.array(interval_list).shape[0]+1)
        sox_cnt += 1
        if len(sox_list)!=1:
            #print(sox_list)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))

        else:
            sox_list = []
            sox_list.append(i+2)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            
            

    elif(mode == 2):
        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
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
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []


        sox_list.append(np.array(interval_list).shape[0]+1)
        sox_cnt += 1
        if len(sox_list)!=1:
            #print(sox_list)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))

        else:
            sox_list = []
            sox_list.append(i+2)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            

    elif(mode == 3):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                if(interval_list[i+1] == interval_list[i]):
                    flag_next = 1
                else:
                    flag_next = 0
                
                if(interval_list[i-1] == interval_list[i]):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #if(flag_time == 1):#connect method
                if(flag_next == 1):#connect method
                    sox_list.append(i+1)
                elif(flag_next == 0 and flag_pred == 1):#connect method2
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        if(interval_list[i-1] == interval_list[i]):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))

    elif(mode == 4):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                if(interval_list[i+1] == interval_list[i]):
                    flag_next = 1
                else:
                    flag_next = 0
                
                if(interval_list[i-1] == interval_list[i]):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #if(flag_time == 1):#connect method
                if(flag_time == 1 and flag_next == 1):#connect method
                    sox_list.append(i+1)
                elif(flag_time == 1 and flag_next == 0 and flag_pred == 1):#connect method2
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        if(interval_time[i]<th_time and interval_list[i-1] == interval_list[i]):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))

    elif(mode == 5):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                interval_percent_next,interval_percent_now = [],[]
                
                interval_percent_next.append(list_bgm[i+1])
                interval_percent_next.append(list_noise[i+1])
                interval_percent_next.append(list_pause[i+1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])
                if(1 - correlation(interval_percent_next, interval_percent_now) > th_pearson):
                    flag_next = 1
                else:
                    flag_next = 0
                
                interval_percent_pre,interval_percent_now = [],[]
                
                interval_percent_pre.append(list_bgm[i-1])
                interval_percent_pre.append(list_noise[i-1])
                interval_percent_pre.append(list_pause[i-1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])

                if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #if(flag_time == 1):#connect method
                if(flag_next == 1):#connect method
                    sox_list.append(i+1)
                elif(flag_next == 0 and flag_pred == 1):#connect method2
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        interval_percent_pre,interval_percent_now = [],[]
        
        interval_percent_pre.append(list_bgm[i-1])
        interval_percent_pre.append(list_noise[i-1])
        interval_percent_pre.append(list_pause[i-1])
        interval_percent_now.append(list_bgm[i])
        interval_percent_now.append(list_noise[i])
        interval_percent_now.append(list_pause[i])

        if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))

    elif(mode == 6):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                interval_percent_next,interval_percent_now = [],[]
                
                interval_percent_next.append(list_bgm[i+1])
                interval_percent_next.append(list_noise[i+1])
                interval_percent_next.append(list_pause[i+1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])
                if(1 - correlation(interval_percent_next, interval_percent_now) > th_pearson):
                    flag_next = 1
                else:
                    flag_next = 0
                
                interval_percent_pre,interval_percent_now = [],[]
                
                interval_percent_pre.append(list_bgm[i-1])
                interval_percent_pre.append(list_noise[i-1])
                interval_percent_pre.append(list_pause[i-1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])

                if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #if(flag_time == 1):#connect method
                if(flag_time == 1 and flag_next == 1):#connect method
                    sox_list.append(i+1)
                elif(flag_time == 1 and ( flag_next == 0 and flag_pred == 1)):#connect method2
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        interval_percent_pre,interval_percent_now = [],[]
        
        interval_percent_pre.append(list_bgm[i-1])
        interval_percent_pre.append(list_noise[i-1])
        interval_percent_pre.append(list_pause[i-1])
        interval_percent_now.append(list_bgm[i])
        interval_percent_now.append(list_noise[i])
        interval_percent_now.append(list_pause[i])

        if(flag_time == 1 and (1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson)):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))

    elif(mode == 7):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                interval_percent_next,interval_percent_now = [],[]
                
                interval_percent_next.append(list_bgm[i+1])
                interval_percent_next.append(list_noise[i+1])
                interval_percent_next.append(list_pause[i+1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])
                if(1 - correlation(interval_percent_next, interval_percent_now) > th_pearson):
                    flag_next = 1
                else:
                    flag_next = 0
                
                interval_percent_pre,interval_percent_now = [],[]
                
                interval_percent_pre.append(list_bgm[i-1])
                interval_percent_pre.append(list_noise[i-1])
                interval_percent_pre.append(list_pause[i-1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])

                if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #print(ivname1,flag_pred,flag_next)

                #if(flag_time == 1):#connect method
                if((flag_time == 1 and flag_next == 1) or interval_time[i]<time_shortest):#connect method
                    sox_list.append(i+1)
                    #print("1")
                elif(flag_time == 1 and ( flag_next == 1 and flag_pred == 0)):#connect method2
                    sox_list.append(i+1)
                    #changed next and pred 1 0
                    #print("2")
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        interval_percent_pre,interval_percent_now = [],[]
        
        interval_percent_pre.append(list_bgm[i-1])
        interval_percent_pre.append(list_noise[i-1])
        interval_percent_pre.append(list_pause[i-1])
        interval_percent_now.append(list_bgm[i])
        interval_percent_now.append(list_noise[i])
        interval_percent_now.append(list_pause[i])

        if((flag_time == 1 and (1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson)) or interval_time[i]<time_shortest):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
    
    elif(mode == 8):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                interval_percent_next,interval_percent_now = [],[]
                
                interval_percent_next.append(list_bgm[i+1])
                interval_percent_next.append(list_noise[i+1])
                interval_percent_next.append(list_pause[i+1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])
                if(1 - correlation(interval_percent_next, interval_percent_now) > th_pearson):
                    flag_next = 1
                else:
                    flag_next = 0
                
                interval_percent_pre,interval_percent_now = [],[]
                
                interval_percent_pre.append(list_bgm[i-1])
                interval_percent_pre.append(list_noise[i-1])
                interval_percent_pre.append(list_pause[i-1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])

                if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                flag_next = 1

                #print(ivname1,flag_pred,flag_next)

                #if(flag_time == 1):#connect method
                if((flag_time == 1 and ivmodule.calc_cos(ivpath,ivname1,ivname2)>th_iv) or interval_time[i]<time_shortest):#connect method
                    sox_list.append(i+1)
                    #print("1")
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        interval_percent_pre,interval_percent_now = [],[]
        
        interval_percent_pre.append(list_bgm[i-1])
        interval_percent_pre.append(list_noise[i-1])
        interval_percent_pre.append(list_pause[i-1])
        interval_percent_now.append(list_bgm[i])
        interval_percent_now.append(list_noise[i])
        interval_percent_now.append(list_pause[i])

        if((flag_time == 1 and (1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson)) or interval_time[i]<time_shortest):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))

    elif(mode == 9):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                interval_percent_next,interval_percent_now = [],[]
                
                interval_percent_next.append(list_bgm[i+1])
                interval_percent_next.append(list_noise[i+1])
                interval_percent_next.append(list_pause[i+1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])
                if(1 - correlation(interval_percent_next, interval_percent_now) > th_pearson):
                    flag_next = 1
                else:
                    flag_next = 0
                
                interval_percent_pre,interval_percent_now = [],[]
                
                interval_percent_pre.append(list_bgm[i-1])
                interval_percent_pre.append(list_noise[i-1])
                interval_percent_pre.append(list_pause[i-1])
                interval_percent_now.append(list_bgm[i])
                interval_percent_now.append(list_noise[i])
                interval_percent_now.append(list_pause[i])

                if(1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)

                #print(ivname1,flag_pred,flag_next)

                #if(flag_time == 1):#connect method
                if((flag_time == 1 and flag_next == 1 and ivmodule.calc_cos(ivpath,ivname1,ivname2)>th_iv) or interval_time[i]<time_shortest):#connect method
                    sox_list.append(i+1)
                    #print("1")
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        interval_percent_pre,interval_percent_now = [],[]
        
        interval_percent_pre.append(list_bgm[i-1])
        interval_percent_pre.append(list_noise[i-1])
        interval_percent_pre.append(list_pause[i-1])
        interval_percent_now.append(list_bgm[i])
        interval_percent_now.append(list_noise[i])
        interval_percent_now.append(list_pause[i])

        if((flag_time == 1 and (1 - correlation(interval_percent_pre, interval_percent_now) > th_pearson)) or interval_time[i]<time_shortest):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))


    elif(mode == 1000):
        flag_skip = 0
        flag_pred = 0

        for i,item in enumerate(interval_list):
            #print(i,i+1,i+2,interval_list[i],interval_time[i])
            
            if(i < len(interval_list)-1):#first line
                if(interval_time[i]<th_time):
                    flag_time = 1
                else:
                    flag_time = 0
                
                if(interval_list[i+1] == interval_list[i]):
                    flag_next = 1
                else:
                    flag_next = 0
                
                if(interval_list[i-1] == interval_list[i]):
                    flag_pred = 1
                else:
                    flag_pred = 0

                #under if is important method!!
                
                ivname1 = "{}_{:04d}".format(newsname,i+1)
                ivname2 = "{}_{:04d}".format(newsname,i+2)
                
                #if(flag_time == 1):#connect method
                if(flag_time == 1 or flag_next == 1):#connect method
                    sox_list.append(i+1)
                elif(flag_time == 1 or (flag_next == 0 and flag_pred == 1)):#connect method2
                    sox_list.append(i+1)
                else:#cut method
                    sox_cnt += 1
                    sox_list.append(i+1)
                    if len(sox_list)!=1:
                        #print("sox ")
                        f.write("sox ")
                        for item1 in sox_list:
                            #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                        print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
                        sox_list = []
                    else:
                        f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
                        #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
                        sox_list = []

        sox_cnt += 1
        if(interval_time[i]<th_time or interval_list[i-1] == interval_list[i]):
            sox_list.append(i+1)
            sox_list.append(i+2)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
        elif(sox_list):
            sox_list.append(i+1)
            #print("sox ")
            f.write("sox ")
            for item1 in sox_list:
                f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,item1))
                #print("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
                f.write("{}/{}_{:04d}.wav ".format(wavpath,newsname,item1))
            #print("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            f.write("{}/soxed_{}_{:04d}.wav\n".format(savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
        else:
            sox_list.append(i+1)
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            sox_list = []
            sox_list.append(i+2)
            sox_cnt += 1
            f1.write("cp soxed_{}_{:04d}.y {}_{:04d}.y\n".format(newsname,sox_cnt,newsname,sox_list[0]))
            #print("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
            f.write("cp {}/{}_{:04d}.wav {}/soxed_{}_{:04d}.wav\n".format(wavpath,newsname,sox_list[0],savepath,newsname,sox_cnt))
    else:
        print("error please select number")
    f.write("cp {}/* -t /home/nozaki/speaker_clustering/news_i-vector/data/sph/\n".format(savepath))
    f.close
    f1.close
