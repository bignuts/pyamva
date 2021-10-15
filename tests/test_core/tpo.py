from datetime import datetime
from typing import List
from connectors import MetaTrader, Rates
from util import pickle_dump, pickle_load
import unittest
from MetaTrader5 import TIMEFRAME_M30, TIMEFRAME_D1, TIMEFRAME_H1
from core import Tpo
from .rates import rates
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
        # rates_path = './tests/test_core/RATES_EURUSD_M30_20210801_20211010.pkl'
        # tpo_path = './tests/test_core/tpo_eurusd_tpo.pkl'
        # mt = MetaTrader()
        # rates = mt.get_rates(
        #     'EURUSD', TIMEFRAME_M30, datetime(
        #         2021, 8, 1), datetime(
        #         2021, 10, 10))
        # pickle_dump(rates, rates_path)
        # rates = pickle_load(rates_path)
        # tpo = Tpo().from_rates(rates, 5, 5)
        # pickle_dump(tpo, tpo_path)
        # tpo_to_compare = pickle_load(tpo_path)
        # self.assertTrue(tpo.equals(tpo_to_compare))
        pass

    def test_prepare_rates(self):
        mt = MetaTrader()
        rates = mt.get_rates(
            'EURUSD', TIMEFRAME_D1, datetime(
                2021, 9, 1), datetime(
                2021, 9, 30))
        prepped_rates = Tpo()._prepare_rates(rates, 5, 5)
        prepped_rates.to_excel('./xlsx/test_prep_rates.xlsx')
        pass

    def test_from_prepared_rates_to_tpo(self):
        pass
