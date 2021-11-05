from unittest import TestCase
from core import Tpo
from .rates import rates_m30
from util import pickle_load, pickle_dump
from core import Reference
# from site import addsitedir
# addsitedir('..')


class TestReference(TestCase):

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

    def test_calculate_tpo_count(self):
        tpo_path = './tests/test_core/pkl/tpo.pkl'
        tpo_count_path = './tests/test_core/pkl/tpo_count.pkl'
        tpo = pickle_load(tpo_path)
        tpo_count = Reference()._calculate_tpo_count(tpo)
        # tpo_count.to_csv("./data/csv/tpo_count.csv")
        # pickle_dump(tpo_count, tpo_count_path)
        to_compare = pickle_load(tpo_count_path)
        self.assertTrue(tpo_count.equals(to_compare))

