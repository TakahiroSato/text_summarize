# -*- coding: utf-8 -*-
import numpy as np
import tfidf

def lexrank(sentences, N, threshold, vectorizer, model):
    """
    LexRankで文章を要約する．
    @param  sentences: list
        文章 e.g.) [u'こんにちは．', u'私の名前は佐藤です．', ... ]
    @param  N: int
        文章に含まれる文の数
    @param  threshold: float
        隣接行列（類似度グラフ）を作成する際の類似度の閾値
    @param  vectorizer: string
        文のベクトル化の手法(tf-idf/word2vec)
    @return : L
        LexRankスコア
    """
    
    CosineMatrix = np.zeros([N, N])
    degree = np.zeros(N)
    L = np.zeros(N)
    
    if vectorizer == "tf-idf":
        vector = tfidf.compute_tfidf(sentences)
    elif vectorizer == "word2vec":
        vector = tfidf.compute_word2vec(sentences, model)
        
        
    # Computing Adjaceney Matrix
    for i in range(N):
        for j in range(N):
            CosineMatrix[i,j] = tfidf.compute_cosine(vector[i], vector[j])
            if CosineMatrix[i,j] > threshold:
                CosineMatrix[i,j] = 1
                degree[i] += 1
            else:
                CosineMatrix[i,j] = 0
                
    # Computing LexRank Score
    for i in range(N):
        for j in range(N):
            CosineMatrix[i,j] = CosineMatrix[i,j]*1.0 / (degree[i] if degree[i] != 0 else 1.0)
            
    L = PowerMethod(CosineMatrix, N, err_tol=10e-6)
    
    return L


def PowerMethod(CosineMatrix, N, err_tol):
    """
    べき乗法を行なう
    @param  CosineMatrix: list
        隣接行列
    @param  N: int
        入力文数
    @param  err_tol: float
        PowerMethodにより収束したと判定するための誤差許容値
    @return p: list
        固有ベクトル（LexRankスコア）
    """
    
    p_old = np.array([1.0/N]*N)
    err = 1.0
    
    while err > err_tol:
        p = np.dot(CosineMatrix.T, p_old)
        err = np.linalg.norm(np.subtract(p, p_old))
        p_old = p
        
    return p