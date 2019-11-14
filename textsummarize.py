# -*- coding: utf-8 -*-
"""
Created on Mon May 14 00:09:49 2018

@author: futur
"""

import lexrank

def summarize(txtfilepath, maxlength, model):
    text_file = open(txtfilepath, "r", encoding="UTF-8")
    text = text_file.read()
    text_file.close()
    
    sentences = list(sent_splitter_ja(text))
    rank = lexrank.lexrank(sentences, len(sentences), 0.5, "word2vec", model)
    dict = {}
    for i in range(len(sentences)):
        dict[sentences[i]] = rank[i]

    result = {}
    for k, v in sorted(dict.items(), key=lambda x: -x[1]):
        result[k] = v

    ret = ""
    keys = list(result.keys())
    while len(ret + keys[0]) < maxlength:
        ret += keys[0] + "\n"
        keys.pop(0)
        if len(keys) == 0:
            break
    
    return ret


# ref: https://github.com/recruit-tech/summpy/blob/master/summpy/tools.py
def sent_splitter_ja(text, delimiters=set(u'。．？！\n\r'),
                     parenthesis=u'（）「」『』“”'):
    '''
    Args:
      text: unicode string that contains multiple Japanese sentences.
      delimiters: set() of sentence delimiter characters.
      parenthesis: to be checked its correspondence.
    Returns:
      generator that yields sentences.
    '''
    paren_chars = set(parenthesis)
    close2open = dict(zip(parenthesis[1::2], parenthesis[0::2]))
    pstack = []
    buff = []

    for i, c in enumerate(text):
        c_next = text[i+1] if i+1 < len(text) else None
        # check correspondence of parenthesis
        if c in paren_chars:
            if c in close2open:  # close
                if len(pstack) > 0 and pstack[-1] == close2open[c]:
                    pstack.pop()
            else:  # open
                pstack.append(c)

        buff.append(c)
        if c in delimiters:
            if len(pstack) == 0 and c_next not in delimiters:
                yield ''.join(buff)
                buff = []

    if len(buff) > 0:
        yield ''.join(buff)