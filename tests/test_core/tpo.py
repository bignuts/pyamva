from util import pickle_dump, pickle_load
from unittest import TestCase
from core import Tpo
from core.tpo import _days_in_df
from .rates import rates_m30
# from site import addsitedir
# addsitedir('..')


class TestTpo(TestCase):

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

    def test_prepare_rates(self):
        path = './tests/test_core/pkl/prepped_rates.pkl'
        prepped_rates = Tpo()._prepare_rates(rates_m30, 5, 5)
        # pickle_dump(prepped_rates, path)
        to_compare = pickle_load(path)
        self.assertTrue(prepped_rates.equals(to_compare))

    def test_from_prepared_rates_to_tpo(self):
        prep_path = './tests/test_core/pkl/prepped_rates.pkl'
        tpo_path = './tests/test_core/pkl/tpo.pkl'
        tpo = Tpo()._from_prepared_rates_to_tpo(pickle_load(prep_path), 5)
        # pickle_dump(tpo, tpo_path)
        to_compare = pickle_load(tpo_path)
        self.assertTrue(tpo.equals(to_compare))

    def test_find_date(self):
        path = './tests/test_core/pkl/prepped_rates.pkl'
        rates_df = pickle_load(path)
        days = _days_in_df(rates_df)
        # days.to_csv('./data/csv/days.csv')
        pass
