"""
remake.shで作ったwavファイルが短いためにivの精度が落ちた可能性があるため、
つなぎ合わせるのではなく、
つなぎ合わせる音声の最初から最後までの区間を全てsoxでtrimするプログラムを作成する
"""
import os
homepath = "/home/nozaki/github/python/M2"
wavpath = "/home/nozaki/newsdata/wav/"
savepath = "/home/nozaki/newsdata/cutwav/vdet_wav/"

f = open("{}/tooltxt/sox_trim.txt".format(homepath),"r")
lines = f.readlines()
newsname,wavnum,st,end = [],[],[],[]

for line in lines:
	line = line.split()
	print(line)

	#line = line[1].replace(wavpath,"")
	#line = line[2].replace(savepath,"")
	newsname.append(line[1])
	wavnum.append(line[2])
	st.append(line[4])
	end.append(float(line[4])+float(line[5]))

f.close()

f = open("{}/tooltxt/connect.txt".format(homepath),"r")
lines = f.readlines()

for line in lines:
	line_sp = line.split()
	if(line_sp[0] == "cp"):
		os.system(line)
		print(line)
	elif(line_sp[0] == "sox"):
		#line_sp[2] = line_sp[2].replace()
		idnum = wavnum.index(line_sp[2])
		sox_news = newsname[idnum]
		sox_st = st[idnum]

		idnum = wavnum.index(line_sp[-2])
		sox_end = end[idnum]

		soxed_wav = line_sp[-1]
		os.system("sox {} {} trim {} {}".format(sox_news,soxed_wav,sox_st,float(sox_end)-float(sox_st)))
		print("sox {} {} trim {} {}".format(sox_news,soxed_wav,sox_st,float(sox_end)-float(sox_st)))
f.close()