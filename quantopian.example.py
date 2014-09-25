'''
Quantopian Gamplan:
	Use the trading algo simulator here: https://www.quantopian.com/
	This website lets you upload custom csv data via fetch_csv()

	The simulator can also be run on the CL using zipline but this involves
	more specifications. I have also been unable to even find the fetch_csv() method
	in the repo: https://github.com/quantopian/zipline

	PandaBro can be used to generate 3 csvs, Market, Sector, and Ticker.
	These can be stored as temporary gists and pulled in the quantopian
	backtesting app. This will give us more accurate backtests and allow for
	potential live trading platforms (I believe thats still a work in progress
	on their end)

	Below is an example from one of the quantopian founders -- it trades based
	off of the google search term 'debt', it is a similar example that can help
	get the wheels in motion
'''

import code # code.interact(local=locals())
import zipline as zp
from lib.panda_bro import PandaBroMarket, PandaBroSector, PandaBroTicker

pbro_market = PandaBroMarket()
pbro_sector = PandaBroSector()
pbro_ticker = PandaBroTicker()

## Graph MVA strategy vs. SP500
# pbro_market.graph_backtest()

import numpy as np
import datetime
# Average over X weeks
delta_t = 'X'

def initialize(context):
    # This is the search query we are using, this is tied to the csv file.
    context.query = 'sentiment'
    # User fetcher to get data. I uploaded this csv file manually, feel free to use.
    # Note that this data is already weekly averages.
    fetch_csv('insert_sentiment_csv_here',
              date_format='%Y-%m-%d',
              symbol='sentiment',
    )
    context.order_size = 'order_size'
    context.sec_id = 8554 # security ids
    context.security = sid(8554) # S&P5000

def handle_data(context, data):
    c = context
  
    if c.query not in data[c.query]:
    	return
   
    # Extract weekly average of search query.
    indicator = data[c.query][c.query]
    
    # Buy and hold strategy that enters on the first day of the week
    # and exits after one week.
    if data[c.security].dt.weekday() == 0: # Monday
        # Compute average over weeks in range [t-delta_t-1, t[
        mean_indicator = mean_past_queries(data, c.query)
        if mean_indicator is None:
            return

        # Exit positions
        amount = c.portfolio['positions'][c.sec_id].amount
        order(c.security, -amount)

        # Long or short depending on whether debt search frequency
        # went down or up, respectively.
        if indicator > mean_indicator:
            order(c.security, -c.order_size)
        else:
            order(c.security, c.order_size)
        
# If we want the average over 5 weeks, we'll have to use a 6
# week window as the newest element will be the current event.
@batch_transform(window_length=delta_t+1, refresh_period=0)
def mean_past_queries(data, query):
    # Compute mean over all events except most current one.
    return data[query][query][:-1].mean()

