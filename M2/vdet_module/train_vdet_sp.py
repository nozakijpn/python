f = open("filelist","r")
for newsname in f.readlines():
    lbl_ori = ["0"] * 1000000
    newsname = newsname.replace('\n','')
    f1 = open("/home/nozaki/tooltxt/{}_v.lbl".format(newsname),"r")
    for line in f1.readlines():
        line = line.split()
        st,end = int(float(line[0])*100),int(float(line[1])*100)
        for i in range(st,end,1):
            lbl_ori[i] = line[2]
    f1.close()
    
    f1 = open("lbl/nozaki_{}_sox.txt".format(newsname),"r")
    fout = open("vdet_lbl_v/{}_vdet_v.lbl".format(newsname),"w")
    for line in f1.readlines():
        line = line.split()
        st,end = int(float(line[1])*100),int(float(line[2])*100)
        lbl_vdet = []
        for i in range(st,end,1):
            lbl_vdet.append(lbl_ori[i])
        lbl_vdet = set(lbl_vdet)
        lbl_vdet = list(lbl_vdet)
        
        for item in lbl_vdet:
            if(item == "0" and len(lbl_vdet) == 1):
                lbl_vdet.append("none")
                lbl_vdet.remove("0")
            elif(item == "0"):
                lbl_vdet.remove("0")
        if(len(lbl_vdet)!=1):
            lbl_vdet = ",".join(lbl_vdet)
        else:
            lbl_vdet = lbl_vdet[0]
        fout.write("{} {} {}\n".format(line[1],line[2],lbl_vdet))
        print("{} {} {}".format(line[1],line[2],lbl_vdet))
    f1.close()
    fout.close()