# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:17:15 2018

@author: TakahiroSato
"""

import sys
import related_words
import pickle
import csv

args = sys.argv

with open(args[1], mode='rb') as f:
    model = pickle.load(f)

source_path = args[2]
source_file = open(source_path, "r", encoding="UTF-8")
source = source_file.read()
source_file.close()
    
suggested_words = related_words.get_related_words(source, model)

f = open(args[3], 'w', encoding="UTF-8")
writer = csv.writer(f, lineterminator='\n', quoting=csv.QUOTE_ALL)
writer.writerow(suggested_words)
f.close()
