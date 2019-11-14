# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:35:18 2018

@author: TakahiroSato
"""
import sys
import textsummarize
import pickle
import codecs

args = sys.argv

with open(args[1], mode='rb') as f:
    model = pickle.load(f)

source = args[2]
length = int(args[3])
summary = textsummarize.summarize(source, length, model)
target = codecs.open(args[4], 'w', 'utf-8')
target.write(summary)
target.close()
