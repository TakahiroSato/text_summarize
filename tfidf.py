# -*- coding: utf-8 -*-
"""
Created on Sat May 12 18:09:53 2018

@author: futur
"""

"""
tf-idfは、文書中に含まれる単語の重要度を評価する手法の1つであり、
主に情報検索やトピック分析などの分野で用いられている。
tf-idfは、
tf（英: Term Frequency、単語の出現頻度）と
idf（英: Inverse Document Frequency、逆文書頻度）の二つの指標に基づいて計算される。(Wikipedia)
"""
import math
import numpy as np
#import fastText as ft
from scipy.spatial import distance
#from gensim.models.wrappers.fasttext import FastText
from janome_segmenter import word_segmenter_ja

def word2id(bow, word_id):
    for w in bow:
        if w not in word_id:
            word_id[w] = len(word_id)
            
    return word_id


def compute_tf(sentences, word_id):
    tf = np.zeros([len(sentences), len(word_id)])
    
    for i in range(len(sentences)):
        for w in sentences[i]:
            tf[i][word_id[w]] += 1
    
    
    return tf


def compute_df(sentences, word_id):
    df = np.zeros(len(word_id))
    
    for i in range(len(sentences)):
        exist = {}
        for w in sentences[i]:
            if w not in exist:
                df[word_id[w]] += 1
                exist[w] = 1
            else:
                continue
            
    return df


def compute_idf(sentences, word_id):
    idf = np.zeros(len(word_id))
    df = compute_df(sentences, word_id)
    
    for i in range(len(df)):
        idf[i] = np.log(len(sentences)/df[i]) + 1
        
    return idf


def compute_tfidf(sentences):
    word_id = {}
    
    for sent in sentences:
        word_id = word2id(sent, word_id)

    tf = compute_tf(sentences, word_id)
    idf = compute_idf(sentences, word_id)

    tf_idf = np.zeros([len(sentences), len(word_id)])
    
    for i in range(len(sentences)):
        tf_idf[i] = tf[i] * idf
        
    return tf_idf


def compute_cosine(v1, v2):
    d = distance.cosine(v1, v2)
    if math.isnan(d):
        d = 1
        
    return 1 - d



def sent2vec(bow, model_w):
    vector = np.zeros(300)
    N = len(bow)
    segments = word_segmenter_ja(bow)
    
    for segment in segments:
        try:
            vector += model_w[segment]
        except:
            continue
      
    vector = vector / float(N)
    
    return vector



def compute_word2vec(sentences, model):
    #model_w = ft.load_model('./model/wiki.ja/wiki.ja.bin')
    model_w = model #FastText.load_fasttext_format('./model/wiki.ja/wiki.ja')
    vector = np.zeros([len(sentences), 300])

    for i in range(len(sentences)):
        vector[i] = sent2vec(sentences[i], model_w)
        
    return vector
    

if __name__ == "__main__":
    pass