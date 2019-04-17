from twitter import Twitter, OAuth

import csv
import re

class Client():

    NO_TWEETS_MSG = 'There are no tweets'

    def __init__(self, config):
        self.t = Twitter(auth=OAuth(**config))
        self.tweets = []
        self.next_reset, self.max_per_reset, self.remaining = [None]*3

    def search_tweets(self, ticker):
        raw_data = self.__search_tweets('$' + ticker)
        self.__format_tweets(raw_data['statuses'], ticker)

    def batch_search_tweets(self, tickers):
        self.__get_twitter_rates()
        remaining = self.remaining

        # Break into groups of 30 to keep query string below 500 chars
        grouped_tickers = [tickers[i:i+30] for i in range(0, len(tickers), 30)]

        for ticker_group in grouped_tickers:
            query_string = ' OR '.join('$' + ticker for ticker in ticker_group)
            max_id = None
            since_id = None # used if db

            while remaining > 0:
                raw_data = self.__search_tweets(query_string, max_id=max_id, since_id=since_id)
                self.__format_batch_tweets(raw_data['statuses'], ticker_group)

                print('remaining: {0}'.format(remaining))
                remaining -= 1

                if raw_data['search_metadata'].get('next_results'):
                    max_id = raw_data['search_metadata']['next_results'].split('&')[0].lstrip('?max_id=')
                else:
                    max_id = raw_data['search_metadata']['max_id']
                    break
        print("Tweets Stored: {0}".format(len(self.tweets)))

    def __format_tweets(self, tweets, ticker):
        return [ self.__format_tweet(tweet, ticker) for tweet in tweets ]

    def __format_tweet(self, tweet, ticker):
        self.tweets.append({
            'ticker': ticker,
            'text': tweet['text'].encode(),
            'tweet_id': tweet['id'],
            'username': tweet['user']['name'],
            'followers': tweet['user']['followers_count'],
            'created_date': tweet['created_at'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count']
        })

    def write_tweets_to_file(self, filename='tweets.csv'):
        if len(self.tweets) == 0:
            return self.NO_TWEETS_MSG

        keys = self.tweets[0].keys()
        with open(filename, 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.tweets)

    def __format_batch_tweets(self, tweets, tickers):
        # Because we are using an OR query
        # create entries based on the tickers
        # that appear in each tweet

        return [
            self.__format_tweet(tweet, ticker)
            for ticker in tickers
            for tweet in tweets
            if re.search(r'\${0}[^A-Z]'.format(ticker), tweet['text'])
        ]


    def __get_twitter_rates(self):
        if self.next_reset and self.max_per_reset and self.remaining:
            return
        else:
            rate_limits = self.t.application.rate_limit_status(resources="search")['resources']['search']['/search/tweets']
            self.next_reset, self.max_per_reset, self.remaining = \
                rate_limits['reset'], rate_limits['limit'], rate_limits['remaining']

    def __search_tweets(self, query_string, max_id=None, since_id=None):
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

        return self.t.search.tweets(**query_args)

