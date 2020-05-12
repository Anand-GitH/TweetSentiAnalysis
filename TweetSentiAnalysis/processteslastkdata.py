###################################################################################
#processteslastkdata reads the Tesla Stock data from the dataset and extracts
#Date,Open,Higher,Low,Close,Adj,Volume
#Inserts formatted data into table
###################################################################################
from IPython.display import display, HTML
import pandas as pd
import sqlite3
from sqlite3 import Error
from genericdbcalls import create_table
from genericdbcalls import execute_sql_statement
from genericdbcalls import drop_table

def insert_Tesla(conn, values):    
    sql = " INSERT INTO Tesla_Stock VALUES(?,?,?,?,?,?,?); "
    cur = conn.cursor()
    cur.execute(sql,values)
    return cur.lastrowid

#Function to query data using pandas
def query_telsastkdatapd(conn):
    sql_statement='''SELECT Date,Open,Higher,Low,Close,Adj,Volume FROM Tesla_Stock order by Date limit 5;'''
    df = pd.read_sql_query(sql_statement, conn)
    display(df)


def processteslastkdata(conn,dataset):
    try:
        Date =[]
        Op=[]
        Hig=[]
        Lo=[]
        Cl=[]
        AdCl=[]
        Vol=[]
        
        drop_table_sql='''DROP TABLE Tesla_Stock;'''
        drop_table(conn,drop_table_sql)

        create_Tesla_Stock_sql = """CREATE TABLE Tesla_Stock (
                                     Date TEXT  PRIMARY KEY NOT NULL,
                                     Open INTEGER  NOT NULL,
                                     Higher INTEGER   NOT NULL,
                                     Low INTEGER  NOT NULL,
                                     Close INTEGER  NOT NULL,
                                     Adj INTEGER  NOT NULL,
                                     Volume INTEGER    NOT NULL
                                     ); """

        create_table(conn, create_Tesla_Stock_sql)

        df = pd.read_csv(dataset)
        for value in df['Date']:
            Date.append(value)

        for value in df['Open']:
            value = round(value, 2)
            Op.append(value)
                        
        for value in df['High']:
            #print(type(value)) 
            #print(value)
            value = round(value, 2)
           # print(value)
            Hig.append(value)
        for value in df['Low']:
            value = round(value, 2)
            Lo.append(value)
            
        for value in df['Close']:
            value = round(value, 2)
            Cl.append(value)

        for value in df['Adj Close']:
            value = round(value, 2)
            AdCl.append(value)
            
        for value in df['Volume']:
            value = round(value, 2)
            Vol.append(value)

        minjoin = zip(Date,Op,Hig,Lo,Cl,AdCl,Vol)
        with conn:
            for kol in minjoin:
                insert_Tesla(conn, (kol[0],kol[1],kol[2],kol[3],kol[4],kol[5],kol[6]))        

    except Error as e:
        print(e)
