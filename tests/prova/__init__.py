import unittest


class TestProva(unittest.TestCase):

    def setUp(self):
        print('setup')

    def tearDown(self):
        print('teardown')

    def test_A(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_B(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 6")
