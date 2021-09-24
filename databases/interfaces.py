from abc import ABC, abstractmethod
from typing import Any, Dict, List
from databases.models import Param


class IDatabase(ABC):
    '''Interfaccia per collegamento e operazioni con il dabase'''

    @abstractmethod
    def connect(self, db_path: str):
        '''Metodo per connettersi al database e restituisce un'istanza ad esso'''
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def add(self, record: Param) -> int:
        pass

    # @abstractmethod
    # def get_all(self):
    #     pass

    # @abstractmethod
    # def get(self, key):
    #     pass

    # @abstractmethod
    # def update(self, record):
    #     pass

    # @abstractmethod
    # def remove(self, key):
    #     pass
