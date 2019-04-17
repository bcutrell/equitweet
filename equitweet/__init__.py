from .client import Client
import os

exists = os.path.isfile('config.py')
if not exists:
    print("There must be a config.py file in the working directory, see config.py.template for an example.")
    exit()

import config
client = Client(config.TWITTER_CONFIG)

def search(ticker):
    client.search_tweets('$' + ticker)
    return client.tweets

def batch_search(ticker):
    client.batch_search_tweets(tickers)
    return client.tweets

def store(ticker):
    pass

def batch_store(ticker):
    pass

