import psycopg2, json

class MyDB(object):

 	_db_connection = None
 	_db_cur = None

	def __init__(self):
		json_data=open('./config.json')
		config = json.load(json_data)['config']
		json_data.close()

		self._db_connection = psycopg2.connect(
			# host=config["db"]["aws"]["host"],
			# password=config["db"]["aws"]["password"],
			database=config["db"]["local"]["database"],
			user=config["db"]["local"]["user"])
		self._db_cur = self._db_connection.cursor()

	def query(self, query, params):
		return self._db_cur.execute(query, params)

	def fetchone(self):
		return self._db_cur.fetchone()

	def commit(self):
		self._db_connection.commit()

	def __del__(self):
		self._db_cur.close()
		self._db_connection.close()
  		