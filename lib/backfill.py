import code # code.interact(local=locals())
import pandas as pd
from twitter import Twitter, OAuth
import json

class SeedText():
    """
    Backfill tweet text
    """

    def cleanup(self):
        partialpath = 'partial_backfill.csv'
        df = pd.read_csv(partialpath, error_bad_lines=False)


    def run(self):
        # filepath = 'data/tweets.csv'
        partialpath = 'partial_backfill.csv'
        df = pd.read_csv(partialpath, error_bad_lines=False)

        # First Time
        # tweet_id_data = df['tweet_id'].dropna().astype(int).tolist()
        # df_no_text = df[df['full_text'].isnull()]
        # tweet_id_data = df_no_text['tweet_id'].dropna().astype(int).tolist()

        df.index = range(0, df.shape[0])
        text_idx = df['full_text'].last_valid_index()
        df_length = df.shape[0]
        df_no_text = df.ix[range(text_idx,df_length-1)]
        tweet_id_data = df_no_text['tweet_id'].dropna().astype(int).tolist()

        groups = [{'ids': tweet_id_data[i:i+100]} for i in xrange(0, len(tweet_id_data), 100)]

        with open('./config.json', 'r') as f:
            config = json.load(f)['config']

        self.twitter_client = Twitter(auth=OAuth(
            config['token'],
            config['token_secret'],
            config['consumer_key'],
            config['consumer_secret']))

        for group in groups:
            # Search will be rate limited at 180 queries 
            # per 15 minute window for the time
            query_string = ','.join(str(g) for g in group['ids'])
            lookup = self.twitter_client.statuses.lookup(_id=query_string, map=True)
            remaining = lookup.rate_limit_remaining

            if remaining > 1:
                for tweet_id in group['ids']:
                    try:
                        full_text = lookup.values()[0][str(tweet_id)]
                        if full_text:
                            full_text = full_text['text'][0:140].encode("ascii", "ignore")
                            print remaining, full_text
                            df.loc[df['tweet_id'] == tweet_id, 'full_text'] = full_text
                        else:
                            continue
                    except:
                        code.interact(local=locals())
                        continue

            else:
                print "Over the limit"
                df.index = range(0, df.shape[0])
                df.to_csv('partial_backfill.csv')
                break

SeedText().cleanup()
