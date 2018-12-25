from nozaki_module import iv_module

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
wavpath = "/home/nozaki/newsdata/cutwav/vdet_wav"

ivmodule = iv_module("",wavpath)

total_time,connect_time=0,0

print_detail = 0

list_soxed,list_wav = [],[]
f = open("/home/nozaki/tooltxt/rename.txt","r")
lines = f.readlines()
cnt_same_good,cnt_same_bad,cnt_other_good,cnt_other_bad = 0,0,0,0

for line in lines:
	line = line.split()
	list_soxed.append(line[1])
	line[2] = line[2].replace(".y","")
	list_wav.append(line[2])

f.close()

for newsname in newslist:
	f = open("/home/nozaki/newsdata/txt/change_speaker_vdet/{}_other.txt".format(newsname),"r")
	lines = f.readlines()
	for line in lines:
		line = line.replace("\n","")
		idnum = list_wav.index(line)
		if(print_detail):
			print(list_wav[idnum-1],list_wav[idnum])
		if(list_soxed[idnum-1] != list_soxed[idnum]):
			cnt_other_good += 1
			if(print_detail):
				print("good\n")
		else:
			cnt_other_bad += 1
			if(print_detail):
				print("bad\n")
	f.close()

for newsname in newslist:
	f = open("/home/nozaki/newsdata/txt/change_speaker_vdet/{}_same.txt".format(newsname),"r")
	lines = f.readlines()
	for line in lines:
		line = line.replace("\n","")
		idnum = list_wav.index(line)
		if(print_detail):
			print(list_wav[idnum-1],list_wav[idnum])
		filepath = "{}/{}.wav".format(wavpath,list_wav[idnum])

		total_time += ivmodule.get_wav_time(filepath)
		if(list_soxed[idnum-1] == list_soxed[idnum]):
			cnt_same_good += 1
			if(print_detail):
				print("good\n")
			connect_time += ivmodule.get_wav_time(filepath)
		else:
			cnt_same_bad += 1
			if(print_detail):
				print("bad\n")
	f.close()
total_same = cnt_same_bad + cnt_same_good
#print(cnt_same_good,cnt_same_bad)
#print("same good : {}".format(float(cnt_same_good)/total_same))
#print("same bad : {}".format(float(cnt_same_bad)/total))
#print(cnt_other_good,cnt_other_bad)
total = cnt_other_bad + cnt_other_good
#print("other good : {}".format(float(cnt_other_good)/total))
#print("other bad : {}".format(float(cnt_other_bad)/total))

#print("connect time : ",connect_time/total_time)

print("{},{},{}\n".format(float(cnt_same_good)/total_same,float(cnt_other_good)/total,connect_time/total_time))