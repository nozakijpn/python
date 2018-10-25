#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 11:37:44 2018

@author: nozaki
"""
anchorpath = "/home/nozaki/newsdata/txt/vdet_txt"
newslist = ["NHK0826","NHK1112","NHK1113","NHK1114"]

for newsname in newslist:
    f = open("{}/{}_anchorlist.txt".format(anchorpath,newsname),"r")
    lines = f.readlines()
    for line in lines:
        print("{}_{:04d}".format(newsname,int(line)))
    f.close