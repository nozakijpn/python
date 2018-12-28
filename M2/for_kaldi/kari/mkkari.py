import os

kana4 = "お願い o n e g a i\nし sh i\nます m a s u\n"
ref2 = "お願い+オネガイ+名詞+サ変接続 し+シ+動詞+自立/サ変・スル/連用形 ます+マス+助動詞/特殊・マス/基本形\n"
word3 = "お願い し ます\n"

vocab_test = "お願いonegai o n e g a i\nしshi sh i\nますmasu m a s u\n"
test_trans = "お願いonegai しshi ますmasu\n"

newslist = ["NHK0825","NHK0826","NHK1112","NHK1113","NHK1114"]
#newslist = ["HK0825","HK0826","HK1112","HK1113","HK1114"]
newsnum = [345,519,608,520,520]

fmv = open("./mvwav.sh","w")

os.system("rm ./dic -r")
os.system("mkdir ./dic")

os.system("rm ./meeting -r")
os.system("mkdir ./meeting")

fukunaga_text = open("./meeting/text","w")
fukunaga_wav_scp = open("./meeting/wav.scp","w")
fukunaga_utt2spk = open("./meeting/utt2spk","w")
fukunaga_spk2utt = open("./meeting/spk2utt","w")
fukunaga_0txt = open("./meeting/0.txt","w")

for i,newsname in enumerate(newslist):
	bunkatu = int(newsnum[i]/8)
	print(bunkatu)
	roop_cnt = 0
	now_dic = 1
	os.system("mkdir ./dic/{}".format(newsname))
	os.system("mkdir ./dic/{2}/{0}{1}".format(newsname,now_dic,newsname))
	fkana4 = open("./dic/{2}/{0}{1}/{0}{1}.kana4".format(newsname,now_dic,newsname),"w")
	fref2 = open("./dic/{2}/{0}{1}/{0}{1}.ref2".format(newsname,now_dic,newsname),"w")
	fword3 = open("./dic/{2}/{0}{1}/{0}{1}.word3".format(newsname,now_dic,newsname),"w")

	f_test_trans = open("./dic/{}/test_trans.txt".format(newsname),"w")
	f_test_spk2utt = open("./dic/{}/test.spk2utt".format(newsname),"w")
	f_test_wav = open("./dic/{}/test_wav.scp".format(newsname),"w")
	f_test_utt2spk = open("./dic/{}/test.utt2spk".format(newsname),"w")
	f_vocab_test = open("./dic/{}/vocab-test.txt".format(newsname),"w")
	f_test_spk2utt.write("{}{}".format(newsname,now_dic))
	if(newsname != "NHK0825"):
		fukunaga_spk2utt.write("\n")
	fukunaga_spk2utt.write("{}{}".format(newsname,now_dic))

	for j in range(newsnum[i]):
		roop_cnt += 1

		f_test_spk2utt.write(" {}_{:03d}".format(newsname,j+1))
		fukunaga_spk2utt.write(" {}_{:03d}".format(newsname,j+1))

		if(roop_cnt == bunkatu and now_dic != 8):
			now_dic += 1
			os.system("mkdir ./dic/{2}/{0}{1}".format(newsname,now_dic,newsname))
			fkana4 = open("./dic/{2}/{0}{1}/{0}{1}.kana4".format(newsname,now_dic,newsname),"w")
			fref2 = open("./dic/{2}/{0}{1}/{0}{1}.ref2".format(newsname,now_dic,newsname),"w")
			fword3 = open("./dic/{2}/{0}{1}/{0}{1}.word3".format(newsname,now_dic,newsname),"w")
			f_test_spk2utt.write("\n")
			f_test_spk2utt.write("{}{}".format(newsname,now_dic))
			fukunaga_spk2utt.write("\n")
			fukunaga_spk2utt.write("{}{}".format(newsname,now_dic))

			roop_cnt = 1
		fmv.write("sox /home/nozaki/newsdata/cutwav/vdet_wav/{}_{:04d}.wav -r 16000 ./dic/{}/{}{}/{}{}_{:03d}.wav\n".format(newsname,j+1,newsname,newsname,now_dic,newsname,now_dic,j+1))

		fkana4.write(kana4)
		fref2.write("{}-{:03d}\n".format(newsname,j+1))
		fref2.write(ref2)
		fword3.write(word3)

		f_test_trans.write("{}_{:03d} {}\n".format(newsname,j+1,test_trans))
		f_test_utt2spk.write("{}{}_{:03d} {}{}\n".format(newsname,now_dic,j+1,newsname,now_dic))
		f_vocab_test.write(vocab_test)

		fukunaga_text.write("{}_{:03d} {}".format(newsname,j+1,word3))
		fukunaga_wav_scp.write("{}{}_{:03d} cat /work/speech_recognition/kaldi/egs/csj/newsdata/{}/{}{}/{}{}_{:03d}.wav |\n".format(newsname,now_dic,j+1,newsname,newsname,now_dic,newsname,now_dic,j+1))
		fukunaga_utt2spk.write("{}{}_{:03d} {}{}\n".format(newsname,now_dic,j+1,newsname,now_dic))
		fukunaga_0txt.write("{}{}_{:03d}\n".format(newsname,now_dic,j+1))