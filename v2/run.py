from twitter import Twitter, OAuth
import config
import code # code.interact(local=locals())

twitter_client = Twitter(auth=OAuth(**config.TWITTER_CONFIG))

def insert_sql_for_tweets(tweets):
    pass

def format_tweets(tweets):
    return [ format_tweet(tweet) for tweet in tweets ]

def format_tweet(tweet):
    return {
        'text': tweet['text'],
        'tweet_id': tweet['id'],
        'username': tweet['user']['name'],
        'followers': tweet['user']['followers_count'],
        'created_date': tweet['created_at'],
        'retweet_count': tweet['retweet_count'],
        'favorite_count': tweet['favorite_count']
    }

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
    results = search_tweets('$' + ticker)
    return format_tweets(results['statuses'])

def batch_search_tweets_for_tickers(tickers):
    # Break into groups of 30 to keep query string below 500 chars
    grouped_tickers = [tickers[i:i+30] for i in range(0, len(tickers), 30)]
    for ticker_group in grouped_tickers:
        query_string = ' OR '.join('$' + ticker for ticker in ticker_group)
        results = search_tweets(query_string)
        print(results['statuses'][0])

if __name__ == '__main__':
    tweets = search_tweets_for_ticker('A')
    print(tweets[0])
    # batch_search_tweets_for_tickers(['A', 'B'])
