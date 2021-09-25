from typing import List, Dict, Optional
from tinydb import TinyDB, Query
from tinydb.table import Document
from databases.interfaces import IDatabase
from databases.models import Param



class TinyDatabase(IDatabase):
    """Implementazione di IDatabase usando TinyDB"""

    def __init__(self, dbpath: str = './tinydb.json'):
        self._db = self.connect(dbpath)

    def __del__(self):
        self.disconnect()

    def connect(self, dbpath) -> TinyDB:
        return TinyDB(dbpath)

    def disconnect(self) -> None:
        self._db.close()

    def select_table(self, table_name: str):
        # self._db = self._db.table(table_name)
        return self._db.table(table_name)

    def add(self, record: Param) -> int:
        return self._db.insert(record)

    def get_all(self) -> List[Dict]: 
        return self._db.all()

    def __len__(self) -> int:
        return len(self._db)

    def get(self, id: int) -> Optional[Dict]:
        return self._db.get(doc_id=id)

    # def get(self, symbol: str) -> Param:
    #     dict = self._db.search(Query().symbol == symbol)
    #     if dict:
    #         return dict[0]
    #     else:
    #         return Param(symbol='NONEXISTING', timeframe=-1, days=-1, decimal=-1,
    #                      offset=-1, tpo_size=-1, profiles=[], active=False)

    # def remove(self, symbol: str) -> int:
    #     removed_ids = self._db.remove(Query().symbol == symbol)
    #     if removed_ids:
    #         return removed_ids[0]
    #     else:
    #         return 0

    # def _exist(self, symbol: str) -> bool:
    #     return bool(len(self._db.search(Query().symbol == symbol)))

    # def get_all(self) -> List[Param]:
    #     # d_list = self._db.all()
    #     # l: List[Param] = []
    #     # for d in d_list:
    #     #     l.append(d)
    #     # return l
    #     return self._db.all()

    # def get_active(self) -> List[Param]:
    #     d_list = self._db.search(Query().active == True)
    #     l: List[Param] = []
    #     for d in d_list:
    #         l.append(d)
    #     return l

    # def update(self, param: Param) -> bool:
    #     if self._exist(param['symbol']):
    #         self._db.update(param, Query().symbol == param['symbol'])
    #         return True
    #     return False
