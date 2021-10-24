from util import pickle_dump, pickle_load
import unittest
from core import Tpo
from .rates import rates_m30
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
        # rates_path = './tests/test_core/pkl/RATES_EURUSD_M30_20210801_20211010.pkl'
        # tpo_path = './tests/test_core/pkl/tpo_eurusd_tpo.pkl'
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
        path = './tests/test_core/pkl/prepped_rates.pkl'
        prepped_rates = Tpo()._prepare_rates(rates_m30, 5, 5)
        # pickle_dump(prepped_rates, path)
        to_compare = pickle_load(path)
        self.assertTrue(prepped_rates.equals(to_compare))

    def test_from_prepared_rates_to_tpo(self):
        path = './tests/test_core/pkl/tpo.pkl'
        t = Tpo()
        tpo = t._from_prepared_rates_to_tpo(t._prepare_rates(rates_m30, 5, 5), 5)
        # pickle_dump(tpo, path)
        to_compare = pickle_load(path)
        self.assertTrue(tpo.equals(to_compare))
