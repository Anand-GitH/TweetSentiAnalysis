###################################################################################
#processtweetdata reads the tweet data from the dataset and extracts
#User,Tweet and the Tweet date and time
#Inserts formatted data into table
###################################################################################
from IPython.display import display, HTML
import sqlite3
from sqlite3 import Error
import json
import os
import datetime
import pandas as pd
from genericdbcalls import create_table
from genericdbcalls import execute_sql_statement
from genericdbcalls import drop_table

month_dict={'January':1,
            'February':2,
            'March':3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12}

#function to read tweets from the file and returns as list
def read_tweetdata(filename):
    tweetlist=list()
    with open(filename, 'r') as json_file:
        json_list = list(json_file)
        
    for each_line in json_list:
        eachtweet = json.loads(each_line)
        eachrec=(eachtweet['UserName'],eachtweet['CreatedAt'],eachtweet['Text'])
        tweetlist.append(eachrec)
        
    return tweetlist


#function to insert tweets into table
def insert_tweetdata(conn, values):
    try:
        sql = ''' INSERT INTO Tweet_Data(ID,User_ID,Tweet_Text,Creation_dt) VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, values)
        return cur.lastrowid  
    except Error as e:
        print(e)
  
#function to query all tweets
def query_tweetdata(conn):
    sql = ''' SELECT * FROM Tweet_Data;'''
    cur = conn.cursor()
    cur.execute(sql)
    alltweets = cur.fetchall()

    return alltweets

#Function to query data using pandas
def query_tweetdatapd(conn):
    sql_statement='''SELECT ID,USER_ID,substr(Tweet_Text,1,25) Tweet,Creation_dt FROM Tweet_Data order by Creation_dt limit 5;'''
    df = pd.read_sql_query(sql_statement, conn)
    display(df)

#function to format the tweet date
def get_tweetdate(unformatted):
    timedatasplit=unformatted.split(" ")
    month=month_dict[timedatasplit[0]]
    day=int(timedatasplit[1].strip(','))
    year=int(timedatasplit[2])
    if timedatasplit[4][5:]=="PM" and int(timedatasplit[4][:2])!=12:
        HH=int(timedatasplit[4][:2])+12
    else:
        HH=int(timedatasplit[4][:2])
                
    MM=int(timedatasplit[4][3:5])
    tdate=datetime.datetime(year,month,day,HH,MM)
    return tdate
            
#function to read data from file,pre process and load to database
def processtweetdata(conn,dataset):
    try:
        tweets_list=read_tweetdata(dataset)
        
        drop_table_sql='''DROP TABLE Tweet_Data;'''
        drop_table(conn,drop_table_sql)
        
        tweet_table="CREATE TABLE Tweet_data (ID INTEGER PRIMARY KEY,User_ID TEXT,Tweet_Text TEXT,Creation_dt DATE)"
        create_table(conn,tweet_table)
        
        count=0
        with conn:
            for eachrec in tweets_list:
                tweetdata=(count+1,eachrec[0],eachrec[2],get_tweetdate(eachrec[1]))
                insert_tweetdata(conn,tweetdata)
                count+=1
        
    except Error as e:
        print(e)