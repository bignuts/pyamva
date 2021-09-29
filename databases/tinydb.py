from typing import Dict, Optional, Sequence, Set, List
from tinydb import TinyDB, Query
from databases.interfaces import IDatabase

# https://tinydb.readthedocs.io/en/latest/


class TinyDatabase(IDatabase):
    """
    Implementazione di IDatabase usando TinyDB
    """

    def __init__(self, dbpath: str = './tinydb.json'):
        self._db: TinyDB
        self._connect(dbpath)
        self._table = self._db.table('_default')

    def __del__(self):
        self._disconnect()

    def _connect(self, dbpath) -> None:
        self._db = TinyDB(dbpath)

    def _disconnect(self) -> None:
        self._db.close()

    def select_table(self, table_name: str) -> None:
        self._table = self._db.table(table_name)

    def get_tables(self) -> Set[str]:
        return self._db.tables()

    def add(self, record: Dict) -> int:
        return self._table.insert(record)

    def get_all(self) -> Sequence[Dict]:
        return self._table.all()

    def __len__(self) -> int:
        return len(self._table)

    def get(self, id: int) -> Optional[Dict]:
        return self._table.get(doc_id=id)

    def remove(self, id: List[int]) -> List[int]:
        return self._table.remove(doc_ids=id)

    def update(self, id: List[int], fields) -> List[int]:
        return self._table.update(fields, doc_ids=id)
