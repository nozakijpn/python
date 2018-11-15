newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]


list_soxed,list_wav = [],[]
f = open("./tooltxt/rename.txt","r")
lines = f.readlines()
cnt_good,cnt_bad = 0,0

for line in lines:
	line = line.split()
	list_soxed.append(line[1])
	line[2] = line[2].replace(".y","")
	list_wav.append(line[2])

f.close()

for newsname in newslist:
	f = open("/home/nozaki/newsdata/txt/change_speaker_vdet/{}.txt".format(newsname),"r")
	lines = f.readlines()
	for line in lines:
		line = line.replace("\n","")
		idnum = list_wav.index(line)
		print(list_wav[idnum-1],list_wav[idnum])
		if(list_soxed[idnum-1] != list_soxed[idnum]):
			cnt_good += 1
			print("good\n")
		else:
			cnt_bad += 1
			print("bad\n")
	f.close()
total = cnt_bad + cnt_good
print(cnt_good,cnt_bad)
print("good : {}".format(float(cnt_good)/total))
print("bad : {}".format(float(cnt_bad)/total))
