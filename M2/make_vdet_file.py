import glob
import os
from statistics import mode
import numpy as np

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]

vdetpath = "/home/nozaki/github/python/M2/vdet_module"
wavpath = "/home/nozaki/newsdata/cutwav/vdet_interval_16k"


for newsname in newslist:
	filelist = glob.glob("{}/{}*wav".format(wavpath,newsname))
	filelist.sort()
	fout = open("{}_vdet.txt".format(newsname),"w")
	for file in filelist:
		file = file.replace(".wav","")
		print("now {}".format(file))
		os.system("{}/vdetMar4w_tomi_class2 -wav {}.wav -chn 1 -ini {}/ass.ini > vdet1.txt".format(vdetpath,file,vdetpath))
		os.system("{}/merge.pl vdet1.txt > vdet2.txt".format(vdetpath))

		f = open("vdet2.txt","r")
		lines = f.readlines()
		if not lines:
			lines = [5]
		print(lines)
		count = np.bincount(lines)
		mode = np.argmax(count)
		#fout.write("{} {}\n".format(file,mode(lines)))
		fout.write("{} {}\n".format(file,mode))
	fout.close()
