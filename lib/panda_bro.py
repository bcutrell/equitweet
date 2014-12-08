# %run '/Users/bcutrell/python/equitweet/lib/panda_bro.py'

import code # code.interact(local=locals())
from postgres_db import MyDB

import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime
import json

class PandaBro(object):
  def __init__(self):
    with open('./database.json', 'r') as f:
      db_config = json.load(f)

    self.db = MyDB(**db_config)
    self.conn = self.db._db_connection
    self.tweets_summary = self.get_summary_table()
    self.weighted_polarity = self.get_weighted_polarity()

  def setup_summary_table(self):
    # "select ticker, sum (polarity) from tweets group by ticker;"
    self.db.execute(''' 
      create temp table tweets_summary as select * from tweets;

      alter table tweets_summary add weighted_followers double precision;
      update tweets_summary set weighted_followers = 
        (select sum(followers_count) from tweets_summary);
      update tweets_summary set weighted_followers = 
      followers_count / weighted_followers;

      alter table tweets_summary add sector varchar(100);
      update tweets_summary set sector =
        (select sector from stocks 
          where ticker = tweets_summary.ticker);
    ''')

  def get_summary_table(self):
    self.setup_summary_table()
    sql = "select * from tweets_summary"
    return pd.io.sql.read_sql(sql, self.conn)

  def get_weighted_polarity(self):
    df = self.tweets_summary.copy()
    df['polarity'] *= df['weighted_followers']
    return df

  def date_range(self):
    date_df = self.tweets_summary['date'].drop_duplicates()
    start = date_df.min()
    end = date_df.max()
    return [start, end]

  def pull_price_data(self, securities):
    start, end = self.date_range()
    series_list = []
    for security in securities:
      s = pd.io.data.get_data_yahoo(security, start=start, end=end)
      s.name = security # Rename series to match security name
      series_list.append(s)
    if len(series_list) == 1:
      return series_list[0]
    else:
      return series_list

  def pct_return_for(self, ticker):
    df = self.pull_price_data([ticker])
    ret_df = pd.DataFrame(df['Adj Close'].pct_change())
    ticker = 'sp500' if ticker == '^GSPC' else ticker
    ret_df.columns = ['ret_' + ticker]
    return ret_df

class PandaBroTicker(PandaBro):
  pass

class PandaBroSector(PandaBro):
  def clean_sector_names(self):
    df = self.weighted_polarity
    df['sector'] = df['sector'].map(lambda x: x.strip())
    return df.replace('Industries', 'Industrials')

  def tweets_by_sector(self):
    old_df = self.clean_sector_names()
    df = pd.DataFrame(old_df.groupby([old_df['date'], old_df['sector']]).polarity.sum())
    return df

class PandaBroMarket(PandaBro):
  def tweets_by_date(self):
    ## "select date, count (date) from tweets group by date order by date;"
    df = pd.DataFrame(self.tweets_summary.groupby(self.tweets_summary['date']).polarity.count(), dtype=float)
    df.columns = ['volume']
    df['Date'] = df.index
    return df

  def polarity_by_date(self):
    df = pd.DataFrame(self.weighted_polarity.groupby(self.weighted_polarity['date']).polarity.sum())
    df.columns = ['mkt_sentiment']
    df['Date'] = df.index
    return df

  def mkt_sentiment(self):
    df = pd.merge(self.tweets_by_date(), self.polarity_by_date())
    df.index = df['Date']
    df = df.drop('Date', 1)
    return df

  def mkt_sentiment_sp500(self):
    df = self.pct_return_for('^GSPC').combine_first(self.mkt_sentiment())
    df['mkt_sentiment_pct_chg'] = df['mkt_sentiment'].pct_change()
    return df

  def add_mavg(self):
    df = self.mkt_sentiment_sp500()
    df['sentiment_mavg'] = pd.rolling_mean(df.mkt_sentiment, 3) #3
    df.sentiment_mavg.shift(1) # still missing some shifts
    return df

  def run_backtest(self):
    df = self.add_mavg()
    df['order'] = 0

    # Determine long/short based on mkt_sentimnet vs mavg
    # going agaisnt the grain
    df['order'][df.mkt_sentiment > df.sentiment_mavg] = -1
    df['order'][df.mkt_sentiment < df.sentiment_mavg] = 1

    df = df.combine_first(self.pct_return_for('IVV')) # add investable S&P500 class
    df['ret_algo'] = df.order * df.ret_IVV
    df['equitweet_value'] = (1 + df.ret_algo).cumprod()
    df['sp500_value'] = (1 + df.ret_IVV).cumprod()
    return df

  def graph_backtest(self):
    df = self.run_backtest()
    plt.figure(); df[['equitweet_value','sp500_value']].ffill().plot()
    plt.show()

pbro_market = PandaBroMarket()

## Graph MVA strategy vs. SP500
pbro_market.graph_backtest()