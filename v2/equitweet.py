'''
Desired API (not how it works now...)
    How to use:
        >> import equitweet

        >> client = equitweet.init_twitter(twitter_config)

        >> tweets = client.search_tweets_for_ticker('A')
        >> tweets.write_to_file('a_tweets.csv')

        >> tweets = client.batch_search_tweets_for_tickers(['A', 'B'], filename='ab_tweets.csv')
        >> tweets.write_to_file('a_b_tweets.csv')

        >> db = equitweet.init_db(db_config)
        >> db.seed_tickers(tickers)
        >> db.seed_tweets()
        >> db.seed_prices()

    Future TODOs:
        >> Exploratory Data Analysis example
        >> Backtesting example
        >> Postgres example
        >> Luigi support
        >> Interactive Dashboard with Plotly.js Dash framework
        >> Pandas support

    Why use this?
        A fun and simple way to do some social media sentiment analysis on the fly or collect data over time
'''

from twitter import Twitter, OAuth
import config
import csv
import code # code.interact(local=locals())
import re

def insert_sql_for_tweets(tweets):
    pass

def get_twitter_rates():
    rate_limits = twitter_client.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
    return rate_limits['reset'], rate_limits['limit'], rate_limits['remaining']

def write_tweets_to_file(tweets, filename='tweets.csv'):
    keys = tweets[0].keys()

    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tweets)

def format_tweets(tweets, ticker):
    return [ format_tweet(tweet, ticker) for tweet in tweets ]

def format_tweet(tweet, ticker):
    return {
        'ticker': ticker,
        'text': tweet['text'].encode(),
        'tweet_id': tweet['id'],
        'username': tweet['user']['name'],
        'followers': tweet['user']['followers_count'],
        'created_date': tweet['created_at'],
        'retweet_count': tweet['retweet_count'],
        'favorite_count': tweet['favorite_count']
    }

def format_batch_tweets(tweets, tickers):
    # Because we are using an OR query
    # create entries based on the tickers
    # that appear in each tweet

    return [
        format_tweet(tweet, ticker)
        for ticker in tickers
        for tweet in tweets
        if re.search(r'\${0}[^A-Z]'.format(ticker), tweet['text'])
    ]

def search_tweets(query_string, max_id=None, since_id=None):
    query_args = {
        'q': query_string,
        'include_entities': False,
        'count': 100,
        'lang': 'en'
    }

    if max_id:
        query_args['max_id'] = max_id
    if since_id:
        query_args['since_id'] = since_id

    return twitter_client.search.tweets(**query_args)

def search_tweets_for_ticker(ticker):
    raw_data = search_tweets('$' + ticker)
    return format_tweets(raw_data['statuses'], ticker)

def batch_search_tweets_for_tickers(tickers, remaining=180):
    # Break into groups of 30 to keep query string below 500 chars
    grouped_tickers = [tickers[i:i+30] for i in range(0, len(tickers), 30)]

    results = []
    for ticker_group in grouped_tickers:
        query_string = ' OR '.join('$' + ticker for ticker in ticker_group)
        max_id = None
        since_id = None # used if db

        while remaining > 0:
            raw_data = search_tweets(query_string, max_id=max_id, since_id=since_id)
            results.append(format_batch_tweets(raw_data['statuses'], ticker_group))

            print('remaining: {0}'.format(remaining))
            remaining -= 1

            if raw_data['search_metadata'].get('next_results'):
                max_id = raw_data['search_metadata']['next_results'].split('&')[0].lstrip('?max_id=')
            else:
                max_id = raw_data['search_metadata']['max_id']
                break

    return [item for sublist in results for item in sublist] # flatten list

if __name__ == '__main__':
    twitter_client = Twitter(auth=OAuth(**config.TWITTER_CONFIG))
    next_reset, max_per_reset, remaining = get_twitter_rates()
    tweets = search_tweets_for_ticker('A')
    tweets = batch_search_tweets_for_tickers(['A', 'B'])
    write_tweets_to_file(tweets)
