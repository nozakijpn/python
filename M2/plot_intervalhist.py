import glob
import numpy as np
import sys
import matplotlib.pyplot as plt


#th_time = float(sys.argv[1])
#path_lbl = "/home/nozaki/tooltxt" 
path_lbl = "./vdet_lbl_v" 
#path_lbl = "/home/nozaki/tooltxt" 
list_lbl = glob.glob("{}/*NHK*lbl".format(path_lbl))
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

th_time = 1.5
shortest = 0
short_cnt=0
list_same,list_other = [],[]
list_per_same,list_per_other = [],[]
cnt_same,cnt_other,cnt_shortest_same,cnt_shortest_other = 0,0,0,0

#config of histgram
bins = 100


for newspath in list_lbl:
    f = open(newspath,"r")
    st,end,sp = [],[],[]
    for i,line in enumerate(f.readlines()):
        """
        if(newspath.find("NHK1030") != -1  or newspath.find("NHK0829") != -1):
            f.close()
            break
        """
        line = line.split()
        st.append(float(line[0]))
        end.append(float(line[1]))
        sp.append(line[2])
        
        if(i!=0):
            if(end[i-1]<st[i]):
                if(sp[i-1] == sp[i]):
                    list_same.append(st[i]-end[i-1])
                    cnt_same += 1
                elif(sp[i-1] != sp[i]):
                    cnt_other += 1
                    list_other.append(st[i]-end[i-1])
                    if(st[i]-end[i-1] < th_time):
                        ti = st[i]
                        #print(newspath,sp[i-1],sp[i],end[i-1],st[i],st[i]-end[i-1])
                        #print(newspath,sp[i-1],sp[i],end[i-1],st[i],"{}:{}".format(int(ti/60),int(ti)%60))
                        #print("     {},{}".format(end[i-1]-st[i-1],end[i]-st[i]))
                        short_cnt+=1
                        if(end[i-1]-st[i-1] < 0.5 or end[i]-st[i] < 0.5):
                            #print("     {},{}".format(end[i-1]-st[i-1],end[i]-st[i]))
                            shortest += 1
                        else:
                            print(newspath,sp[i-1],sp[i],end[i-1],st[i],"{}:{}".format(int(ti/60),int(ti)%60))
                            print("     {},{}".format(end[i-1]-st[i-1],end[i]-st[i]))
                    """
                    if(sp[i-1] == "none" or sp[i] == "none"):
                        print(newspath,sp[i-1],sp[i],end[i-1],st[i],st[i]-end[i-1])
                        shortest += 1
                    """
list_same = np.array(list_same)
list_other = np.array(list_other)

print(np.average(list_same))
print(np.average(list_other))

percent_same = np.sum(list_same < th_time)/float(np.shape(list_same)[0])
percent_other = np.sum(list_other > th_time)/float(np.shape(list_other)[0])
list_per_same.append(percent_same)
list_per_other.append(percent_other)

plt.xlabel("time[s]")
plt.ylabel("Num of speech data[%]")
plt.title("histogram of time plot (same speaker)")
plt.hist(list_same,bins,range=(0,10),normed=True)
plt.show()

plt.xlabel("time[s]")
plt.ylabel("Num of speech data[%]")
plt.title("histogram of time plot (different speaker)")
plt.hist(list_other,bins,range=(0,10),normed=True)
plt.show()

print(len(list_lbl))
print(len(list_same))
print("same ave",np.average(np.array(list_same)))
print("same std",np.std(np.array(list_same)))
print(len(list_other))

print("different ave",np.average(np.array(list_other)))
print("different std",np.std(np.array(list_other)))

print("percent of same min{}sec\n".format(th_time),np.sum(list_same < th_time)/float(cnt_same))
print("percent of different min{}sec\n".format(th_time),np.sum(list_other < th_time)/float(cnt_other))

print(shortest)
print(float(shortest)/short_cnt)