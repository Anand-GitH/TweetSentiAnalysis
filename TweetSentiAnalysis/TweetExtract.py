from IPython.display import display, HTML
import pandas as pd
import sqlite3
from sqlite3 import Error
import tweepy
import datetime

def rename_dbfile(old_file, new_file):
    import os
    if os.path.exists(old_file):
        os.rename(old_file, new_file)


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


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def drop_table(conn, drop_table_sql):
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except Error as e:
        print(e)
        
    
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)

    rows = cur.fetchall()

    return rows

auth = tweepy.OAuthHandler('NFR3qzSeoBC7OXWRaQTV5jT1R', 'Nq4BuPBqNrCG3xte2msAaE9fSLs8Ws0rSouavZ37ph1Rj05K63')
auth.set_access_token('3965026341-hlM3KoeLLyBFlUQDPj9jm2fvsDWwuc8KnA5YryV', '8Akgzg33ho671emEfxxw2obpqht5qoq2h2NwG4rUQ35Ir')
username='ElonMusk'

api = tweepy.API(auth)

tweets = api.user_timeline(screen_name=username, 
                           # 200 is the maximum allowed count
                           count=5000,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )

print(len(tweets))
for tweet in tweets[:3]:
    print(tweet.id, "------",tweet.created_at,"-----", tweet.full_text)


    