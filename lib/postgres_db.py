import psycopg2, json

class MyDB(object):

    def __init__(self, **kwargs):
        self._db_connection = psycopg2.connect(**kwargs)
        self._db_cur = self._db_connection.cursor()

        if kwargs.get('autocommit'):
            self.autocommit = True

    def query(self, *args):
        return self._db_cur.execute(*args)

    def fetchone(self):
        return self._db_cur.fetchone()

    def fetchall(self):
        return self._db_cur.fetchall()

    def copy_expert(self, *args, **kwargs):
        return self._db_cur.copy_expert(*args, **kwargs)

    def commit(self):
        self._db_connection.commit()

    @property
    def autocommit(self):
        return self._db_connection.autocommit

    @autocommit.setter
    def autocommit(self, value):
        self._db_connection.autocommit = value

    @property
    def tables(self):
        self.query('''
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        ''')
        return [x[0] for x in self.fetchall()]

    def __del__(self):
        self._db_cur.close()
        self._db_connection.close()
