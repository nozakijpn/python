import os

kana4 = "お願い o n e g a i\nし sh i\nます m a s u\n"
ref2 = "お願い+オネガイ+名詞+サ変接続 し+シ+動詞+自立/サ変・スル/連用形 ます+マス+助動詞/特殊・マス/基本形\n"
word3 = "お願い し ます\n"

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
newsnum = [345,519,608,520,520]

fmv = open("./mvwav.sh","w")

os.system("rm ./dic -r")

os.system("mkdir ./dic")
for i,newsname in enumerate(newslist):
	bunkatu = int(newsnum[i]/7)
	print(bunkatu)
	roop_cnt = 0
	now_dic = 1
	os.system("mkdir ./dic/{}".format(newsname))
	os.system("mkdir ./dic/{2}/{0}{1}".format(newsname,now_dic,newsname))
	fkana4 = open("./dic/{2}/{0}{1}/{0}{1}.kana4".format(newsname,now_dic,newsname),"w")
	fref2 = open("./dic/{2}/{0}{1}/{0}{1}.ref2".format(newsname,now_dic,newsname),"w")
	fword3 = open("./dic/{2}/{0}{1}/{0}{1}.word3".format(newsname,now_dic,newsname),"w")

	for j in range(newsnum[i]):
		roop_cnt += 1
		if(roop_cnt == bunkatu and now_dic != 7):
			now_dic += 1
			os.system("mkdir ./dic/{2}/{0}{1}".format(newsname,now_dic,newsname))
			fkana4 = open("./dic/{2}/{0}{1}/{0}{1}.kana4".format(newsname,now_dic,newsname),"w")
			fref2 = open("./dic/{2}/{0}{1}/{0}{1}.ref2".format(newsname,now_dic,newsname),"w")
			fword3 = open("./dic/{2}/{0}{1}/{0}{1}.word3".format(newsname,now_dic,newsname),"w")
			roop_cnt = 0
		fmv.write("cp /home/nozaki/newsdata/cutwav/vdet_wav/{}_{:04d}.wav ./dic/{}/{}{}/{}{}_{}.wav\n".format(newsname,j+1,newsname,newsname,now_dic,newsname,now_dic,j+1))

		fkana4.write(kana4)
		fref2.write("{}-{:04d}\n".format(newsname,j+1))
		fref2.write(ref2)
		fword3.write(word3)

