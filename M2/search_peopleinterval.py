import glob
import numpy as np
import sys

#th_time = float(sys.argv[1])
path_lbl = "./tooltxt/vlbl"  
list_lbl = glob.glob("{}/*lbl".format(path_lbl))
list_hm = []

weight1,weight2 = 1,2

def weight_mean(x,y):
	if(x == 0 or y == 0):
		x = 0.000001
		y = 0.000001
	return ((x*weight1)+(y*weight2))/(weight1+weight2)

def harmonic_mean(x,y):
	if(x == 0 or y == 0):
		x = 0.000001
		y = 0.000001
	return 2/((1/x)+(1/y))

for th_time in range(0,300,1):
	th_time = th_time*0.01
	list_same,list_other = [],[]
	list_per_same,list_per_other = [],[]

	for newspath in list_lbl:
		f = open(newspath,"r")
		st,end,sp = [],[],[]
		for i,line in enumerate(f.readlines()):
			line = line.split()
			st.append(float(line[0]))
			end.append(float(line[1]))
			sp.append(line[2])

			if(i!=0):
				if(end[i-1]<st[i]):
					if(sp[i-1] == sp[i]):
						list_same.append(st[i]-end[i-1])
					elif(sp[i-1] != sp[i]):
						list_other.append(st[i]-end[i-1])

	list_same = np.array(list_same)
	list_other = np.array(list_other)

	#print(np.average(list_same))
	#print(np.average(list_other))

	percent_same = np.sum(list_same < th_time)/float(np.shape(list_same)[0])
	percent_other = np.sum(list_other > th_time)/float(np.shape(list_other)[0])
	list_per_same.append(percent_same)
	list_per_other.append(percent_other)
	list_hm.append(weight_mean(percent_same,percent_other))
	print(int(th_time*100),percent_same,percent_other,weight_mean(percent_same,percent_other))

list_hm = np.array(list_hm)
print(np.argmax(list_hm)*0.01,np.max(list_hm))