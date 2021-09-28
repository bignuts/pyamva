from site import addsitedir
addsitedir('..')
import unittest
from connectors.metatrader import MetaTrader


class TestMetaTrader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_connect(self):
        MetaTrader()
        pass
