import psycopg2, json
# http://initd.org/psycopg/docs/usage.html?highlight=create

class MyDB(object):

    def __init__(self, autocommit=True, **kwargs):
        self._db_connection = psycopg2.connect(**kwargs)
        self._db_cur = self._db_connection.cursor()

        self.autocommit = autocommit

    def execute(self, *args):
        return self._db_cur.execute(*args)

    def mogrify(self, *args):
        return self._db_cur.mogrify(*args)

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
