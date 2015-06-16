import code # code.interact(local=locals())
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.feature_extraction.text  import TfidfVectorizer
import nltk
import datetime
import re
from nltk.corpus import stopwords

def clean_string(text):
  text = text.lower()
  text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
  words = re.findall(r'\w+', text,flags = re.UNICODE | re.LOCALE) 
  words = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
  important_words=[]
  for word in words:
    if word not in stopwords.words('english'):
      important_words.append(word)
      important_words = filter(lambda x: x not in stopwords.words('english'), words)
  return ' '.join(important_words)

def prep_tweet_set(df):
  prepped_tweets = []
  for row in df.iterrows():
    try:
      tok_tweet = nltk.word_tokenize(row[1].full_text)
    except:
      code.interact(local=locals())
    sentiment = row[1].price_up
    prepped_tweets.append([tok_tweet, sentiment])
  return prepped_tweets


def gen_price_up_column():
  df['price_up'] = np.nan
  df.index = df['date']
  for date in df['date'].unique():
    for sector in df['sector'].unique():
      try:
        text = df['full_text'][df['Financials'] == 1].ix[date]
        start_price = df['sector_adj_close'][df['Financials'] == 1].ix[date].unique()

        count = 1
        while count < 5:
          d = datetime.datetime.strptime(date, '%Y-%m-%d')
          d1 = d + datetime.timedelta(days=count)
          try:
            end_price = df['sector_adj_close'][df['Financials'] == 1].ix[d1.strftime('%Y-%m-%d')].unique()
            cond = (start_price < end_price)[0]
            if cond == True:
              df.loc[(df["sector"] == sector) & (df["date"] == date), "price_up"] = 1
            else:
              df.loc[(df["sector"] == sector) & (df["date"] == date), "price_up"] = 0

            break
          except:
            count += 1
      except:
        continue

df = pd.read_csv('data/train_text.csv')
df = df[df['price_up'].notnull()]
df = df[df['full_text'].notnull()]



prepped_tweets = prep_tweet_set(df)
all_words = set()
for tweet in prepped_tweets:
    all_words.update(tweet[0])

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
text_clf = Pipeline([ ('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB())])

text_clf = text_clf.fit(df.full_text, df.price_up)

text_clf = text_clf.fit(df.full_text.as_matrix(), df.price_up.as_matrix())
text_clf.predict('buy me please buy buy buy sell ')

predicted = text_clf.predict(df.full_text)
np.mean(predicted == df.price_up)

from sklearn import metrics
print(metrics.classification_report(df.price_up, predicted, target_names=['price_down', 'price_up']))

# What are people saying?
# df['full_text'][df['ticker'] == 'AAPL'].sum()
# with open("Output.txt", "w") as text_file:
#     text_file.write(a)
