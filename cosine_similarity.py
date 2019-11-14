# -*- coding: utf-8 -*-
"""
Created on Fri May 11 16:59:17 2018

@author: TakahiroSato
"""

from collections import Counter
import math


def idf_modified_cosine(sentences, sentence1, sentence2):
    """
    2文間のコサイン類似度を計算
    @param  sentence1: list
        文1([w1,w2,w3]のような単語リスト)
    @param  sentence2: list
        文2([w1,w2,w3]のような単語リスト)
    @param  sentences: list
        文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような単語リスト)
    @return : float
        コサイン類似度
    """
    
    tf1 = compute_tf(sentence1)
    tf2 = compute_tf(sentence2)
    idf_metrics = compute_idf(sentences)
    return cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics)


def compute_tf(sentence):
    """
    TFを計算
    @param  sentence: list
        文([w1,w2,w3]のような単語リスト)
    @return : list
        TFリスト
    """
    
    tf_values = Counter(sentence)
    tf_metrics = {}
    
    max_tf = find_tf_max(tf_values)
    
    for term, tf in tf_values.items():
        tf_metrics[term] = tf/max_tf
        
    return tf_metrics


def find_tf_max(terms):
    """
    単語の最大出現頻度を探索
    @param  terms: list
        単語の出現頻度
    @return : int
        単語の最大出現頻度
    """
    
    return max(terms.values()) if terms else 1


def compute_idf(sentences):
    """
    文章中の単語のIDF値を計算
    @param sentences: list
        文章([[w1,w2,w3],[w1,w3,w4,w5],..]のような単語リスト)
    @return: list
        IDFリスト
    """
    
    idf_metrics = {}
    sentences_count = len(sentences)
    
    for sentence in sentences:
        for term in sentence:
            if term not in idf_metrics:
                n_j = sum(1 for s in sentences if term in s)
                idf_metrics[term] = math.log(sentences_count / float(1 + n_j))
                
                
    return idf_metrics


def cosine_similarity(sentence1, sentence2, tf1, tf2, idf_metrics):
    """
    コサイン類似度を計算
    @param  sentence1: list
        文1([w1,w2,w3]のような単語リスト)
    @param  sentence2: list
        文2([w1,w2,w3]のような単語リスト)
    @param  tf1: list
        文1のTFリスト
    @param  tf2: list
        文2のTFリスト
    @param  idf_metrics: list
        文章のIDFリスト
    @return : float
        コサイン類似度
    """
    
    unique_words1 = set(sentence1)
    unique_words2 = set(sentence2)
    common_words = unique_words1 & unique_words2
    
    numerator = sum((tf1[t] * tf2[t] * idf_metrics[t] ** 2) for t in common_words)
    denominator1 = sum((tf1[t] * idf_metrics[t]) ** 2 for t in unique_words1)
    denominator2 = sum((tf2[t] * idf_metrics[t]) ** 2 for t in unique_words2)
    
    if denominator1 > 0 and denominator2 > 0:
        return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))
    else:
        return 0.0
    