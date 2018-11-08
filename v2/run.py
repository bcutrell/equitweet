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
    print(results['statuses'])

if __name__ == '__main__':
    search_tweets_for_ticker('A')
