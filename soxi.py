"""
You should make soxi.txt.Please do under command.
soxi -D *.wav > soxi.txt
"""

import numpy as np

th = 5 #time threshold[sec]

cnt = 0
f = open("./soxi.txt","r")

lines = f.readlines()
times = []
for i,line in enumerate(lines):
    times.append(float(line))
    if(float(line)<th):
        cnt += 1
print("average speech time:{:02f}[sec]".format(np.average(times)))
print("time threshold:{}[sec] percent:{:02f}[%]".format(th,float(cnt)*100/float(i+1)))
