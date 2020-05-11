###################################################################################
#Apply sentiment analysis on each tweet and calculate its scores
#to classify it as 
#Positive
#Negative
#Neutral
###################################################################################
import pandas as pd
import numpy as np
from preproctweets import clean_tweets
from sanalysis import sentimentanalyzer

def calculatetweetscores(conn):
    
    df = pd.read_sql_query("SELECT * FROM Tweet_Data", conn)
 
    scores = []
    list_of_tweets = list(df['Tweet_Text'])
    
    for tweet in list_of_tweets:
        processed_data = clean_tweets(tweet)
        sentiment_score = sentimentanalyzer(processed_data)
        scores.append(sentiment_score)

    df1 = pd.DataFrame(scores)
    df1.columns = ['Score_Polarity', 'Score']
    
    merged_df = df.merge(df1, left_index = True, right_index = True)
    
    #merged_df['Date_Created'] = merged_df['Creation_dt']
    #merged_df.drop('Creation_dt')
    
    #grouped_df = merged_df.groupby('Date_Created')
    
    merged_df.to_sql('Tweet_Scores',conn, if_exists = 'replace')
