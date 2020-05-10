# -*- coding: utf-8 -*-
"""
Created on Sun May 10 03:41:02 2020

@author: Rahul Patil
"""

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

analyzer = SentimentIntensityAnalyzer()

def SentimentAnalyzer(tweet):
    tweet_score = []
    
    score = analyzer.polarity_scores(tweet)
    tweet_score.append(score)
    df = pd.DataFrame(tweet_score)
    for i, row in df.iterrows():
        if row['compound']<0:
            row['neg'] = abs(row['neg']) + abs(row['compound'])
        elif row['compound'] > 0:
            row['pos'] = row['pos'] + row['compound']
    df.drop('compound', axis = 1, inplace = True)
    for i,rows in df.iterrows():
        if row['pos'] > row['neg'] and row['pos'] > row['neu']:
            print("positive", row['pos'])
            return ("positive", row['pos'])
            
        elif row['neg']>row['pos'] and row['neg'] > row['neu']:
            print("negative", row['neg'])
            return ("negative", row['neg'])
            
        else:
            print("neutral", row['neu'])
            return ("neutral", row['neu'])
            


SentimentAnalyzer('Thank you for sending my baggage to CityX and flying me to CityY at the same time. Brilliant service. #thanksGenericAirline')

