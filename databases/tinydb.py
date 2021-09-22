from typing import List
from tinydb import TinyDB, Query
from databases.interfaces import IDatabase
from databases.structs import Param


class TinyDatabase(IDatabase):
    """Implementazione di IDatabase usando TinyDB"""

    def __init__(self, dbpath: str = './tinydb.json'):
        self._db = TinyDB(dbpath)

    def connect(self) -> None:
        return super().connect()

    def disconnect(self) -> None:
        return super().disconnect()

    def add(self, param: Param) -> bool:
        if not self._exist(param.symbol):
            id = self._db.insert(param.to_dict())
            return bool(id)
        return False

    def get_all(self) -> List[Param]:
        d_list = self._db.all()
        l: List[Param] = []
        for d in d_list:
            l.append(Param.from_dict(d))
        return l

    def get(self, symbol: str) -> Param:
        d = self._db.search(Query().symbol == symbol)[0]
        return Param.from_dict(d)

    def get_active(self) -> List[Param]:
        d_list = self._db.search(Query().active == True)
        l: List[Param] = []
        for d in d_list:
            l.append(Param.from_dict(d))
        return l

    def update(self, param: Param) -> bool:
        if self._exist(param.symbol):
            self._db.update(param.to_dict(), Query().symbol == param.symbol)
            return True
        return False

    def remove(self, symbol: str) -> None:
        self._db.remove(Query().symbol == symbol)

    def _exist(self, symbol: str) -> bool:
        return bool(len(self._db.search(Query().symbol == symbol)))
