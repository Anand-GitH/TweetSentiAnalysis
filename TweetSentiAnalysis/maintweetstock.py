###################################################################################
#Start of the project
#Loads Elon Musk tweet data
#Loads Tesla Stock data
#Cleans tweet data and applies sentiment analysis
#Plots correlation of plots of tweet v/s stock prices
###################################################################################
from IPython.display import display, HTML
import pandas as pd
import numpy as np
import sqlite3
import os
import matplotlib.pyplot
from sqlite3 import Error
from processtweetdata import processtweetdata
from processtweetdata import query_tweetdatapd
from processteslastkdata import processteslastkdata
from processteslastkdata import query_telsastkdatapd
from calculatetweetscores import calculatetweetscores
from plotsaresults import plotpiechart
from plotsaresults import plotdailystkprvar
from plotsaresults import plotscores
from plotsaresults import plotfinalinteract
from genericdbcalls import create_connection
from plotsaresults import plotstatisticssa
from plotsaresults import plotstatisticssayear

#StartTweetAnalysis - Start function of Project
def maintweetstock():
  elontweetdataset="user-tweets.jsonl"
  teslastockdataset="TSLA.csv"
  dbfile="SentimentAnalysis.db"

  conn= create_connection(dbfile,True)
  try: 
    with conn:
      processtweetdata(conn,elontweetdataset)
      processteslastkdata(conn,teslastockdataset)
      calculatetweetscores(conn)
    
    conn.commit()

    query_tweetdatapd(conn)
    query_telsastkdatapd(conn)
    plotpiechart(conn)
    plotdailystkprvar(conn)
    plotscores(conn)
    plotstatisticssa(conn)
    plotstatisticssayear(conn)
    plotfinalinteract(conn)
    
  except Error as e:
    print(e)
  finally:
    if(conn):
      conn.close()


##Start by calling explicitly
maintweetstock()