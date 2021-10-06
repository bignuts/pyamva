import unittest
from connectors.metatrader import MetaTrader
from MetaTrader5 import TIMEFRAME_D1, TIMEFRAME_M30
from datetime import datetime, timezone, timedelta
from util import pickle_dump, pickle_load
# from site import addsitedir
# addsitedir('..')


class TestMetaTrader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mt = MetaTrader()

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
        rates1 = self.mt.get_rates("EURUSD", TIMEFRAME_D1, dt, 10)
        # pickle_dump(rates1, path)
        rates2 = pickle_load(path)
        self.assertListEqual(rates1, rates2)

    def test_get_rates_copy_rates_from_pos(self):
        rates_df = self.mt.get_rates("EURUSD", TIMEFRAME_D1, 0, 13)
        self.assertEqual(len(rates_df), 13)

    def test_get_rates_copy_rates_range(self):
        path = './tests/test_connectors/copy_rates_range.pkl'
        to = datetime(2021, 7, 20, 15, 25, 36, tzinfo=timezone.utc)
        frm = to - timedelta(days=15)
        rates1 = self.mt.get_rates("EURUSD", TIMEFRAME_M30, frm, to)
        # pickle_dump(rates1, path)
        rates2 = pickle_load(path)
        self.assertListEqual(rates1, rates2)
