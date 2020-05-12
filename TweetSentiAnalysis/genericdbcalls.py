###################################################################################
#Generic Database Methods
#To Create Table
#To Drop Table
#To Execute SQL Statement
###################################################################################
from IPython.display import display, HTML
import sqlite3
import os
from sqlite3 import Error

#function to create a sqllite db file and returns connection
def create_connection(db_file, delete_db=False):
   if delete_db and os.path.exists(db_file):
        os.remove(db_file)
    
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       conn.execute("PRAGMA foreign_keys = 1")
   except Error as e:
       print(e)
    
   return conn

#function to Create table 
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)
    rows = cur.fetchall()
    return rows

#function to drop the table
def drop_table(conn, drop_table_sql):
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except Error as e:
        print(e)    

