###################################################################################
#Plots for the project are built in this
#Pie Chart of tweet sentiments
#DailyStockvariations
#Final Interactive Plot showing details of Rise and Fall of Tesla Stock prices on 
#Elon musk tweets sentiments
###################################################################################
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import cufflinks as cf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plotpiechart(conn):
    sql_statement='''SELECT count(1) count 
                       FROM (SELECT t.ID,date(t.Creation_dt) TDate,t.Tweet_Text,t1.Score_Polarity,t1.Score,abs(close-open),
		                       CASE WHEN (close-open)<0 then 'D'
                               WHEN (close-open)>0 then 'I'
                               ELSE 'F'
                                END as stockstatus
	                           FROM Tesla_Stock ts,Tweet_data t,Tweet_Scores t1 where t.ID=t1.ID and date(t.Creation_dt)=ts.Date)
                               WHERE score_polarity=? and stockstatus=?
                               GROUP BY score_polarity,stockstatus'''
                               
    df1=pd.read_sql_query(sql_statement,conn,params=['negative','D'])
    df2=pd.read_sql_query(sql_statement,conn,params=['positive','I'])
    df3=pd.read_sql_query(sql_statement,conn,params=['neutral','F'])
    
    tweet_cnt=[df1['count'].tolist()[0],df2['count'].tolist()[0],df3['count'].tolist()[0]]
    tweet_status=['Negative tweets','Positive tweets','Neutral tweets']
    
    colors = ['orange','springgreen','red']
    patches, texts = plt.pie(tweet_cnt, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, tweet_status, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def plotdailystkprvar(conn):
    sql_statement='''select date,adj from Tesla_Stock where date>(select min(date(creation_dt)) from tweet_data) order by date;'''
    df=pd.read_sql_query(sql_statement,conn)
    df.set_axis(df['Date'], axis='index', inplace=True)
    df=df.drop(['Date'],axis=1)
    df['Adj'].plot(label='Tesla',figsize=(16,8),title='Tesla Stock Price - 2017 to Current',color='dodgerblue')
    plt.legend()
    plt.show()

def plotscores(conn):
    sql_statement='''select date(creation_dt) Date,score from Tweet_data t,Tweet_Scores t1 where t.ID=t1.ID order by date;'''
    df=pd.read_sql_query(sql_statement,conn)
    df.set_axis(df['Date'], axis='index', inplace=True)
    df=df.drop(['Date'],axis=1)
    df['Score'].plot(label='Tweet Scores',figsize=(16,8),title='Elon Musk Tweet Scores',color='orangered')
    plt.legend()
    plt.show()

def plotfinalinteract(conn):
    
    sql_statement='''select date,adj from Tesla_Stock where date>(select min(date(creation_dt)) from tweet_data) order by date;'''
    df=pd.read_sql_query(sql_statement,conn)

    sql_statement='''SELECT distinct Tdate,Tweet_Text,Score_Polarity,Adj,stockstatus
                      FROM (SELECT date(t.Creation_dt) TDate,t.Tweet_Text,t1.Score_Polarity,t1.Score,ts.Adj,
                              CASE WHEN (close-open)<0 then 'D'
                                   WHEN (close-open)>0 then 'I'
                                   ELSE 'F'
                                   END as stockstatus 
                              FROM Tesla_Stock ts,Tweet_data t,Tweet_Scores t1 where t.ID=t1.ID and date(t.Creation_dt)=ts.Date) 
                             WHERE Score_Polarity=? and stockstatus=? order by TDate;'''

    dfpos=pd.read_sql_query(sql_statement,conn,params=['positive','I'])
    dfneg=pd.read_sql_query(sql_statement,conn,params=['negative','D'])
    
    fig = go.Figure(layout_title_text="Tesla Stock Prices v/s Elon Musk Tweets Sentiments")
    
    fig.add_trace(go.Scatter(x=df["Date"].tolist(), y=df["Adj"].tolist(),
                    mode='lines',
                    name='Tesla Stock Price',
                    line = dict(color='rgb(102,102,102)')
                    ))
      
    fig.add_trace(go.Scatter(
        x=dfpos["TDate"],
        y=dfpos["Adj"],
        hovertext=dfpos["Tweet_Text"].tolist(),
        hoverinfo="text",
        mode='markers',
        name='PositiveTweet',
        marker=dict(
            color="#00CC96"
        ),
        showlegend=True
    ))
        
    fig.add_trace(go.Scatter(
        x=dfneg["TDate"],
        y=dfneg["Adj"],
        hovertext=dfneg["Tweet_Text"].tolist(),
        hoverinfo="text",
        mode='markers',
        name='NegativeTweet',
        marker=dict(
            color="#E45756"
        ),
        showlegend=True
    ))
    
    
    fig.show()
    
def plotstatisticssa(conn):
    sql_statement='''SELECT score_polarity,stockstatus,count(1) total 
                       FROM (SELECT distinct Tdate,Tweet_Text,Score_Polarity,Adj,stockstatus
                               FROM (SELECT date(t.Creation_dt) TDate,t.Tweet_Text,t1.Score_Polarity,t1.Score,ts.Adj,
                               CASE WHEN (close-open)<0 then 'D'
                               WHEN (close-open)>0 then 'I'
                               ELSE 'F'
                               END as stockstatus 
                               FROM Tesla_Stock ts,Tweet_data t,Tweet_Scores t1 
                               WHERE t.ID=t1.ID and date(t.Creation_dt)=ts.Date)) 
                      GROUP BY score_polarity,stockstatus;'''
                      
                      
    df=pd.read_sql_query(sql_statement,conn)
    incdata=df[df["stockstatus"]=="I"]
    decdata=df[df["stockstatus"]=="D"]
    flatdata=df[df["stockstatus"]=="F"]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=incdata["Score_Polarity"].tolist(),
        y=incdata["total"].tolist(),
        name='Rise in Stock Price',
        marker_color='rgb(139,224,164)'
    ))
    fig.add_trace(go.Bar(
        x=decdata["Score_Polarity"].tolist(),
        y=decdata["total"].tolist(),
        name='Fall in Stock Price',
        marker_color='rgb(237,100,90)'
    ))
    fig.add_trace(go.Bar(
        x=flatdata["Score_Polarity"].tolist(),
        y=flatdata["total"].tolist(),
        name='No Change in Stock Price',
        marker_color='rgb(158,185,243)'
    ))
    
    fig.update_layout(barmode='group',title_text='Statistics of Tweet Sentiment v/s Fluctuations',uniformtext_minsize=12, uniformtext_mode='hide')
    fig.show()
    
