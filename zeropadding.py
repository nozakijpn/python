#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 16:05:09 2018

@author: nozaki
"""

"""
f = open("rename.sh","w")

for i in range(1,1000):
    f.write("mv NHK1112_{0:04d}.txt NHK1112_{0:04d}.y\n".format(i,i))
    
for i in range(1,1000):
    f.write("mv NHK1113_{0:04d}.txt NHK1113_{0:04d}.y\n".format(i,i))

for i in range(1,1000):
    f.write("mv NHK1114_{0:04d}.txt NHK1114_{0:04d}.y\n".format(i,i))

for i in range(1,1000):
    f.write("mv NHK0826_{0:04d}.txt NHK0826_{0:04d}.y\n".format(i,i))


"""
filename = "NHK1113"
path = "/home/nozaki/speaker_clustering/news_kotae/{0}".format(filename)


f = open("{0}/anchor2.txt".format(path))
lines2 = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
f.close()

f = open("{0}/re_anchor2.txt".format(path),"w")
for line in lines2:
    line = line.replace("\n","")
    f.write("{0}_{1:04d}\n".format(filename,int(line)))
    
f.close()
