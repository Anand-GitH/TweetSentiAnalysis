# -*- coding: utf-8 -*-
"""
Created on Sun May 10 03:21:36 2020

@author: Rahul Patil
"""

import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer



stop_words = set(stopwords.words('english'))
stemmer= PorterStemmer()




def tweet_preprocessing(tweet):
    out = []
    tweet_str = tweet
    tweet_str = tweet_str.lower()
    #tweet_numbers = ''.join([i for i in tweet_str if not i.isdigit()])
    tweet_whitespaces = tweet_str.strip()
    tweet_tokenize = word_tokenize(tweet_whitespaces)
    tokenize_result = [word for word in tweet_tokenize if not word in stop_words]  
    for word in tokenize_result:
        x = stemmer.stem(word)
        out.append(x)
    
    list_to_str = ' '.join([str(ele) for ele in out])
    return list_to_str


    
    
tweet_preprocessing('Box A contains 3 red and 5 white balls, while Box B contains 4 red and 2 blue balls.')