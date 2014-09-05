import code #code.interact(local=locals())
from lib.twitter_man import tman
from lib.postgres_db import MyDB
import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib as mpl 
import datetime

### query examples ###
# sql = "select * from medicine_journal where medication = '%(medicine)s'"
# pd.io.sql.read_frame(sql % {'medicine':'flonase'}, conn)

my_db = MyDB()
conn = my_db._db_connection

sql = "select * from tweets"
# Create a dataframe that consists of the data defined by our SQL
df = pd.io.sql.read_frame(sql, conn) # change to read sql
conn.close() # close after we create dataframe
code.interact(local=locals())
df[df['polarity'] > 0.5] # all polarity > 0.5
np.mean(df['polarity'].values) # avg of all polarity

### pandas stock data example ###
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2013, 1, 27)

f = web.DataReader("F", 'yahoo', start, end)
