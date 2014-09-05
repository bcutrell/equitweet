# Populates DB with values from data/constituents.csv
from lib.seeder import SeedStocks

seed_stocks = SeedStocks().run()
