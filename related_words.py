# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:58:21 2018

@author: TakahiroSato
"""
import gensim
import janome_segmenter

def get_related_words(source, model, topn=10):
    tokens = janome_segmenter.word_segmenter_ja(source)
    for token in tokens:
        try:
            model[token]
        except:
            tokens.remove(token)
            pass
        
    result = model.most_similar(positive=tokens, topn=topn)
    ret = []
    for val in result:
        ret.append(val[0])
    
    return ret