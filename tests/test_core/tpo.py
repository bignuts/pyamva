from datetime import datetime
from connectors import MetaTrader
from util import pickle_dump, pickle_load
import unittest
from MetaTrader5 import TIMEFRAME_M30
from core import Tpo
# from site import addsitedir
# addsitedir('..')


class TestTpo(unittest.TestCase):

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

    def test_Tpo(self):
        # rates_path = './tests/test_core/tpo_eurusd_rates.pkl'
        tpo_path = './tests/test_core/tpo_eurusd_tpo.pkl'
        mt = MetaTrader()
        rates = mt.get_rates(
            'EURUSD', TIMEFRAME_M30, datetime(
                2021, 10, 1), datetime(
                2021, 10, 5))
        # pickle_dump(rates, path)
        # rates = pickle_load(rates_path)
        tpo = Tpo().from_rates(rates, 5, 5)
        pickle_dump(tpo, tpo_path)
        tpo_to_compare = pickle_load(tpo_path)
        self.assertTrue(tpo.equals(tpo_to_compare))
