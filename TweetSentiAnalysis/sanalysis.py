###################################################################################
#Sentimentanalyzer uses library vaderSentiment
#which give plority scores of tweets
###################################################################################
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

analyzer = SentimentIntensityAnalyzer()

def sentimentanalyzer(tweet):
    
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
            return ("positive", row['pos'])
            
        elif row['neg']>row['pos'] and row['neg'] > row['neu']:
            return ("negative", row['neg'])
            
        else:
            return ("neutral", row['neu'])
