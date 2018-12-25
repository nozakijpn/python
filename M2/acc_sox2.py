from nozaki_module import iv_module
import matplotlib.pyplot as plt
import numpy as np

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
wavpath = "/home/nozaki/newsdata/cutwav/vdet_wav"

ivmodule = iv_module("",wavpath)

same,other=[],[]
time = []
list_score=[]
for i in range(50,201,1):
	total_time,connect_time=0,0
	time.append(i*0.01)
	list_soxed,list_wav = [],[]
	f = open("/home/nozaki/github/python/M2/txt_for_decide_th/rename_{}.txt".format(i),"r")
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
			#print(list_wav[idnum-1],list_wav[idnum])
			if(list_soxed[idnum-1] != list_soxed[idnum]):
				cnt_other_good += 1
				#print("good\n")
			else:
				cnt_other_bad += 1
				#print("bad\n")
		f.close()

	for newsname in newslist:
		f = open("/home/nozaki/newsdata/txt/change_speaker_vdet/{}_same.txt".format(newsname),"r")
		lines = f.readlines()
		for line in lines:
			line = line.replace("\n","")
			idnum = list_wav.index(line)
			#print(list_wav[idnum-1],list_wav[idnum])
			filepath = "{}/{}.wav".format(wavpath,list_wav[idnum])

			total_time += ivmodule.get_wav_time(filepath)
			if(list_soxed[idnum-1] == list_soxed[idnum]):
				cnt_same_good += 1
				#print("good\n")
				connect_time += ivmodule.get_wav_time(filepath)
			else:
				cnt_same_bad += 1
				#print("bad\n")
		f.close()
	total = cnt_same_bad + cnt_same_good
	"""
	print(cnt_same_good,cnt_same_bad)
	print("same good : {}".format(float(cnt_same_good)/total))
	print("same bad : {}".format(float(cnt_same_bad)/total))
	print(cnt_other_good,cnt_other_bad)
	"""
	total = cnt_other_bad + cnt_other_good
	"""
	print("other good : {}".format(float(cnt_other_good)/total))
	print("other bad : {}".format(float(cnt_other_bad)/total))
	"""

	same.append(connect_time*100/total_time)
	other.append(float(cnt_other_good)*100/total)
	list_score.append(connect_time*100/total_time + float(cnt_other_good)*100/total)
	#print(i,connect_time/total_time,float(cnt_other_good)/total)

list_score = np.array(list_score)
print(np.argmax(list_score),np.max(list_score))

plt.xlabel("time[s]")
plt.ylabel("Acc[%]")
plt.plot(time,same) 
plt.show()

plt.xlabel("time[s]")
plt.ylabel("Acc[%]")
plt.plot(time,other) 
plt.show()

