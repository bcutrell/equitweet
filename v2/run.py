from twitter import Twitter, OAuth
import config

twitter_client = Twitter(auth=OAuth(**config.TWITTER_CONFIG))

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
    print(results['statuses'][0])

def batch_search_tweets_for_tickers(tickers):
    # Break into groups of 30 to keep query string below 500 chars
    grouped_tickers = [tickers[i:i+30] for i in range(0, len(tickers), 30)]
    for ticker_group in grouped_tickers:
        query_string = ' OR '.join('$' + ticker for ticker in ticker_group)
        results = search_tweets(query_string)
        print(results['statuses'][0])

if __name__ == '__main__':
    # search_tweets_for_ticker('A')
    batch_search_tweets_for_tickers(['A', 'B'])
