import unittest
import sqlite3

conn = sqlite3.connect("../pfit.db")
curs = conn.cursor()


class TestDatabase(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()