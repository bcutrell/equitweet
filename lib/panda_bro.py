import code # code.interact(local=locals())
from postgres_db import MyDB
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime
import json

# As the data grows... 
# A lot of these pandas data manipulations should
# be replaced by sql queries 

class PandaBro(object):
  def __init__(self):
    with open('./aws_database.json', 'r') as f:
      db_config = json.load(f)

    my_db = MyDB(**db_config)
    conn = my_db._db_connection
    sql = "select * from tweets"

    self.tweets_df = pd.io.sql.read_sql(sql, conn)

    conn.close()

  def date_range(self):
    date_df = self.tweets_df['date'].drop_duplicates()
    start = date_df.min()
    end = date_df.max()
    return [start, end]

##########################
# TICKER LEVEL
##########################

  def get_mean_polarity(self):
    """
    get the mean polarity for each ticker
    """
    return self.tweets_df.groupby(self.tweets_df['ticker'])['polarity'].mean()
    # df.argmax() get ticker

  def generate_prices(self, ticker, start, end):
    df = web.DataReader(ticker, 'yahoo', start, end)
    df['ticker'] = ticker
    return df

  def normalize_polarity(self):
    """
    normalize polarity by the number of followers and
    level of subjectivity
    """
    df = self.tweets_df.copy()
    max_followers = df['followers_count'].max()
    df['weighted_followers'] = df['followers_count'] / max_followers
    
    df['polarity'] *= df['weighted_followers']

    # subjectivity (facts vs. opinions) => 
    # 0.0 is very objective(good) : 1.0 is very subjective(bad)
    # not really sure about the best way to incorporate this
    # need to do some debugging on this one, do we even care?
    # df['polarity'] *= abs(df['subjectivity'] - 1) # prefer objective
    # df['polarity'] *= df['subjectivity'] # prefer subjective
    return df

##########################
# SECTOR LEVEL
##########################

##########################
# MARKET LEVEL
##########################

  def overall_sentiment(self):
    """
    overall s&p 500 sentiment -- weighted by volume
    TODO: include market volume
    """
    volume_by_date = pd.DataFrame(self.tweets_df.groupby(self.tweets_df['date'])['polarity'].count(), dtype=float)
    volume_by_date.columns = ['volume']
    volume_by_date['date'] = volume_by_date.index

    ## use normalized polarity
    mean_by_date = pd.DataFrame(self.normalize_polarity().groupby(self.tweets_df['date'])['polarity'].mean())
    mean_by_date.columns = ['daily_sentiment']
    mean_by_date['date'] = mean_by_date.index

    date_volume_mean = pd.merge(volume_by_date, mean_by_date)

    max_volume = volume_by_date['volume'].max(numeric_only=True)
    date_volume_mean['weighted_volume'] = date_volume_mean['volume'] / max_volume
    date_volume_mean['daily_sentiment'] *= date_volume_mean['weighted_volume']
    return date_volume_mean.drop(['weighted_volume', 'volume'], 1)

  def overall_sentiment_vs_sp500(self):
    start, end = self.date_range()
    sp500_df = self.generate_prices('^GSPC', start, end)

    df = self.overall_sentiment()
    df_pct_change = pd.DataFrame(sp500_df['Adj Close'].pct_change())
    df_pct_change.columns = ['sp500_pct_change']
    df_pct_change['daily_sentiment'] = df.set_index(['date'])['daily_sentiment'].pct_change()    
    # Find a way to incorporate weekends/holidays
    return df_pct_change
