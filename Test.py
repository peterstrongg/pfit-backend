import unittest
from Database import Database

db = Database("pfit.db")

class TestDatabase(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()