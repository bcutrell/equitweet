import code # code.interact(local=locals())
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import linear_model
from scipy.sparse import hstack

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

def load_data(filepath):
	return pd.read_csv(filepath)

filepath = '/Users/bcutrell/python/equitweet/data/full_train.csv'
df = load_data(filepath) # need historical prices
df = df.dropna()

# get dummy variables for each sector
sector_names = df['sector'].unique()
df = df.join(pd.get_dummies(df['sector'])) # df = df.drop('sector', 1)

code.interact(local=locals())

# merge all the text for each sector?
vect_two = vect_one =
	TfidfVectorizer(min_df=1,ngram_range=(1,3),max_features=200) # 24000000

tweets = df['full_text']
sectors = df['sector']

# features add sector name to each tweet?
tweets_vect = vect_one.fit_transform(tweets)
sectors_vect = vect_two.fit_transform(sectors) # add as binary 

# b.reshape(5, 1)
# merge and add to regression
merged = hstack((tweets_vect,sectors_vect))
rr = linear_model.Ridge(alpha=0.035)

sector_prices = df['sector_adj_close']
sector_prices = sector_prices.reshape(sector_prices.shape[0], 1)

# rr.fit(merged,sector_prices)
# rr.fit(tweets_vect.toarray(),sector_prices)
