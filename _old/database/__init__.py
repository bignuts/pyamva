from tinydb import TinyDB, Query
from typing import List, Dict, Optional
import abc


class Param:
    """Classe per la definizione dei parametri"""

    def __init__(self,
                 symbol: str = '',
                 timeframe: str = '',
                 days: int = -1,
                 decimal: int = -1,
                 offset: int = -1,
                 tpo_size: int = -1,
                 profiles: List[int] = [],
                 active: bool = False) -> None:

        self.symbol = symbol
        self.timeframe = timeframe
        self.days = days
        self.decimal = decimal
        self.offset = offset
        self.tpo_size = tpo_size
        self.profiles = profiles
        self.active = active

    @classmethod
    def from_dict(cls, d: Dict):
        symbol = d.get('symbol', '')
        timeframe = d.get('timeframe', '')
        days = d.get('days', -1)
        decimal = d.get('decimal', -1)
        offset = d.get('offset', -1)
        tpo_size = d.get('tpo_size', -1)
        profiles = d.get('profiles', [])
        active = d.get('active', False)
        return cls(symbol, timeframe, days, decimal, offset, tpo_size, profiles, active)

    def to_dict(self) -> Dict:
        return {'symbol': self.symbol,
                'timeframe': self.timeframe,
                'days': self.days,
                'decimal': self.decimal,
                'offset': self.offset,
                'tpo_size': self.tpo_size,
                'profiles': self.profiles,
                'active': self.active}

    def to_list(self) -> List:
        return [self.symbol,
                self.timeframe,
                self.days,
                self.decimal,
                self.offset,
                self.tpo_size,
                self.profiles,
                self.active]


class IDatabase:
    """Interfaccia per collegamento e operazioni con il Database"""

    def __init__(self, name: str = './/database//db.json'):
        self.__db = TinyDB(name)

    @abc.abstractclassmethod
    def add(self, param: Param) -> bool:
        pass

    @abc.abstractclassmethod
    def get_all(self) -> List[Param]:
        pass

    @abc.abstractclassmethod
    def get(self, symbol: str) -> Param:
        pass

    # @abc.abstractclassmethod
    # def get_active(self) -> List[Param]:
    #     pass

    @abc.abstractclassmethod
    def update(self, param: Param) -> bool:
        pass

    @abc.abstractclassmethod
    def remove(self, symbol: str) -> None:
        pass


class TinyDatabase(IDatabase):
    """Implementazione di IDatabase usando TinyDB"""

    def __init__(self, name: str = './/database//db.json'):
        self.__db = TinyDB(name)

    def add(self, param: Param) -> bool:
        if not self._exist(param.symbol):
            id = self.__db.insert(param.to_dict())
            return bool(id)
        return False

    def get_all(self) -> List[Param]:
        d_list = self.__db.all()
        l: List[Param] = []
        for d in d_list:
            l.append(Param.from_dict(d))
        return l

    def get(self, symbol: str) -> Param:
        d = self.__db.search(Query().symbol == symbol)[0]
        return Param.from_dict(d)

    def get_active(self) -> List[Param]:
        d_list = self.__db.search(Query().active == True)
        l: List[Param] = []
        for d in d_list:
            l.append(Param.from_dict(d))
        return l

    def update(self, param: Param) -> bool:
        if self._exist(param.symbol):
            self.__db.update(param.to_dict(), Query().symbol == param.symbol)
            return True
        return False

    def remove(self, symbol: str) -> None:
        self.__db.remove(Query().symbol == symbol)

    def _exist(self, symbol: str) -> bool:
        return bool(len(self.__db.search(Query().symbol == symbol)))
