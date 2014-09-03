# import code code.interact(local=locals())

import os.path, sys
### grab path for db file ###
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('postgres_db.py'))))

from postgres_db import MyDB
import pandas as pd

sp_data = pd.read_csv('../data/constituents.csv')
db = MyDB()

for index, row in sp_data.iterrows():
	db.query("INSERT INTO stocks (stock, symbol, name, sector) VALUES (%s, %s, %s, %s)",
	('$' + row['Symbol'], row['Symbol'], row['Name'], row['Sector']))

db.commit()
