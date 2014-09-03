import psycopg2

class MyDB(object):

 	_db_connection = None
 	_db_cur = None

	def __init__(self):
		## add dbname and user to config
		self._db_connection = psycopg2.connect("dbname='demodb' user='bcutrell'")
		self._db_cur = self._db_connection.cursor()

	def query(self, query, params):
		return self._db_cur.execute(query, params)

	def commit(self):
		self._db_connection.commit()

	def __del__(self):
  		self._db_connection.close()
  		self._db_cur.close()
