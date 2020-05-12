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
from genericdbcalls import create_table
from genericdbcalls import execute_sql_statement
from genericdbcalls import drop_table

def calculatetweetscores(conn):
    
    sql_statement='''DROP TABLE Tweet_Scores;'''
    drop_table(conn,sql_statement)

    sql_statement='''CREATE TABLE Tweet_Scores(ID INTEGER PRIMARY KEY,Score_Polarity TEXT,Score REAL);'''
    create_table(conn,sql_statement)

    df = pd.read_sql_query("SELECT * FROM Tweet_Data", conn)
 
    scores = []
    list_of_tweets = list(df['Tweet_Text'])
    
    for tweet in list_of_tweets:
        processed_data = clean_tweets(tweet)
        sentiment_score = sentimentanalyzer(processed_data)
        scores.append(sentiment_score)

    df1 = pd.DataFrame(scores)
    df1.columns = ['Score_Polarity', 'Score']

    df.drop(['User_ID','Tweet_Text','Creation_dt'],axis=1)
    
    merged_df = df.merge(df1, left_index = True, right_index = True)
    
    merged_df=merged_df.drop(['User_ID','Tweet_Text','Creation_dt'],axis=1)
    merged_df=merged_df.rename_axis(None)
        
    merged_df.to_sql('Tweet_Scores',conn,index=False,if_exists = 'append')

