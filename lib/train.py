# %run '/Users/bcutrell/python/equitweet/lib/train.py'

# TODO:
# cross value score alpha comparison
# decesion trees
# ensemble methods

import code # code.interact(local=locals())
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import linear_model
from scipy.sparse import hstack

# validations
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split

from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import make_scorer
from sklearn.cross_validation import KFold

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

def load_clean_data(filepath, get_normalized_followers=False, get_sector_dummies=False):
  df = pd.read_csv(filepath)
  df = df.drop('full_text', 1) # currently do not use text
  df = df.dropna()
  if get_normalized_followers:
    df = normalize_followers(df)
  if get_sector_dummies:
    df = df.join(pd.get_dummies(df['sector']))
  return df

def clean_data(df, get_normalized_followers=False, get_sector_dummies=False):
  df = df.drop('full_text', 1) # currently do not use text
  df = df.dropna()
  if get_normalized_followers:
    df = normalize_followers(df)
  if get_sector_dummies:
    df = df.join(pd.get_dummies(df['sector']))
  return df

def normalize_followers(df):
  max_followers = df['followers_count'].max()
  df['weighted_followers'] = df['followers_count'] / max_followers
  df['weighted_polarity'] = (df['polarity'] * df['weighted_followers'])
  return df

def gen_matrix_for(series):
  return series.as_matrix().reshape(series.shape[0], 1)

def gen_features():
  return np.hstack([df[sector_names].as_matrix(),
    gen_matrix_for(df['weighted_polarity']),
    gen_matrix_for(df['weighted_followers'])
    ])

# group followers by day 0-1000, 1000-10000, 10000-10000, 100000
# gen_matrix_for(df['weighted_followers']),
# gen_matrix_for(df['security_volume']),  
# gen_matrix_for(df['security_adj_close'])
# gen_matrix_for(df['polarity']),
# gen_matrix_for(df['followers_count'])])

def gen_predictions():
  rr = linear_model.Ridge()
  rr.fit(features, sector_prices)
  df['predictions'] = np.exp(rr.predict(features))
  df['predictions'] = df['predictions'].round(2)

def validator():
  rr = linear_model.Ridge()
  scoring = make_scorer(mean_squared_error, greater_is_better=False)
  parameters = {'alpha': [.001, .1, .01]}
  clf = GridSearchCV(rr, parameters, scoring=scoring)

  clf.fit(Xtrain, Ytrain)
  print clf.best_estimator_.score(Xtest, Ytest)

  scoring = make_scorer(mean_squared_error, greater_is_better=False)
  cv = KFold(Xtrain.shape[0], 10)
  model = linear_model.RidgeCV(alphas=[0.5, 1.0, 1.5], cv=cv, scoring=scoring)
  model.fit(Xtrain,Ytrain)
  print model.coef_
  print model.alpha_
  print model.score(Xtest,Ytest)

def eval_sectors(sector):
  for sector in df['sector'].unique():
    print "*" * 10
    print sector
    print "*" * 10
    print ("-" * 3) + 'Predicted' + ("-" * 3)
    print df['predictions'][df[sector] == 1].describe()
    print ("-" * 3) + 'Actual' + ("-" * 3)
    print df['sector_adj_close'][df[sector] == 1].describe()
    df['sector_adj_close'][df[sector] == 1].plot()
    df['polarity'][df[sector] == 1].plot

np.set_printoptions(formatter={'float_kind':'{:25f}'.format})

filepath = '/Users/bcutrell/python/equitweet/data/train200k.csv'
df = load_clean_data(filepath, get_normalized_followers=True, get_sector_dummies=True)
sector_names = df['sector'].unique()

# get features
features = gen_features()
sector_prices = np.log(gen_matrix_for(df['sector_adj_close']))

# validations
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features, sector_prices, test_size=0.33, random_state=42)
validator()

# try with pct change
def run_pct_chg_graph_for(sector):
  df_chg = df[df[sector] == 1]
  df_sac = df_chg.groupby('date').sector_adj_close.mean()
  df_wp = df_chg.groupby('date').weighted_polarity.mean()
  df_chg = pd.concat([df_sac, df_wp],axis=1)
  df_pct_chg = df_chg.pct_change()
  best way to handle these outliers?
  df_pct_chg.loc[df_pct_chg["weighted_polarity"] > 5, 'weighted_polarity'] = 0
  df_pct_chg.plot(subplots=True, figsize=(6, 6));


# gen_predictions()
# eval_sector('Consumer Discretionary', df)
# mean_squared_error(df['sector_adj_close'], df['predictions'])
# df['sector_adj_close'][df[sector] == 1].plot()
# df['polarity'][df[sector] == 1].plot()
# df['sector_adj_close'][df['Industrials'] == 1].hist()
