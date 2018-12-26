newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
fout_all = open("/home/nozaki/kakiokoshi_txt_forvdet/kakiokoshi.txt","w")
for newsname in newslist:
    ori_st,ori_end,vdet_st,vdet_end=[],[],[],[]
    sentence = []
    
    f = open("/home/nozaki/newsdata/txt/vdet_txt/{}.txt".format(newsname),"r")
    for item in f.readlines():
        item = item.split()
        vdet_st.append(int(float(item[2])*100))
        vdet_end.append(int(float(item[3])*100))
    f.close()
    f = open("/home/nozaki/newsdata/kakiokoshi_txt/{}.txt".format(newsname),"r")
    for item in f.readlines():
        item = item.split()
        if(len(item)==1):
            break
        ori_st.append(int(float(item[0])*100))
        ori_end.append(int(float(item[1])*100)+int(float(item[0])*100))
        sentence.append(item[2])
        print(item[2])

    f.close()
    if(vdet_end[-1]>ori_end[-1]):
        lenght = vdet_end[-1]
    else:
        lenght = ori_end[-1]
        
    ori_speaker_list = [0]*lenght
    vdet_speaker_list = [0]*lenght
    
    for i,st in enumerate(ori_st):
        for now in range(ori_st[i],ori_end[i],1):
            ori_speaker_list[now] = i
    
    for i,st in enumerate(vdet_st):
        now_list = []
        for now in range(vdet_st[i],vdet_end[i],1):
            vdet_speaker_list[now] = i        
            now_list.append(ori_speaker_list[now])
        now_list = list(set(now_list))
        
        fout = open("/home/nozaki/kakiokoshi_txt_forvdet/{}_{:04d}.txt".format(newsname,i+1),"w")
        
        if(len(now_list)==1 and now_list[0]==0):
            print("{}_{:04d} None".format(newsname,i+1))
            fout_all.write("{}_{:04d}\n\n".format(newsname,i+1))
        else:
            #now_list.pop(0)
            now_list = [i1 for i1 in now_list if i1 != 0]
            print("{}_{:04d} {}".format(newsname,i+1,now_list))
            
            #print("{}\n".format(newsname))
            fout_all.write("{}_{:04d}\n".format(newsname,i+1))
            for ii in now_list:
                #print("{} ".format(sentence[ii]))
                fout.write("{} ".format(sentence[ii]))
                fout_all.write("{} ".format(sentence[ii]))
            fout_all.write("\n")
            
                
            
    #print(vdet_speaker_list)