f = open("/home/nozaki/newsdata/txt/other/sox_trim.sh","r")

wavpath = "/home/nozaki/newsdata/wav"
savepath = "/home/nozaki/newsdata/cutwav/vdet_interval"

lines = f.readlines()

list_st,list_end = [],[]

for line in lines:
	line = line.split()
	list_st.append(float(line[4]))
	list_end.append(float(line[4])+float(line[5]))

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
newscnt = 0
cnt_i = 0

for i,line in enumerate(list_st):
	cnt_i += 1
	#print(len(list_st),i+1)
	if(len(list_st)==i+1):
		break
	elif(list_st[i+1]-list_end[i]<0):
		newscnt += 1
		cnt_i = 0
	else:
		print("sox {}/{}.wav {}/{}_{:04d}_{:04d}.wav trim {} {}".format(wavpath,newslist[newscnt],savepath,newslist[newscnt],cnt_i,cnt_i+1,list_end[i],list_st[i+1]-list_end[i]))