# -*- coding: utf-8 -*-
"""
Created on Sun May 10 03:57:26 2020

@author: Rahul Patil
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot
import sqlite3
import os

def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn

    
def main(database):
    conn = create_connection(database)
    df = pd.read_sql_query("SELECT * FROM Tweet_data", conn)
    df2 = pd.read_sql_query("SELECT * FROM Tesla_Stock", conn)
    #display(df2)
    scores = []
    list_of_tweets = list(df['Tweet_Text'])
    for tweet in list_of_tweets:
        processed_data = clean_tweets(tweet)
        sentiment_score = SentimentAnalyzer(processed_data)
        scores.append(sentiment_score)
    df1 = pd.DataFrame(scores)
    df1.columns = ['Score_Polarity', 'Score']
    #display(df1)
    merged_df = df.merge(df1, left_index = True, right_index = True)
    merged_df['Date_Created'] = merged_df['Creation_dt'].map(lambda x: x.strftime('%B %d,%Y'))
    merged_df.drop['Creation_dt']
    grouped_df = merged_df.groupby('Date_Created')
    display(merged_df)
    merged_df.to_sql('Scores', con = sqlite3.connect("SentimentAnalysis.db"), if_exists = 'replace')



main('SentimentAnalysis.db')    
