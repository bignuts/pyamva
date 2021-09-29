from site import addsitedir
addsitedir('..')
import unittest
from connectors.metatrader import MetaTrader
from MetaTrader5 import TIMEFRAME_D1, TIMEFRAME_M30
from datetime import datetime, timezone, timedelta
from pandas import DataFrame, read_pickle
import os


class TestMetaTrader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mt = MetaTrader()
        print(os.getcwd())

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_rates_copy_rates_from(self):
        path = './tests/test_connectors/copy_rates_from.pkl'
        dt = datetime(2021, 9, 20, 15, 25, 36, tzinfo=timezone.utc)
        rates_df1 = self.mt.get_rates("EURUSD", TIMEFRAME_D1, dt, 10)
        # rates_df1.to_pickle(path)
        rates_df2 = read_pickle(path)
        self.assertTrue(rates_df1.equals(rates_df2))
    
    def test_get_rates_copy_rates_range(self):
        path = './tests/test_connectors/copy_rates_range.pkl'
        to = datetime(2021, 7, 20, 15, 25, 36, tzinfo=timezone.utc)
        frm = to - timedelta(days=15)
        rates_df1 = self.mt.get_rates("EURUSD", TIMEFRAME_M30, frm, to)
        # rates_df1.to_pickle(path)
        rates_df2 = read_pickle(path)
        self.assertTrue(rates_df1.equals(rates_df2))
