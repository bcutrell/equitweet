import pandas.io.data as web
import datetime

filepath = 'data/constituents.csv'
stocks_df = pd.read_csv(filepath)

stocks_df['sector'] = stocks_df['sector'].map(lambda x: x.strip())
stocks_df.replace('Industries', 'Industrials')

filepath = 'data/train.csv'
tweets_df = pd.read_csv(filepath)

start = datetime.datetime(2014, 8, 1)
end = datetime.datetime(2014, 8, 27)

df.min
df.max

f=web.DataReader('XLY', 'yahoo', start, end)

f.ix['2010-01-04']

'''
Consumer Discretionary (XLY)
Consumer Staples (XLP)
Energy (XLE)
Financials (XLF)
Health Care (XLV)
Industrials (XLI)
Materials (XLB)
Technology (XLK)
Utilities (XLU)
'''
pprint(ystockquote.get_all('XLU'))

def date_range(self):
  date_df = self.tweets_summary['date'].drop_duplicates()
  start = date_df.min()
  end = date_df.max()
  return [start, end]

# technial indicators
# https://github.com/mrjbq7/ta-lib

# import ystockquote
#	from pprint import pprint
# pprint(ystockquote.get_all('GOOG'))
# {'avg_daily_volume': '2178170',

# pprint(ystockquote.get_historical_prices('GOOG', '2013-01-03', '2013-01-08'))

# sector price t+1
# tech feature
# fund feature

# pprint(ystockquote.get_all('XLU'))
# {'avg_daily_volume': '12103100',
#  'book_value': '0.00',
#  'change': '-0.17',
#  'dividend_per_share': '1.49',
#  'dividend_yield': '3.21',
#  'earnings_per_share': '0.00',
#  'ebitda': '0',
#  'fifty_day_moving_avg': '43.63',
#  'fifty_two_week_high': '46.61',
#  'fifty_two_week_low': '37.11',
#  'market_cap': 'N/A',
#  'price': '46.31',
#  'price_book_ratio': 'N/A',
#  'price_earnings_growth_ratio': 'N/A',
#  'price_earnings_ratio': 'N/A',
#  'price_sales_ratio': 'N/A',
#  'short_ratio': 'N/A',
#  'stock_exchange': '"PCX"',
#  'two_hundred_day_moving_avg': '42.845',
#  'volume': '5562956'}