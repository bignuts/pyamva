import unittest
from databases.tinydb import TinyDatabase


class TestZullo(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')

    def test_ZU(self):
        TinyDatabase()
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_LLO(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")
