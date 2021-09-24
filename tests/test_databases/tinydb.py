from site import addsitedir
addsitedir('..')
from functools import wraps
from os import remove
from databases import TinyDatabase, Param
import unittest


# TODO fai funzionare sta merda
# class SetUpDatabase:

#     def __init__(self, db_name: str):
#         self._db_path = f'./tests/test_databases/{db_name}.json'
#         self._db = TinyDatabase(self._db_path)

#     def __enter__(self):
#         return self._db

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         pass

#     def __del__(self):
#         self._db = None
#         del self._db
#         remove(self._db_path)


def setup_database(func):
    '''Setup e pulizia del database per eseguire i vari test'''
    @wraps(func)
    def func_wrapper(self, **kwargs):
        total_run = 0
        db_name = f'{func.__name__}.json'
        db = TinyDatabase(db_name)
        func(self, db=db)
        # chiudi connessione
        del db
        # rimuovi database
        remove(db_name)
        total_run += 1
        print(f'\nRunned total times => {total_run}')
    return func_wrapper


class TestTinyDatabase(unittest.TestCase):

    @setup_database
    def test_add(self, **kwargs):
        db = kwargs['db']
        record = Param(symbol='TEST', timeframe=30, days=20, decimal=5,
                       offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
        id = db.add(record)
        self.assertEqual(
            id, 1, 'Il valore dovrebbe essere ugale a 1 perchè si è inserito un solo record')

    @setup_database
    def test_get_all(self, **kwargs):
        db = kwargs['db']
        for i in range(10):
            record = Param(symbol=f'TEST{i}', timeframe=30, days=20, decimal=5,
                           offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
            db.add(record)
        db_len = len(db)
        self.assertEqual(
            db_len, 10, 'Il valore dovrebbe essere ugale a 10 perchè sono stati inseriti 10 records')

    @setup_database
    def test_get_with_int(self, **kwargs):
        db = kwargs['db']
        for i in range(10):
            record = Param(symbol=f'TEST{i}', timeframe=30, days=20, decimal=5,
                           offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
            db.add(record)
        res = db.get(5)
        self.assertDictEqual(
            res, Param(symbol=f'TEST4', timeframe=30, days=20, decimal=5,
                       offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True), 'Il valore dovrebbe essere ugale a 10 perchè sono stati inseriti 10 records')
    
    @setup_database
    def test_get_with_str(self, **kwargs):
        db = kwargs['db']
        for i in range(10):
            record = Param(symbol=f'TEST{i}', timeframe=30, days=20, decimal=5,
                           offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
            db.add(record)
        res = db.get('TEST4')
        self.assertDictEqual(
            res, Param(symbol=f'TEST4', timeframe=30, days=20, decimal=5,
                       offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True), 'Il valore dovrebbe essere ugale a 10 perchè sono stati inseriti 10 records')

    # def setUp(self):
    #     self.db = TinyDatabase(dbname)

    # def tearDown(self):
    #     del self.db
    #     remove(dbname)

    # def test_add_get_remove(self):
    #     param = Param(symbol='TEST', timeframe=30, days=20, decimal=5,
    #                   offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
    #     record_id = self.db.add(param)
    #     ret_param = self.db.get('TEST')
    #     self.assertDictEqual(ret_param, param,
    #                          f'La riga aggiunta dovrebbe essere {param}')
    #     rem_param = self.db.remove('TEST')
    #     self.assertEqual(rem_param, record_id,
    #                      f'Il valore di remove dovrebbe essere {record_id}')

    # def test_exist_getall(self):
    #     param = Param(symbol='TEST', timeframe=30, days=20, decimal=5,
    #                   offset=2, tpo_size=10, profiles=[1, 2, 3, 4], active=True)
    #     self.db.add(param)
    #     self.db.add(param)
    #     all_param = self.db.get_all()
    #     self.assertEqual(len(all_param), 1,
    #                      f'Dovrebbe esserci solo 1 riga nel database')
    #     self.db.remove('TEST')

    # def test_get_non_existing(self):
    #     ret_param = self.db.get('NONEXISTING')
    #     self.assertEqual(ret_param['symbol'], 'NONEXISTING')

    # def test_remove_non_existing(self):
    #     rem_param = self.db.remove('NONEXISTING')
    #     self.assertEqual(rem_param, 0)
