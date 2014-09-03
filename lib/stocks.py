from postgres_db import MyDB
import pandas as pd

sp_data = pd.read_csv('./data/constituents.csv')
db = MyDB()

for index, row in sp_data.iterrows():
	db.query("INSERT INTO stocks (ticker, name, sector) VALUES (%s, %s, %s)",
	(row['Ticker'], row['Name'], row['Sector']))

db.commit()
