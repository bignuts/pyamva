import unittest
import sys

print(sys.path)


class TestSum(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")
