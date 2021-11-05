from unittest import TestCase
from typing import Dict
from functools import wraps
from os import remove
from databases import TinyDatabase
# from site import addsitedir
# addsitedir('..')


# TODO fai funzionare sta merda
# class SetUpDatabase:

#     def __init__(self, db_name: str):
#         self._db_path = f'./tests/test_databases/{db_name}.json'
#         self._db = TinyDatabase(self._db_path)
#         self._total_run = 0

#     def __enter__(self):
#         self._total_run += 1
#         return self._db

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print(f'\nRunned total times => {self._total_run}')

#     def __del__(self):
#         self._db = None
#         del self._db
#         remove(self._db_path)


def setup_database(func):
    '''Setup e pulizia del database per eseguire i vari test'''
    @wraps(func)
    def func_wrapper(self):
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


def return_record(record_name: str) -> Dict:
    return {
        'symbol': record_name,
        'timeframe': 30,
        'days': 20,
        'decimal': 5,
        'offset': 2,
        'tpo_size': 10,
        'profiles': [
            1,
            2,
            3,
            4],
        'active': True}


class TestTinyDatabase(TestCase):

    # Una volta per istanza
    @classmethod
    def setUpClass(cls) -> None:
        pass

    # Una volta per test
    def setUp(self) -> None:
        self.db_name = './tests/test_connectors/test_tinydb.json'
        self.db = TinyDatabase(self.db_name)

    # Una volta per test
    def tearDown(self) -> None:
        del self.db
        remove(self.db_name)

    # Una volta per istanza
    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_select_table(self):
        table_name = 'testselecttable'
        self.db.select_table(table_name)
        self.db.add({'BTEST': 4321})
        tables = self.db.get_tables().pop()
        self.assertEqual(tables, table_name)

    def test_add(self):
        record = return_record('TEST')
        id = self.db.add(record)
        self.assertEqual(id, 1)

    def test_get_all(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        db_len = len(self.db)
        self.assertEqual(db_len, 10)

    def test_get_all_no_add(self):
        db_len = len(self.db)
        self.assertEqual(db_len, 0)

    def test_get_with_int(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        res = self.db.get(5)
        self.assertDictEqual(res, return_record('TEST4'))

    def test_get_with_int_wrong_id(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        res = self.db.get(99)
        self.assertEqual(res, None)

    def test_remove_multiple(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        res = self.db.remove([1, 3, 8])
        self.assertListEqual(res, [1, 3, 8])

    def test_remove_no_records(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        res = self.db.remove([])
        self.assertListEqual(res, [])

    def test_remove_update(self):
        for i in range(10):
            record = return_record(f'TEST{i}')
            self.db.add(record)
        self.db.update([5], {'timeframe': 60})
        res = self.db.get(5)['timeframe']
        self.assertEqual(res, 60)