def plotstatisticssayear(conn):
    sql_statement='''SELECT strftime('%Y',Tdate) year,score_polarity,stockstatus,count(1) total 
						   FROM (SELECT distinct Tdate,Tweet_Text,Score_Polarity,Adj,stockstatus
								   FROM (SELECT date(t.Creation_dt) TDate,t.Tweet_Text,t1.Score_Polarity,t1.Score,ts.Adj,
								   CASE WHEN (close-open)<0 then 'D'
								   WHEN (close-open)>0 then 'I'
								   ELSE 'F'
								   END as stockstatus 
								   FROM Tesla_Stock ts,Tweet_data t,Tweet_Scores t1 
								   WHERE t.ID=t1.ID and date(t.Creation_dt)=ts.Date)) 
						  GROUP BY year,score_polarity,stockstatus;'''
    df=pd.read_sql_query(sql_statement,conn)
    incdata=df[df["stockstatus"]=="I"]
    decdata=df[df["stockstatus"]=="D"]
    flatdata=df[df["stockstatus"]=="F"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=incdata["year"].tolist(),
					y=incdata["total"].tolist(),
					name='Rise in Stock Price',
					marker_color='rgb(139,224,164)'
					))
    
    fig.add_trace(go.Bar(x=decdata["year"].tolist(),
					y=decdata["total"].tolist(),
					name='Fall in Stock Price',
					marker_color='rgb(237,100,90)'
					))
    
    fig.add_trace(go.Bar(x=flatdata["year"].tolist(),
					y=flatdata["total"].tolist(),
					name='No change in Stock Price',
					marker_color='rgb(158,185,243)'
					))
    
    fig.update_layout(
		title='Statistics of Stock Price Fluctuations by year',
		xaxis_tickfont_size=14,
		yaxis=dict(
			title='Total',
			titlefont_size=16,
			tickfont_size=14,
		),
		legend=dict(
			x=0,
			y=1.0,
			bgcolor='rgba(255, 255, 255, 0)',
			bordercolor='rgba(255, 255, 255, 0)'
		),
		barmode='group',
		bargap=0.15, 
		bargroupgap=0.1 
	)
    
    fig.show()