import code # code.interact(local=locals())
import pandas as pd
import pandas.io.data as web
import numpy as np
import json
from twitter import Twitter, OAuth
import datetime

class Cleaner(object):
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, error_bad_lines=False)

class BackFillText(Cleaner):
    def run(self):
        df = self.df
        df_no_text = df[df['full_text'].isnull()]

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
                df.to_csv('data/partial_backfill.csv')
                break

class SetupTrain(Cleaner):
    '''
    Used with backfilled data
    '''

    def sector_security_map(self, sector):
        sector_map = {  'Consumer Discretionary': 'XLY',
                        'Consumer Staples': 'XLP',
                        'Energy': 'XLE',
                        'Financials': 'XLF',
                        'Health Care': 'XLV',
                        'Industrials': 'XLI',
                        'Materials': 'XLB',
                        'Technology': 'XLK',
                        'Information Technology': 'XLK',
                        'Utilities': 'XLU',
                        'Telecommunications Services': 'XTL'}
        return sector_map[sector]

    def setup_train_seed_sectors(self):
        '''
        cleanup backfill data for training set
        '''
        df = self.df
        text_df = df[df['full_text'].notnull()]

        filepath = 'data/constituents.csv'
        stocks_df = pd.read_csv(filepath)
        stocks_df['sector'] = stocks_df['Sector'].map(lambda x: x.strip())
        stocks_df = stocks_df.replace('Industries', 'Industrials')

        text_df['sector'] = np.nan
        for ticker in stocks_df.Ticker.tolist():
            sector = stocks_df.sector[stocks_df.Ticker == ticker].values[0]
            text_df.loc[text_df['ticker'] == ticker, 'sector'] = sector

        text_df = text_df.drop('Unnamed: 0', 1)
        # text_df.to_csv('data/train.csv', index=False)

    def prices_for(self, ticker, start, end):
        try:
            prices = web.DataReader(ticker, 'yahoo', start, end)
        except IOError:
            print 'missing ' + ticker
            print IOError
            prices = False
        return prices

    def get_price_history_for(self, tickers, start, end, sector=False):
        price_history = {}
        for ticker in tickers:
            if sector:
                sector_etf = self.sector_security_map(ticker)
                prices = self.prices_for(sector_etf, start, end)
            else:
                prices = self.prices_for(ticker, start, end)

            price_history[ticker] = prices
        return price_history

    def date_range(self, df):
        date_df = df['date'].drop_duplicates().dropna()
        start = datetime.datetime.strptime(date_df.min(), '%Y-%m-%d')
        end = datetime.datetime.strptime(date_df.max(), '%Y-%m-%d')
        return start, end

    def get_unique_list_for(self, column, df):
        return df[column].drop_duplicates().dropna().tolist()

    def setup_train_seed_prices(self):
        '''
        Add prices
        '''
        tweets_df = self.df
        start, end = self.date_range(tweets_df) # get dates

        # sector_list = self.get_unique_list_for('sector', tweets_df)
        # sector_price_history = self.get_price_history_for(sector_list, start, end, True)
        
        securities_list = self.get_unique_list_for('ticker', tweets_df)
        security_price_history = self.get_price_history_for(securities_list, start, end)
        
        tweets_df['sector_adj_close'] = tweets_df['security_adj_close'] = \
        tweets_df['security_volume'] = np.nan

        tweets_df = tweets_df[tweets_df.sector.notnull()]
        for index, row in tweets_df.iterrows(): # horrible... but easy to read
            # price_df = sector_price_history[self.sector_security_map(row['sector'])]
            price_df = security_price_history[row['ticker']]

            try:
                price_df_t1 = price_df.shift(-1)
            except:
                continue

            count = 0
            date = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            while count < 5:
                try:
                    d = date + datetime.timedelta(days=count)
                    # sector_price = price_df_t1.ix[d]['Adj Close']
                    # sector_price = price_df_t1.ix[row['date']]['Adj Close']
                    # tweets_df.loc[row.name, 'sector_adj_close'] = sector_price

                    security_price = price_df_t1.ix[d]['Adj Close']
                    security_volume = price_df_t1.ix[d]['Volume']

                    tweets_df.loc[row.name, 'security_adj_close'] = security_price
                    tweets_df.loc[row.name, 'security_volume'] = security_volume
                    break
                except:
                    count += 1

        # tweets_df.to_csv('data/train_new.csv', index=False)

    def setup_train_seed_security_prices(self):
        pass


# filepath = 'data/train.csv'
# SetupTrain(filepath).setup_train_seed_prices()
