import unittest
import os

import equitweet

class TestEquitweet(unittest.TestCase):

    def setUp(self):
        #  basedir = os.path.abspath(os.path.dirname(__file__))
        # 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
        # db.create_all()
        pass

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        pass

    def test_init_twitter(self):
        client = equitweet.init_twitter('f', 'a', 'k', 'e')
        assert client


    def test_init_db(self):
        db = equitweet.init_db('f', 'a', 'k', 'e')
        assert db

    def write_to_file(self):
        pass


if __name__ == '__main__':
    unittest.main()